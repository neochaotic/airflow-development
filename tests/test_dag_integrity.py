import os
import pytest
from airflow.models.dagbag import DagBag

# Defines the path to the DAGs folder relative to this test file.
DAGS_PATH = os.path.join(os.path.dirname(__file__), "..", "dags")

# Mark all tests in this file as 'unit' tests
pytestmark = pytest.mark.unit

@pytest.fixture(scope="session")
def dag_bag():
    """
    A pytest fixture that loads all DAGs once per test session.
    This is more efficient and provides a consistent DagBag object to all tests.
    """
    return DagBag(dag_folder=DAGS_PATH, include_examples=False)


def test_dag_bag_import_errors(dag_bag):
    """
    Verifies that the DagBag has no import errors, indicating that all DAGs
    can be parsed by Airflow without syntax or import issues.
    """
    assert not dag_bag.import_errors, f"DAG import errors found: {dag_bag.import_errors}"


def test_dags_adhere_to_best_practices(dag_bag):
    """
    Iterates over each DAG and verifies adherence to best practices:
    1.  Checks for cyclic dependencies.
    2.  Ensures 'owner' is defined in default_args.
    3.  Ensures the owner is not the default 'airflow'.
    4.  Ensures 'retries' is defined in default_args.
    """
    for dag_id, dag in dag_bag.dags.items():
        # 1. Check for cycles and other structural issues
        dag.validate()

        default_args = dag.default_args or {}

        # 2. & 3. Validate owner
        assert "owner" in default_args, f"DAG '{dag_id}' does not have an 'owner' in default_args."
        assert default_args.get("owner", "").lower() != "airflow", f"DAG '{dag_id}' has the default 'airflow' owner. Please set a specific owner."

        # 4. Validate retries
        assert "retries" in default_args, f"DAG '{dag_id}' does not have 'retries' configured in default_args."