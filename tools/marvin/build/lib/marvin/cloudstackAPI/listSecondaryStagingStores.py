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


"""Lists secondary staging stores."""
from baseCmd import *
from baseResponse import *
class listSecondaryStagingStoresCmd (baseCmd):
    def __init__(self):
        self.isAsync = "false"
        """the ID of the staging store"""
        self.id = None
        """List by keyword"""
        self.keyword = None
        """the name of the staging store"""
        self.name = None
        """"""
        self.page = None
        """"""
        self.pagesize = None
        """the staging store protocol"""
        self.protocol = None
        """the staging store provider"""
        self.provider = None
        """the Zone ID for the staging store"""
        self.zoneid = None
        self.required = []

class listSecondaryStagingStoresResponse (baseResponse):
    def __init__(self):
        """the ID of the image store"""
        self.id = None
        """the details of the image store"""
        self.details = None
        """the name of the image store"""
        self.name = None
        """the protocol of the image store"""
        self.protocol = None
        """the provider name of the image store"""
        self.providername = None
        """the scope of the image store"""
        self.scope = None
        """the url of the image store"""
        self.url = None
        """the Zone ID of the image store"""
        self.zoneid = None
        """the Zone name of the image store"""
        self.zonename = None
