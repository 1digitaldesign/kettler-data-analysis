#!/usr/bin/env python3
"""
Parallel Execution Orchestrator
Manages parallel execution of ETL and analysis tasks using Docker/Kubernetes
"""

import subprocess
import json
import time
from pathlib import Path
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelExecutor:
    """Orchestrates parallel execution of tasks"""

    def __init__(self, backend='docker'):
        self.backend = backend
        self.project_root = Path(__file__).parent.parent.parent

    def execute_docker_compose(self, services: List[str], scale: Dict[str, int] = None):
        """Execute services using Docker Compose"""
        if scale:
            for service, replicas in scale.items():
                subprocess.run(
                    ['docker-compose', 'up', '-d', '--scale', f'{service}={replicas}'],
                    cwd=self.project_root
                )
        else:
            subprocess.run(
                ['docker-compose', 'up', '-d'] + services,
                cwd=self.project_root
            )

    def execute_kubernetes(self, deployments: List[str], replicas: Dict[str, int] = None):
        """Execute services using Kubernetes"""
        for deployment in deployments:
            if replicas and deployment in replicas:
                subprocess.run([
                    'kubectl', 'scale', 'deployment', deployment,
                    f'--replicas={replicas[deployment]}'
                ])
            else:
                subprocess.run([
                    'kubectl', 'apply', '-f',
                    f'kubernetes/{deployment}-deployment.yaml'
                ])

    def run_etl_pipeline(self, parallel: bool = True):
        """Run ETL pipeline in parallel"""
        if parallel and self.backend == 'docker':
            # Scale ETL service to multiple replicas
            self.execute_docker_compose(['python-etl'], scale={'python-etl': 3})
        elif parallel and self.backend == 'kubernetes':
            self.execute_kubernetes(['python-etl'], replicas={'python-etl': 3})
        else:
            subprocess.run(['python3', 'scripts/etl/etl_pipeline.py'], cwd=self.project_root)

    def run_analysis_tasks(self, tasks: List[Dict[str, Any]], parallel: bool = True):
        """Run multiple analysis tasks in parallel"""
        if parallel and self.backend == 'docker':
            # Create multiple containers for parallel execution
            with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
                futures = []
                for task in tasks:
                    future = executor.submit(self._run_docker_task, task)
                    futures.append(future)

                results = []
                for future in as_completed(futures):
                    results.append(future.result())
                return results
        else:
            # Sequential execution
            results = []
            for task in tasks:
                results.append(self._run_task(task))
            return results

    def _run_docker_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single task in Docker container"""
        service = task.get('service', 'r-analysis')
        script = task.get('script')
        args = task.get('args', [])

        cmd = ['docker-compose', 'run', '--rm', service, 'Rscript', script] + args
        result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)

        return {
            'task': task.get('name'),
            'status': 'success' if result.returncode == 0 else 'error',
            'output': result.stdout,
            'error': result.stderr
        }

    def _run_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single task locally"""
        script = task.get('script')
        args = task.get('args', [])

        cmd = ['Rscript', script] + args
        result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)

        return {
            'task': task.get('name'),
            'status': 'success' if result.returncode == 0 else 'error',
            'output': result.stdout,
            'error': result.stderr
        }

    def monitor_services(self, services: List[str]) -> Dict[str, Any]:
        """Monitor service status"""
        status = {}

        for service in services:
            if self.backend == 'docker':
                result = subprocess.run(
                    ['docker-compose', 'ps', service],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                status[service] = {
                    'running': 'Up' in result.stdout,
                    'output': result.stdout
                }
            elif self.backend == 'kubernetes':
                result = subprocess.run(
                    ['kubectl', 'get', 'pods', '-l', f'app={service}'],
                    capture_output=True,
                    text=True
                )
                status[service] = {
                    'running': 'Running' in result.stdout,
                    'output': result.stdout
                }

        return status

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Parallel Execution Orchestrator')
    parser.add_argument('--backend', choices=['docker', 'kubernetes'], default='docker')
    parser.add_argument('--etl', action='store_true', help='Run ETL pipeline')
    parser.add_argument('--parallel', action='store_true', help='Run in parallel')
    parser.add_argument('--scale', type=int, help='Number of replicas')

    args = parser.parse_args()

    executor = ParallelExecutor(backend=args.backend)

    if args.etl:
        executor.run_etl_pipeline(parallel=args.parallel)

    if args.scale:
        if args.backend == 'docker':
            executor.execute_docker_compose(['python-etl'], scale={'python-etl': args.scale})
        elif args.backend == 'kubernetes':
            executor.execute_kubernetes(['python-etl'], replicas={'python-etl': args.scale})

if __name__ == '__main__':
    main()
