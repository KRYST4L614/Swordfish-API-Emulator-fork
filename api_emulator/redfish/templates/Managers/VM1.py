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

VM={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/VirtualMedia/$entity",
    "@odata.id": "{rb}Managers_1/VirtualMedia",
    "@odata.type": "#VirtualMedia.1.00.0.VirtualMediaCollection",
    "Name": "Virtual Media Services",
    "Description": "iLO Virtual Media Services Settings",
    "Total": 2,
    "Links": {
        "Members@odata.count": 2,
        "Members": [
            {
                "@odata.id": "{rb}Managers/Manager_1/VM1/Floppy1"
            },
            {
                "@odata.id": "{rb}Managers/Manager_1/VM1/CD1"
            }
        ]
    },
    "Oem": {}
}


def get_VM1_template(rest_base):


    c=VM.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.type']=c['@odata.type'].format(rb=rest_base)
    c['Links']['Members'][0]['@odata.id']=c['Links']['Members'][0]['@odata.id'].format(rb=rest_base)
    c['Links']['Members'][1]['@odata.id']=c['Links']['Members'][1]['@odata.id'].format(rb=rest_base)
    return c

    

