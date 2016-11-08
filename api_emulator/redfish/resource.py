#
# Copyright (c) 2016 Intel Corporation. All Rights Reserved.
# Copyright (c) 2016, The Storage Networking Industry Association.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of The Storage Networking Industry Association (SNIA) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
Resource module based on Resource.0.9.2 (Redfish)
"""

class StateEnum(object):
    """
    States based on Resource.State in Resource.0.9.2 (Redfish)
    """
    ENABLED = 'Enabled'
    DISABLED = 'Disabled'
    OFFLINE = 'Offline'
    IN_TEST = 'InTest'
    STARTING = 'Starting'
    ABSENT = 'Absent'


class HealthEnum(object):
    """
    Health based on Resource.Health in Resource.0.9.2 (Redfish)
    """
    OK = 'OK'
    WARNING = 'Warning'
    CRITICAL = 'Critical'
    # WARNING: THIS IS NOT IN THE SPEC -- In the mockup data for system 1
    DEGRADED = 'Degraded'


def Status(state, health, health_rollup=None):
    """
    Status based on Resource.Status in Resource.0.9.2 (Redfish)
    """
    status = {'State': state, 'Health': health}

    if health_rollup is not None:
        status['HealthRollup'] = health_rollup
    return status
