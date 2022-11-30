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

# Resource implementation for - /redfish/v1/Systems/{ComputerSystemId}/Storage/{StorageId}/FileSystems/{FileSystemId}/CapacitySources/{CapacitySourceId}
# Program name - Capacity8_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Capacity8 import get_Capacity8_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Capacity8 Collection API
class Capacity8CollectionAPI(Resource):
	def __init__(self):
		logging.info('Capacity8 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ComputerSystemId, StorageId, FileSystemId):
		logging.info('Capacity8 Collection get called')
		path = os.path.join(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources', 'index.json').format(ComputerSystemId, StorageId, FileSystemId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ComputerSystemId, StorageId, FileSystemId):
		logging.info('Capacity8 Collection post called')

		if request.data:
			config = json.loads(request.data)
			if "@odata.type" in config:
				if "Collection" in config["@odata.type"]:
					return "Invalid data in POST body", 400

		if FileSystemId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources').format(ComputerSystemId, StorageId, FileSystemId)
		parent_path = os.path.dirname(path)
		if not os.path.exists(path):
			os.mkdir(path)
			create_collection (path, 'Capacity', parent_path)

		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		if request.data:
			config = json.loads(request.data)
			if "@odata.id" in config:
				return Capacity8API.post(self, ComputerSystemId, StorageId, FileSystemId, os.path.basename(config['@odata.id']))
			else:
				return Capacity8API.post(self, ComputerSystemId, StorageId, FileSystemId, str(res))
		else:
			return Capacity8API.post(self, ComputerSystemId, StorageId, FileSystemId, str(res))

	# HTTP PUT Collection
	def put(self, ComputerSystemId, StorageId, FileSystemId):
		logging.info('Capacity8 Collection put called')

		path = os.path.join(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources', 'index.json').format(ComputerSystemId, StorageId, FileSystemId)
		put_object (path)
		return self.get(ComputerSystemId)

# Capacity8 API
class Capacity8API(Resource):
	def __init__(self):
		logging.info('Capacity8 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ComputerSystemId, StorageId, FileSystemId, CapacitySourceId):
		logging.info('Capacity8 get called')
		path = create_path(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources/{3}', 'index.json').format(ComputerSystemId, StorageId, FileSystemId, CapacitySourceId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ComputerSystemId, StorageId, FileSystemId, CapacitySourceId):
		logging.info('Capacity8 post called')
		path = create_path(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources/{3}').format(ComputerSystemId, StorageId, FileSystemId, CapacitySourceId)
		collection_path = os.path.join(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources', 'index.json').format(ComputerSystemId, StorageId, FileSystemId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Capacity8CollectionAPI.post(self, ComputerSystemId, StorageId, FileSystemId)

		if CapacitySourceId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ComputerSystemId':ComputerSystemId, 'StorageId':StorageId, 'FileSystemId':FileSystemId, 'CapacitySourceId':CapacitySourceId, 'rb':g.rest_base}
			config=get_Capacity8_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Capacity8API POST exit')
		return resp

	# HTTP PUT
	def put(self, ComputerSystemId, StorageId, FileSystemId, CapacitySourceId):
		logging.info('Capacity8 put called')
		path = os.path.join(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources/{3}', 'index.json').format(ComputerSystemId, StorageId, FileSystemId, CapacitySourceId)
		put_object(path)
		return self.get(ComputerSystemId, StorageId, FileSystemId, CapacitySourceId)

	# HTTP PATCH
	def patch(self, ComputerSystemId, StorageId, FileSystemId, CapacitySourceId):
		logging.info('Capacity8 patch called')
		path = os.path.join(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources/{3}', 'index.json').format(ComputerSystemId, StorageId, FileSystemId, CapacitySourceId)
		patch_object(path)
		return self.get(ComputerSystemId, StorageId, FileSystemId, CapacitySourceId)

	# HTTP DELETE
	def delete(self, ComputerSystemId, StorageId, FileSystemId, CapacitySourceId):
		logging.info('Capacity8 delete called')
		path = create_path(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources/{3}').format(ComputerSystemId, StorageId, FileSystemId, CapacitySourceId)
		base_path = create_path(self.root, 'Systems/{0}/Storage/{1}/FileSystems/{2}/CapacitySources').format(ComputerSystemId, StorageId, FileSystemId)
		return delete_object(path, base_path)

