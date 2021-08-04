# Copyright Notice:
#
# Copyright (c) 2017-2021, The Storage Networking Industry Association.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither the name of The Storage Networking Industry Association (SNIA) nor
# the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#  THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright 2015-2021 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md

# ComputerSystem API File

"""
Collection API:  GET, POST
Singleton  API:  GET, POST, PATCH, DELETE
"""

import g

import sys, traceback
import logging
import copy
import json, os

from flask import jsonify
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.ComputerSystem import get_ComputerSystem_instance
from .ResetActionInfo_api import ResetActionInfo_API
from .ResetAction_api import ResetAction_API
from .processor import members as processors
from .memory import members as memory
from .ethernetinterface import members as ethernetinterfaces
from .simplestorage import members as simplestorage
from .ResourceBlock_api import members as resource_blocks
from .constants import *

members = {}

INTERNAL_ERROR = 500


# ComputerSystem Singleton API
class ComputerSystemAPI(Resource):

    # kwargs is used to pass in the wildcards values to be replaced
    # when an instance is created via get_<resource>_instance().
    #
    # The call to attach the API establishes the contents of kwargs.
    # All subsequent HTTP calls go through __init__.
    #
    # __init__ stores kwargs in wildcards, which is used to pass
    # values to the get_<resource>_instance() call.
    def __init__(self, **kwargs):
        logging.info('ComputerSystemAPI init called')
        self.root = PATHS['Root']
        self.systems = PATHS['Systems']['path']

    def memory_summary(self,ident):
        totalsysmem=sum([x['CapacityMiB']for x in
            list(memory.get(ident,{}).values()) if x['MemoryType']=='DRAM'])
        totalpsysmem=sum([x['CapacityMiB']for x in
            list(memory.get(ident,{}).values()) if 'NVDIMM' in x['MemoryType']])
        return {u'Status': {u'Health': 'OK', u'State': 'Enabled'},
                    u'TotalSystemMemoryGiB': totalsysmem,
                    u'TotalSystemPersistentMemoryGiB': totalpsysmem}

    def processor_summary(self,ident):
        procs=list(processors.get(ident,{}).values())
        if not procs:
            return {}
        return {u'Status': {u'Health': 'OK', u'State': 'Enabled'},
                    u'Count': len(procs),
                    u'Model': procs[0].get('Model','unknown')}

    # HTTP GET
    def get(self, ident):
        logging.info('ComputerSystemAPI GET called')
        if ident in members:
            resp = 404
            return resp
        path = os.path.join(self.root, self.systems, ident, 'index.json')
        try:
            systems_json = open(path)
            data = json.load(systems_json)
        except Exception as e:
            traceback.print_exc()
            raise Exception("Unable read file because of following error::{}".format(e))
        return jsonify(data)

    # HTTP PUT
    def put(self, ident):
        logging.info('ComputerSystemAPI PUT called')
        return 'PUT is not a supported command for ComputerSystemAPI', 405

    # HTTP POST
    # This is an emulator-only POST command that creates new resource
    # instances from a predefined template. The new instance is given
    # the identifier "ident", which is taken from the end of the URL.
    # PATCH commands can then be used to update the new instance.
    def post(self, ident):
        logging.info('ComputerSystemAPI POST called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            wildcards['linkMgr'] = 'UpdateWithPATCH'
            wildcards['linkChassis'] = ['UpdateWithPATCH']
            config=get_ComputerSystem_instance(wildcards)
            members[ident]=config
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PATCH
    def patch(self, ident):
        logging.info('ComputerSystemAPI PATCH called')
        raw_dict = request.get_json(force=True)
        try:
            # Update specific portions of the identified object
            for key, value in raw_dict.items():
                members[ident][key] = value
            resp = members[ident], 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP DELETE
    def delete(self, ident):
        logging.info('ComputerSystemAPI DELETE called')
        try:
            resp = 404
            if ident in members:
                if members[ident]['SystemType'] == 'Composed':
                    # Delete a composed system
                    resp = DeleteComposedSystem(ident)
                    resp = 200
                else:
                    # Delete a physical system
                    del(members[ident])
                    resp = 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# ComputerSystem Collection API
class ComputerSystemCollectionAPI(Resource):

    def __init__(self):
        logging.info('ComputerSystemCollectionAPI init called')
        self.root = PATHS['Root']
        self.systems = PATHS['Systems']['path']

    # HTTP GET
    def get(self):
        path = os.path.join(self.root, self.systems, 'index.json')
        try:
            systems_json = open(path)
            data = json.load(systems_json)
        except Exception as e:
            traceback.print_exc()
            return {"error": "Unable to read file because of following error::{}".format(e)}, 500

        return jsonify(data)

    # HTTP PUT
    def put(self):
        logging.info('ComputerSystemCollectionAPI PUT called')
        return 'PUT is not a supported command for ChassisCollectionAPI', 405

    def verify(self, config):
        #TODO: Implement a method to verify that the POST body is valid
        return True,{}

    # HTTP POST
    # POST should allow adding multiple instances to a collection.
    # For now, this only adds one instance.
    # TODO: 'id' should be obtained from the request data.
    # TODO: May need an update for composed systems.
    def post(self):
        logging.info('ComputerSystemCollectionAPI POST called')
        try:
            config = request.get_json(force=True)
            ok, msg = self.verify(config)
            if ok:
                members[config['Id']] = config
                resp = config, 201
            else:
                resp = msg, 400
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

        '''
        resp = INTERNAL_ERROR
        req = request.get_json()

        if req is not None:
            composed_system = CreateComposedSystem(req)
            resp = composed_system, 200
        else:
            resp = INTERNAL_ERROR

        return resp
        '''

    # HTTP PATCH
    def patch(self):
        logging.info('ComputerSystemCollectionAPI PATCH called')
        return 'PATCH is not a supported command for ChassisCollectionAPI', 405

    # HTTP DELETE
    def delete(self):
        logging.info('ComputerSystemCollectionAPI DELETE called')
        return 'DELETE is not a supported command for ChassisCollectionAPI', 405



def state_disabled(ident):
    try:
        resp = 404
        conf= members[ident]
        conf['Status']['State'] = 'Disabled'
    except Exception:
        traceback.print_exc()
        resp = INTERNAL_ERROR
    return resp

def state_enabled(ident):
        try:
            resp = 404
            conf= members[ident]
            conf['Status']['State'] = 'Enabled'
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


#class ComposedSystem(Resource):
#    def __init__(self):
#        pass

def CreateComposedSystem(req):
        rb = g.rest_base
        status = False      # if the request can be processed, status will become True

        # Verify Existence of Resource Blocks
        blocks = req['Links']['ResourceBlocks']
        map_zones = dict()

        resource_ids={'Processors':[],'Memory':[],'SimpleStorage':[],'EthernetInterfaces':[]}

        for block in blocks:
            block = block['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
            if block in resource_blocks:
                zones = resource_blocks[block]['Links']['Zones']
                for zone in zones:
                    if block in map_zones.keys():
                        map_zones[block].append(zone['@odata.id'].replace(rb + 'CompositionService/ResourceZones/',''))
                    else:
                        map_zones[block] = [zone['@odata.id'].replace(rb + 'CompositionService/ResourceZones/','')]

                for device_type in resource_ids.keys():
                    for device in resource_blocks[block][device_type]:
                        resource_ids[device_type].append(device)

            else:
                # One of the Resource Blocks in the request does not exist
                resp = INTERNAL_ERROR

        # Verify that they all are under, at least, one Resource Zone
        for k1 in map_zones.keys():
            counter = 0
            for k2 in map_zones.keys():
                if k1==k2:
                    break
                for item in map_zones[k1]:
                    if item in map_zones[k2]:
                        counter = counter +1
                        if counter == len(map_zones.keys()):
                            break
                if counter == len(map_zones.keys()):
                            break
            if counter == len(map_zones.keys()):
                            status = True
                            break


        if status == True:
            if req['Name'] not in members.keys():

                # Create Composed System
                new_system = CreateComputerSystem(resource_class_kwargs={'rb': g.rest_base, 'linkChassis': [], 'linkMgr': None})
                new_system.put(req['Name'])

                # Remove unecessary Links and add ResourceBlocks to Links (this is a bit of a hack though)
                del members[req['Name']]['Links']['ManagedBy']
                del members[req['Name']]['Links']['Chassis']
                del members[req['Name']]['Links']['Oem']

                # This should be done through the CreateComputerSystem
                members[req['Name']]['SystemType'] = 'Composed'

                members[req['Name']]['Links']['ResourceBlocks']=[]


                # Add links to Processors, Memory, SimpleStorage, etc
                for device_type in resource_ids.keys():
                    for device in resource_ids[device_type]:
                        if device_type == 'Processors':
                            device = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            device_back = device
                            block = device.split('/', 1)[0]
                            device = device.split('/', 1)[-1]
                            device = device.split('/', 1)[-1]
                            try:
                                processors[req['Name']][device_back] = processors[block][device]
                            except:
                                processors[req['Name']] = {}
                                processors[req['Name']][device_back] = processors[block][device]
                        elif device_type == 'Memory':
                            device = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            device_back = device
                            block = device.split('/', 1)[0]
                            device = device.split('/', 1)[-1]
                            device = device.split('/', 1)[-1]
                            try:
                                memory[req['Name']][device_back] = memory[block][device]
                            except:
                                memory[req['Name']] = {}
                                memory[req['Name']][device_back] = memory[block][device]
                        elif device_type == 'SimpleStorage':
                            device = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            device_back = device
                            block = device.split('/', 1)[0]
                            device = device.split('/', 1)[-1]
                            device = device.split('/', 1)[-1]
                            try:
                                simplestorage[req['Name']][device_back] = simplestorage[block][device]
                            except:
                                simplestorage[req['Name']] = {}
                                simplestorage[req['Name']][device_back] = simplestorage[block][device]
                        elif device_type == 'EthernetInterfaces':
                            device = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            device_back = device
                            block = device.split('/', 1)[0]
                            device = device.split('/', 1)[-1]
                            device = device.split('/', 1)[-1]
                            try:
                                ethernetinterfaces[req['Name']][device_back] = ethernetinterfaces[block][device]
                            except:
                                ethernetinterfaces[req['Name']] = {}
                                ethernetinterfaces[req['Name']][device_back] = ethernetinterfaces[block][device]


                # Add ResourceBlocks to Links
                for block in blocks:
                    members[req['Name']]['Links']['ResourceBlocks'].append({'@odata.id': block['@odata.id']})


                # Update Resource Blocks affected
                for block in blocks:
                    block = block['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                    resource_blocks[block]['CompositionStatus']['CompositionState'] = 'Composed'
                    resource_blocks[block]['Links']['ComputerSystems'].append({'@odata.id': members[req['Name']]['@odata.id']})

                return members[req['Name']]
            else:
                # System Name already exists
                return INTERNAL_ERROR

        else:
            return INTERNAL_ERROR

        return req


def DeleteComposedSystem(ident):
    rb = g.rest_base
    resource_ids={'Processors':[],'Memory':[],'SimpleStorage':[],'EthernetInterfaces':[]}

    # Verify if the System exists and if is of type - "SystemType": "Composed"
    if ident in members:
        if members[ident]['SystemType'] == 'Composed':

            # Remove Links to Composed System and change CompositionState (to 'Unused') in associated Resource Blocks

            for block in members[ident]['Links']['ResourceBlocks']:
                block = block['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                resource_blocks[block]['Links']['ComputerSystems']
                for index, item in enumerate(resource_blocks[block]['Links']['ComputerSystems']):
                    if resource_blocks[block]['Links']['ComputerSystems'][index]['@odata.id'].replace(rb + 'Systems/','') == ident:
                        del resource_blocks[block]['Links']['ComputerSystems'][index]
                        resource_blocks[block]['CompositionStatus']['CompositionState'] = 'Unused'

                        for device_type in resource_ids.keys():
                            for device in resource_blocks[block][device_type]:
                                resource_ids[device_type].append(device)

            # Remove links to Processors, Memory, SimpleStorage, etc
            for device_type in resource_ids.keys():
                    for device in resource_ids[device_type]:
                        if device_type == 'Processors':
                            device_back = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            del processors[ident][device_back]
                            if processors[ident]=={}: del processors[ident]
                        elif device_type == 'Memory':
                            device_back = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            del memory[ident][device_back]
                            if memory[ident]=={}: del memory[ident]
                        elif device_type == 'SimpleStorage':
                            device_back = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            del simplestorage[ident][device_back]
                            if simplestorage[ident]=={}: del simplestorage[ident]
                        elif device_type == 'EthernetInterfaces':
                            device_back = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            del ethernetinterfaces[ident][device_back]
                            if ethernetinterfaces[ident]=={}: del ethernetinterfaces[ident]

            # Remove Composed System from System list
            del members[ident]
            resp = 200
        else:
            # It is not a Composed System and therefore cannot be deleted as such"
            return INTERNAL_ERROR
    #

    return resp

def UpdateComposedSystem(req):
    resp = 201

    return resp

# CreateComputerSystem
#
# Called internally to create instances of a resource. If the
# resource has subordinate resources, those subordinate resource(s)
# are created automatically.
#
# Note: In 'init', the first time through, kwargs may not have any
# values, so we need to check. The call to 'init' stores the path
# wildcards. The wildcards are used to modify the resource template
# when subsequent calls are made to instantiate resources.
class CreateComputerSystem(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateComputerSystem init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])

    # Create instance
    def put(self, ident):
        logging.info('CreateComputerSystem put called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            wildcards['sys_id'] = ident
            config = get_ComputerSystem_instance(wildcards)
            members[ident] = config

            ResetAction_API(resource_class_kwargs={'rb': g.rest_base,'sys_id': ident})
            ResetActionInfo_API(resource_class_kwargs={'rb': g.rest_base,'sys_id': ident})

            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateComputerSystem init exit')
        return resp