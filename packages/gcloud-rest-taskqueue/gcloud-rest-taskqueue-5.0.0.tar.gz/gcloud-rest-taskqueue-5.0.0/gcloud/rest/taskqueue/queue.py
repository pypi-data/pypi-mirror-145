"""
An asynchronous push queue for Google Appengine Task Queues
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
import io
import json
import logging
import os
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import backoff
from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[no-redef]

API_ROOT = 'https://cloudtasks.googleapis.com'
LOCATION = 'us-central1'
SCOPES = [
    'https://www.googleapis.com/auth/cloud-tasks',
]

CLOUDTASKS_EMULATOR_HOST = os.environ.get('CLOUDTASKS_EMULATOR_HOST')
if CLOUDTASKS_EMULATOR_HOST:
    API_ROOT = 'http://{}'.format((CLOUDTASKS_EMULATOR_HOST))

log = logging.getLogger(__name__)


class PushQueue(object):
    def __init__(self, project     , taskqueue     ,
                 service_file                                  = None,
                 location      = LOCATION,
                 session                    = None,
                 token                  = None)        :
        self.base_api_root = '{}/v2beta3'.format((API_ROOT))
        self.api_root = ('{}/projects/{}/'
                         'locations/{}/queues/{}'.format((self.base_api_root), (project), (location), (taskqueue)))
        self.session = SyncSession(session)
        self.token = token or Token(service_file=service_file, scopes=SCOPES,
                                    session=self.session.session)

    def headers(self)                  :
        if CLOUDTASKS_EMULATOR_HOST:
            return {'Content-Type': 'application/json'}

        token = self.token.get()
        return {
            'Authorization': 'Bearer {}'.format((token)),
            'Content-Type': 'application/json',
        }

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/create
    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def create(self, task                ,
                     session                    = None)       :
        url = '{}/tasks'.format((self.api_root))
        payload = json.dumps({
            'task': task,
            'responseView': 'FULL',
        }).encode('utf-8')

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, data=payload)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/delete
    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def delete(self, tname     ,
                     session                    = None)       :
        url = '{}/{}'.format((self.base_api_root), (tname))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.delete(url, headers=headers)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/get
    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def get(self, tname     , full       = False,
                  session                    = None)       :
        url = '{}/{}'.format((self.base_api_root), (tname))
        params = {
            'responseView': 'FULL' if full else 'BASIC',
        }

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, params=params)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/list
    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def list(self, full       = False, page_size      = 1000,
                   page_token      = '',
                   session                    = None)       :
        url = '{}/tasks'.format((self.api_root))
        params = {
            'responseView': 'FULL' if full else 'BASIC',
            'pageSize': page_size,
            'pageToken': page_token,
        }

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, params=params)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/run
    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def run(self, tname     , full       = False,
                  session                    = None)       :
        url = '{}/{}:run'.format((self.base_api_root), (tname))
        payload = json.dumps({
            'responseView': 'FULL' if full else 'BASIC',
        }).encode('utf-8')

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, data=payload)
        return resp.json()

    def close(self)        :
        self.session.close()

    def __enter__(self)               :
        return self

    def __exit__(self, *args     )        :
        self.close()
