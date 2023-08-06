from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
import io
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

from .bigquery import API_ROOT
from .bigquery import BigqueryBase

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[no-redef]


class Dataset(BigqueryBase):
    def __init__(self, dataset_name                = None,
                 project                = None,
                 service_file                                  = None,
                 session                    = None,
                 token                  = None)        :
        self.dataset_name = dataset_name
        super().__init__(project=project, service_file=service_file,
                         session=session, token=token)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/list
    def list_tables(
            self, session                    = None,
            timeout      = 60,
            params                           = None)                  :
        """List tables in a dataset."""
        project = self.project()
        if not self.dataset_name:
            raise ValueError('could not determine dataset,'
                             ' please set it manually')

        url = ('{}/projects/{}/datasets/'
               '{}/tables'.format((API_ROOT), (project), (self.dataset_name)))
        return self._get_url(url, session, timeout, params=params)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list
    def list_datasets(
            self, session                    = None,
            timeout      = 60,
            params                           = None)                  :
        """List datasets in current project."""
        project = self.project()

        url = ('{}/projects/{}/datasets'.format((API_ROOT), (project)))
        return self._get_url(url, session, timeout, params=params)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get
    def get(self, session                    = None,
                  timeout      = 60,
                  params                           = None)                  :
        """Get a specific dataset in current project."""
        project = self.project()
        if not self.dataset_name:
            raise ValueError('could not determine dataset,'
                             ' please set it manually')

        url = ('{}/projects/{}/datasets/'
               '{}'.format((API_ROOT), (project), (self.dataset_name)))
        return self._get_url(url, session, timeout, params=params)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert
    def insert(self, dataset                ,
                     session                    = None,
                     timeout      = 60)                  :
        """Create datasets in current project."""
        project = self.project()

        url = ('{}/projects/{}/datasets'.format((API_ROOT), (project)))
        return self._post_json(url, dataset, session, timeout)
