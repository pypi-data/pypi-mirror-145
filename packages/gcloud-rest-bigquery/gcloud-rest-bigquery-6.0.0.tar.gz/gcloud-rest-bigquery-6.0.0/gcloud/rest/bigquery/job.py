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
from .bigquery import Disposition

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[no-redef]


class Job(BigqueryBase):
    def __init__(self, job_id                = None,
                 project                = None,
                 service_file                                  = None,
                 session                    = None,
                 token                  = None)        :
        self.job_id = job_id
        super().__init__(project=project, service_file=service_file,
                         session=session, token=token)

    @staticmethod
    def _make_query_body(
            query     ,
            write_disposition             ,
            use_query_cache      ,
            dry_run      , use_legacy_sql      ,
            destination_table               )                  :
        return {
            'configuration': {
                'query': {
                    'query': query,
                    'writeDisposition': write_disposition.value,
                    'destinationTable': {
                        'projectId': destination_table.project,
                        'datasetId': destination_table.dataset_name,
                        'tableId': destination_table.table_name,
                    } if destination_table else destination_table,
                    'useQueryCache': use_query_cache,
                    'useLegacySql': use_legacy_sql,
                },
                'dryRun': dry_run,
            },
        }

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get
    def get_job(self, session                    = None,
                      timeout      = 60)                  :
        """Get the specified job resource by job ID."""

        project = self.project()
        url = '{}/projects/{}/jobs/{}'.format((API_ROOT), (project), (self.job_id))

        return self._get_url(url, session, timeout)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults
    def get_query_results(self, session                    = None,
                                timeout      = 60,
                                params                           = None,
                                )                  :
        """Get the specified jobQueryResults by job ID."""

        project = self.project()
        url = '{}/projects/{}/queries/{}'.format((API_ROOT), (project), (self.job_id))

        return self._get_url(url, session, timeout, params=params)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel
    def cancel(self, session                    = None,
                     timeout      = 60)                  :
        """Cancel the specified job by job ID."""

        project = self.project()
        url = '{}/projects/{}/queries/{}/cancel'.format((API_ROOT), (project), (self.job_id))

        return self._post_json(url, {}, session, timeout)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
    def query(self, query_request                ,
                    session                    = None,
                    timeout      = 60)                  :
        """Runs a query synchronously and returns query results if completes
        within a specified timeout."""
        project = self.project()
        url = '{}/projects/{}/queries'.format((API_ROOT), (project))

        return self._post_json(url, query_request, session, timeout)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    def insert(self, job                ,
                     session                    = None,
                     timeout      = 60)                  :
        """Insert a new asynchronous job."""
        project = self.project()
        url = '{}/projects/{}/jobs'.format((API_ROOT), (project))

        return self._post_json(url, job, session, timeout)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery
    def insert_via_query(
            self, query     , session                    = None,
            write_disposition              = Disposition.WRITE_EMPTY,
            timeout      = 60, use_query_cache       = True,
            dry_run       = False, use_legacy_sql       = True,
            destination_table                = None)                  :
        """Create table as a result of the query"""
        project = self.project()
        url = '{}/projects/{}/jobs'.format((API_ROOT), (project))

        body = self._make_query_body(query=query,
                                     write_disposition=write_disposition,
                                     use_query_cache=use_query_cache,
                                     dry_run=dry_run,
                                     use_legacy_sql=use_legacy_sql,
                                     destination_table=destination_table)
        response = self._post_json(url, body, session, timeout)
        if not dry_run:
            self.job_id = response['jobReference']['jobId']
        return response

    def result(self,
                     session                    = None)                  :
        data = self.get_job(session)
        status = data.get('status', {})
        if status.get('state') == 'DONE':
            if 'errorResult' in status:
                raise Exception('Job finished with errors', status['errors'])
            return data

        raise OSError('Job results are still pending')
