from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
import io
import json
import os
from enum import Enum
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[no-redef]


API_ROOT = 'https://www.googleapis.com/bigquery/v2'
SCOPES = [
    'https://www.googleapis.com/auth/bigquery.insertdata',
    'https://www.googleapis.com/auth/bigquery',
]

BIGQUERY_EMULATOR_HOST = os.environ.get('BIGQUERY_EMULATOR_HOST')
if BIGQUERY_EMULATOR_HOST:
    API_ROOT = 'http://{}/bigquery/v2'.format((BIGQUERY_EMULATOR_HOST))


class SourceFormat(Enum):
    AVRO = 'AVRO'
    CSV = 'CSV'
    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    ORC = 'ORC'
    PARQUET = 'PARQUET'


class Disposition(Enum):
    WRITE_APPEND = 'WRITE_APPEND'
    WRITE_EMPTY = 'WRITE_EMPTY'
    WRITE_TRUNCATE = 'WRITE_TRUNCATE'


class SchemaUpdateOption(Enum):
    ALLOW_FIELD_ADDITION = 'ALLOW_FIELD_ADDITION'
    ALLOW_FIELD_RELAXATION = 'ALLOW_FIELD_RELAXATION'


class BigqueryBase(object):
    def __init__(self,
                 project                = None,
                 service_file                                  = None,
                 session                    = None,
                 token                  = None)        :
        self._project = project
        self.session = SyncSession(session)
        self.token = token or Token(service_file=service_file, scopes=SCOPES,
                                    session=self.session.session)

    def project(self)       :
        if self._project:
            return self._project

        if BIGQUERY_EMULATOR_HOST:
            self._project = str(os.environ.get('BIGQUERY_PROJECT_ID', 'dev'))
            return self._project

        self._project = self.token.get_project()
        if self._project:
            return self._project

        raise Exception('could not determine project, please set it manually')

    def headers(self)                  :
        if BIGQUERY_EMULATOR_HOST:
            return {}

        token = self.token.get()
        return {
            'Authorization': 'Bearer {}'.format((token)),
        }

    def _post_json(
            self, url     , body                , session                   ,
            timeout     )                  :
        payload = json.dumps(body).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=payload, headers=headers, params=None,
                            timeout=timeout)
        data                 = resp.json()
        return data

    def _get_url(
            self, url     , session                   ,
            timeout     ,
            params                           = None)                  :
        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, timeout=timeout,
                           params=params or {})
        data                 = resp.json()
        return data

    def close(self)        :
        self.session.close()

    def __enter__(self)                  :
        return self

    def __exit__(self, *args     )        :
        self.close()
