import pytest
import numpy
import shutil
import uuid
import os
import datetime
import time
import concurrent.futures

class TestBenchmark():

    def _run_async_task(self, concurrency, func, *args, **kwargs):

        responses=[]

        def _run_task():
            start_time = datetime.datetime.now()

            func(*args, **kwargs)
            
            end_time = datetime.datetime.now()
            time_diff = (end_time - start_time)
            execution_time = time_diff.total_seconds() * 1000
            return execution_time

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(concurrency):
                futures.append(
                    executor.submit(
                        _run_task
                    )
                )
            for future in concurrent.futures.as_completed(futures):
                responses.append(future.result())

        return responses


    def test_run_process(self, config, results):

        pids=[]
        max_registration_time = 3000.0
        max_start_time_50 = 6000.0
        max_start_time_75 = 10000.0

        registration_results = {
            'status': 'passed',
            'criteria': f'<{max_registration_time}/50%',
            'values': [],
        }
        start_results = {
            'status': 'passed',
            'criteria': f'<{max_start_time_50}/50%, <{max_start_time_75}/75%',
            'values': [],
        }

        def run_process():
            test_username=config.client.input['opereto_user']
            pid = config.client.create_process('shell_command', title=f'Created by Opereto benchmark test (originator: {test_username})', command='/bin/sh -c "ls -l"', agent=config.opereto_agent)
            pids.append(pid)

        for interations in range(config.execution_cycles):
            response_times = self._run_async_task(config.parallel_executions, run_process)
            registration_results['values']+=response_times
            time.sleep(config.execution_cycles_time_intervals)

        fail_test=False
        if numpy.percentile(registration_results['values'], 50, axis=None, out=None)>max_registration_time:
            registration_results['status']='failed'
            fail_test=True
        results['data']['process_registration_time']=registration_results
        if fail_test:
            pytest.fail(f'One of more process registration times exceeded {max_registration_time} ms')

        for pid in pids:
            process_info = config.client.get_process_info(pid)
            registered_time = datetime.datetime.strptime(process_info['orig_date'], '%Y-%m-%dT%H:%M:%S.%f')
            start_time = datetime.datetime.strptime(process_info['start_date'], '%Y-%m-%dT%H:%M:%S.%f')
            registered_to_start_diff = (start_time - registered_time).total_seconds() * 1000
            start_results['values'].append(registered_to_start_diff)
        if numpy.percentile(start_results['values'], 50, axis=None, out=None) > max_start_time_50 or \
                numpy.percentile(start_results['values'], 75, axis=None, out=None) > max_start_time_75:
            start_results['status'] = 'failed'
            fail_test=True
        results['data']['process_start_time'] = start_results
        if fail_test:
            pytest.fail(f'One of more process start times exceeded the average rate of {max_start_time_50} ms')


    def test_deploy_service_to_sandbox(self, config, results, tid):

        max_deploy_service_time_50 = 3000.0
        max_deploy_service_time_75 = 6000.0

        deploy_service_results = {
            'status': 'passed',
            'criteria': f'<{max_deploy_service_time_50}/50%, <{max_deploy_service_time_75}/75%',
            'values': [],
        }

        service_unique_name = 'opereto_banchmark_test_'+tid

        def deploy_process():
            temp_dir = config.tempdir
            source_service_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'microservices',
                                             'opereto_test_service')
            temp_service_directory = os.path.join(config.tempdir, str(uuid.uuid4()))
            shutil.copytree(source_service_directory, temp_service_directory)
            zip_action_file = os.path.join(temp_dir, str(uuid.uuid4()) + '.action')

            base_dir = os.path.basename(os.path.normpath(temp_service_directory))
            root_dir = os.path.dirname(temp_service_directory)
            shutil.make_archive(zip_action_file, "zip", root_dir, base_dir)
            config.client.upload_service_version(service_zip_file=zip_action_file+'.zip', mode='development', service_id=service_unique_name)
            
        fail_test = False

        try:
            print(f'\nUploading the following service in a loop: {service_unique_name}')
            for interations in range(config.execution_cycles):
                response_times = self._run_async_task(1, deploy_process)
                deploy_service_results['values']+=response_times
                time.sleep(config.execution_cycles_time_intervals)
        finally:
            print(f'deleting service: {service_unique_name}')
            config.client.delete_service(service_id=service_unique_name)

        if numpy.percentile(deploy_service_results['values'], 50, axis=None, out=None) > max_deploy_service_time_50 or \
                numpy.percentile(deploy_service_results['values'], 75, axis=None, out=None) > max_deploy_service_time_75:
            deploy_service_results['status'] = 'failed'
            fail_test=True
        results['data']['simple_service_deployment_time'] = deploy_service_results
        if fail_test:
            pytest.fail(f'One of more service deployment times exceeded the average rate of {max_deploy_service_time_50} ms')


    def test_view_process_rca(self, config, results):

        max_process_rca_time_50 = 5000.0
        max_process_rca_time_75 = 10000.0

        process_rca_results = {
            'status': 'passed',
            'criteria': f'{max_process_rca_time_50}/50%, <{max_process_rca_time_75}/75%',
            'values': []
        }
        fail_test = False

        selected_testplan_service=config.testplan_pid
        if not selected_testplan_service:
            testplan_services = config.client._call_rest_api(method='post', url='/search/processes',
                                                             data={
                                                                 'start': 0,
                                                                 'limit': 1,
                                                                 'filter': {
                                                                     'service_type': 'testplan'
                                                                 }
                                                             })
            selected_testplan_service = testplan_services[0]['id']

        process_rca_results['criteria'] += f' (pid={selected_testplan_service})'
        opereto_host = config.client.input['opereto_host']
        print(f'\nSelected test plan process to view RCA: {opereto_host}/ui#dashboard/flow/{selected_testplan_service}')

        def view_process_rca():
            config.client.get_process_rca(selected_testplan_service)

        for interations in range(config.execution_cycles):
            response_times = self._run_async_task(config.parallel_executions, view_process_rca)
            process_rca_results['values']+=response_times
            time.sleep(config.execution_cycles_time_intervals)

        if numpy.percentile(process_rca_results['values'], 50, axis=None, out=None) > max_process_rca_time_50 or \
                numpy.percentile(process_rca_results['values'], 75, axis=None, out=None) > max_process_rca_time_75:
            process_rca_results['status'] = 'failed'
            fail_test=True
        results['data']['random_testplan_process_rca_time'] = process_rca_results

        if fail_test:
            pytest.fail(f'One of more process rca_viea times exceeded the average rate of {max_process_rca_time_50} ms')

