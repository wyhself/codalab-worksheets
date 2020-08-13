import unittest
from mock import Mock
from bottle import local, request
import os
import json
import uuid
from .base import BaseTestCase
from freezegun import freeze_time


@freeze_time("2012-01-14")
class BundlesTest(BaseTestCase):
    def test_create(self):
        worksheet_id = self.create_worksheet()
        body = {
            'data': [
                {
                    'type': 'bundles',
                    'attributes': {
                        'bundle_type': 'run',
                        'command': 'echo TEST',
                        'metadata': {
                            'name': 'run-echo',
                            'description': '',
                            'tags': [''],
                            'allow_failed_dependencies': False,
                            'request_docker_image': 'codalab/default-cpu:latest',
                            'request_time': '',
                            'request_memory': '4g',
                            'request_disk': '',
                            'request_cpus': 1,
                            'request_gpus': 0,
                            'request_queue': '',
                            'request_priority': 0,
                            'request_network': False,
                            'exclude_patterns': [],
                        },
                        'dependencies': [],
                    },
                }
            ]
        }
        response = self.app.post_json(f'/rest/bundles?worksheet={worksheet_id}', body)
        self.assertEqual(response.status_int, 200)
        bundle_id = response.json["data"][0]["id"]
        self.assertEqual(
            response.json["data"],
            [
                {
                    "type": "bundles",
                    "attributes": {
                        "permission": 2,
                        "data_hash": None,
                        "uuid": bundle_id,
                        "args": "run \"echo TEST\" --request-cpus 1 --request-docker-image codalab/default-cpu:latest --request-memory 4g",
                        "metadata": {
                            "request_docker_image": "codalab/default-cpu:latest",
                            "allow_failed_dependencies": False,
                            "request_disk": "",
                            "actions": [],
                            "created": 1326499200,
                            "name": "run-echo",
                            "request_time": "",
                            "request_cpus": 1,
                            "request_gpus": 0,
                            "request_network": False,
                            "exclude_patterns": [],
                            "description": "",
                            "request_queue": "",
                            "tags": [""],
                            "request_memory": "4g",
                            "request_priority": 0,
                        },
                        "permission_spec": "all",
                        "is_anonymous": False,
                        "state": "created",
                        "bundle_type": "run",
                        "command": "echo TEST",
                        "dependencies": [],
                    },
                    "relationships": {"owner": {"data": {"type": "users", "id": "0"}}},
                    "id": bundle_id,
                }
            ],
        )