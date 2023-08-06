import pytest
import os
import json
import uuid
import shutil
from pyopereto.client import OperetoClient
import tempfile

TEMP_DIR = tempfile.gettempdir()
TEST_TEMP_DIR = os.path.join(TEMP_DIR, str(uuid.uuid4()))


@pytest.fixture(autouse=True, scope="session")
def config():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        print(f'Creating test temp dir {TEST_TEMP_DIR}')

    class TestConfig(object):
        def __init__(self):
            self.client = OperetoClient()
            self.execution_cycles = 10
            self.parallel_executions = 5
            self.execution_cycles_time_intervals = 5
            self.opereto_agent = 'opereto-worker-node-0'
            self.tempdir = TEST_TEMP_DIR
            self.testplan_pid = os.environ.get('OPERETO_TEST_BENCHMAR_TESTPLAN_PID') or ''

    test_config_obj = TestConfig()
    yield test_config_obj


@pytest.fixture(autouse=True, scope="session")
def results():
    test_results={
        'status': 'passed',
        'data': {}
    }

    yield test_results

    for test, results in test_results['data'].items():
        if results['status']=='failed':
            test_results['status']='failed'
            break

    test_results_file = os.path.join(TEMP_DIR, 'opereto_test_results.json')
    with open(test_results_file, 'w') as results_file:
        results_file.write(json.dumps(test_results))
    if os.path.exists(TEST_TEMP_DIR):
        print(f'Removing test temp dir {TEST_TEMP_DIR}')
        shutil.rmtree(TEST_TEMP_DIR)

@pytest.fixture(autouse=True, scope="session")
def tid():
    return str(uuid.uuid4())