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

SD_temp={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/NICs/Links/Members/1/Links/Settings/$entity",
    "@odata.id": "{rb}Managers/Manager_1/NICs/NIC_1/SD",
    "@odata.type": "#EthernetNetworkInterface.1.00.0.EthernetNetworkInterface",
    "Name": "Manager NIC",
    "Description": "Management Network Interface",
    "FactoryMacAddress": "AA:BB:CC:DD:EE:FF",
    "MacAddress": "AA:BB:CC:DD:EE:FF",
    "LinkTechnology": "Ethernet",
    "SpeedMbps": 100,
    "Autosense": "true",
    "FullDuplex": "true",
    "FrameSize": 1500,
    "HostName": "MyHostName",
    "FQDN": "MyHostName.MyDomainName.com",
    "MaxIPv6StaticAddresses": 1,
    "VLANEnable": "true",
    "VLANId": 101,
    "IPv4Addresses": [
        {
            "Address": "192.168.0.10",
            "SubnetMask": "255.255.252.0",
            "AddressOrigin": "DHCP",
            "Gateway": "192.168.0.1",
            "Oem": {}
        }
    ],
    "IPv6AddressPolicyTable": [
        {
            "Prefix": "::1/128",
            "Precedence": 50,
            "Label": 0
        }
    ],
    "IPv6StaticAddresses": [
        {
            "Address": "fe80::1ec1:deff:fe6f:1e24",
            "PrefixLength": 16
        }
    ],
    "IPv6DefaultGateway": "fe80::1ec1:deff:fe6f:1e24",
    "IPv6Addresses": [
        {
            "Address": "fe80::1ec1:deff:fe6f:1e24",
            "PrefixLength": 64,
            "AddressOrigin": "SLAAC",
            "AddressState": "Preferred",
            "Oem": {}
        }
    ],
    "NameServers": [
        "TheNameServer"
    ],
    "Oem": {}
}


def get_SD_template(rest_base):

    c=SD_temp.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base)
    return c

    
