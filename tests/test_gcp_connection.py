import os

import pytest
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from google.api_core import exceptions

# Mark this entire test module as 'integration'
# It requires a live connection and valid credentials.
pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.environ.get("GCP_PROJECT_ID") == "ci-project",
    reason="Skipping live GCP connection test in CI environment",
)
def test_gcp_credentials_and_project_are_valid():
    """
    Attempts a simple, read-only operation against BigQuery to validate
    that the configured credentials and GCP_PROJECT_ID are valid.
    """
    try:
        # Use the default connection 'bigquery_default' which is configured on startup
        hook = BigQueryHook(gcp_conn_id="bigquery_default")

        # A lightweight way to check credentials and project validity.
        # This will fail if the project doesn't exist or if credentials are invalid.
        hook.get_client()

    except exceptions.PermissionDenied as e:
        pytest.fail(
            "GCP Permission Denied. Check if the authenticated user has the "
            f"'BigQuery User' role on project '{os.environ.get('GCP_PROJECT_ID')}'. Error: {e}"
        )
    except Exception as e:
        pytest.fail(f"An unexpected error occurred when connecting to GCP: {e}")