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


"""Creates a new Pod."""
from baseCmd import *
from baseResponse import *
class createPodCmd (baseCmd):
    def __init__(self):
        self.isAsync = "false"
        """the gateway for the Pod"""
        """Required"""
        self.gateway = None
        """the name of the Pod"""
        """Required"""
        self.name = None
        """the netmask for the Pod"""
        """Required"""
        self.netmask = None
        """the starting IP address for the Pod"""
        """Required"""
        self.startip = None
        """the Zone ID in which the Pod will be created"""
        """Required"""
        self.zoneid = None
        """Allocation state of this Pod for allocation of new resources"""
        self.allocationstate = None
        """the ending IP address for the Pod"""
        self.endip = None
        self.required = ["gateway","name","netmask","startip","zoneid",]

class createPodResponse (baseResponse):
    def __init__(self):
        """the ID of the Pod"""
        self.id = None
        """the allocation state of the Pod"""
        self.allocationstate = None
        """the ending IP for the Pod"""
        self.endip = None
        """the gateway of the Pod"""
        self.gateway = None
        """the name of the Pod"""
        self.name = None
        """the netmask of the Pod"""
        self.netmask = None
        """the starting IP for the Pod"""
        self.startip = None
        """the Zone ID of the Pod"""
        self.zoneid = None
        """the Zone name of the Pod"""
        self.zonename = None
        """the capacity of the Pod"""
        self.capacity = []

class capacity:
    def __init__(self):
        """"the total capacity available"""
        self.capacitytotal = None
        """"the capacity currently in use"""
        self.capacityused = None
        """"the Cluster ID"""
        self.clusterid = None
        """"the Cluster name"""
        self.clustername = None
        """"the percentage of capacity currently in use"""
        self.percentused = None
        """"the Pod ID"""
        self.podid = None
        """"the Pod name"""
        self.podname = None
        """"the capacity type"""
        self.type = None
        """"the Zone ID"""
        self.zoneid = None
        """"the Zone name"""
        self.zonename = None
