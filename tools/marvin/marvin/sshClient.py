# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import paramiko
import time
import cloudstackException
import contextlib
import logging
from marvin.codes import (
    SUCCESS, FAIL, INVALID_INPUT, EXCEPTION_OCCURRED
    )
from contextlib import closing


class SshClient(object):
    '''
    Added timeout flag for ssh connect calls.Default to 3.0 seconds
    '''
    def __init__(self, host, port, user, passwd, retries=20, delay=30,
                 log_lvl=logging.INFO, keyPairFiles=None, timeout=10.0):
        self.host = None
        self.port = 22
        self.user = user
        self.passwd = passwd
        self.keyPairFiles = keyPairFiles
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.logger = logging.getLogger('sshClient')
        self.retryCnt = 0
        self.delay = 0
        self.timeout = 3.0
        ch = logging.StreamHandler()
        ch.setLevel(log_lvl)
        self.logger.addHandler(ch)

        #Check invalid host value and raise exception
        #Atleast host is required for connection
        if host is not None and host != '':
            self.host = host
        if retries is not None and retries > 0:
            self.retryCnt = retries
        if delay is not None and delay > 0:
            self.delay = delay
        if timeout is not None and timeout > 0:
            self.timeout = timeout
        if port is not None or port >= 0:
            self.port = port
        if self.createConnection() == FAIL:
            raise cloudstackException.\
                internalError("Connection Failed")

    def execute(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.readlines()
        errors = stderr.readlines()
        results = []
        if output is not None and len(output) == 0:
            if errors is not None and len(errors) > 0:
                for error in errors:
                    results.append(error.rstrip())

        else:
            for strOut in output:
                results.append(strOut.rstrip())
        self.logger.debug("{Cmd: %s via Host: %s} {returns: %s}" %
                          (command, str(self.host), results))
        return results

    def createConnection(self):
        '''
        @Name: createConnection
        @Desc: Creates an ssh connection for
               retries mentioned,along with sleep mentioned
        @Output: SUCCESS on successful connection
                 FAIL If connection through ssh failed
        '''
        ret = FAIL
        while self.retryCnt >= 0:
            try:
                self.logger.debug("SSH Connection: Host:%s User:%s\
                                   Port:%s" %
                                  (self.host, self.user, str(self.port)
                                   ))
                if self.keyPairFiles is None:
                    self.ssh.connect(hostname=self.host,
                                     port=self.port,
                                     username=self.user,
                                     password=self.passwd,
                                     timeout=self.timeout)
                else:
                    self.ssh.connect(hostname=self.host,
                                     port=self.port,
                                     username=self.user,
                                     password=self.passwd,
                                     key_filename=self.keyPairFiles,
                                     timeout=self.timeout,
                                     look_for_keys=False
                                     )
                ret = SUCCESS
                break
            except Exception as se:
                self.retryCnt = self.retryCnt - 1
                if self.retryCnt == 0:
                    break
                time.sleep(self.delay)
        return ret

    def runCommand(self, command):
        '''
        @Name: runCommand
        @Desc: Runs a command over ssh and
               returns the result along with status code
        @Input: command to execute
        @Output: 1: status of command executed.
                 Default to None
                 SUCCESS : If command execution is successful
                 FAIL    : If command execution has failed
                 EXCEPTION_OCCURRED: Exception occurred while executing
                                     command
                 INVALID_INPUT : If invalid value for command is passed
                 2: stdin,stdout,stderr values of command output
        '''
        excep_msg = ''
        ret = {"status": None, "stdin": None, "stdout": None, "stderr": None}
        if command is None or command == '':
            ret["status"] = INVALID_INPUT
            return ret
        try:
            status_check = 1
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.readlines()
            errors = stderr.readlines()
            inp = stdin.readlines()
            ret["stdin"] = inp
            ret["stdout"] = output
            ret["stderr"] = errors
            if stdout is not None:
                status_check = stdout.channel.recv_exit_status()
            if status_check == 0:
                ret["status"] = SUCCESS
            else:
                ret["status"] = FAIL
        except Exception as e:
            excep_msg = str(e)
            ret["status"] = EXCEPTION_OCCURRED
        finally:
            self.logger.debug(" Host: %s Cmd: %s Output:%s Exception: %s" %
                              (self.host, command, str(ret), excep_msg))
            return ret

    def scp(self, srcFile, destPath):
        transport = paramiko.Transport((self.host, int(self.port)))
        transport.connect(username=self.user, password=self.passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.put(srcFile, destPath)
        except IOError, e:
            raise e

    def close(self):
            if self.ssh is not None:
                self.ssh.close()


if __name__ == "__main__":
    with contextlib.closing(SshClient("10.223.75.10", 22, "root",
                                            "password")) as ssh:
        print ssh.execute("ls -l")