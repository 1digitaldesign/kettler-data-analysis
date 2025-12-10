#!/usr/bin/env python3
"""
Docker MCP Server
Manages Docker containers and services for parallel execution
"""

import docker
import json
import subprocess
from typing import Dict, List, Any
from pathlib import Path

class DockerMCPServer:
    """Docker MCP Server for container management"""

    def __init__(self):
        self.client = docker.from_env()
        self.project_root = Path(__file__).parent.parent.parent

    def list_containers(self) -> List[Dict]:
        """List all running containers"""
        containers = self.client.containers.list(all=True)
        return [
            {
                'id': c.id[:12],
                'name': c.name,
                'status': c.status,
                'image': c.image.tags[0] if c.image.tags else 'unknown'
            }
            for c in containers
        ]

    def start_service(self, service_name: str) -> Dict[str, Any]:
        """Start a Docker Compose service"""
        try:
            result = subprocess.run(
                ['docker-compose', 'up', '-d', service_name],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            return {
                'status': 'success',
                'service': service_name,
                'output': result.stdout
            }
        except Exception as e:
            return {
                'status': 'error',
                'service': service_name,
                'error': str(e)
            }

    def stop_service(self, service_name: str) -> Dict[str, Any]:
        """Stop a Docker Compose service"""
        try:
            result = subprocess.run(
                ['docker-compose', 'stop', service_name],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            return {
                'status': 'success',
                'service': service_name,
                'output': result.stdout
            }
        except Exception as e:
            return {
                'status': 'error',
                'service': service_name,
                'error': str(e)
            }

    def scale_service(self, service_name: str, replicas: int) -> Dict[str, Any]:
        """Scale a Docker Compose service"""
        try:
            result = subprocess.run(
                ['docker-compose', 'up', '-d', '--scale', f'{service_name}={replicas}'],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            return {
                'status': 'success',
                'service': service_name,
                'replicas': replicas,
                'output': result.stdout
            }
        except Exception as e:
            return {
                'status': 'error',
                'service': service_name,
                'error': str(e)
            }

    def run_parallel_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run multiple tasks in parallel containers"""
        results = []

        for task in tasks:
            service_name = task.get('service', 'python-etl')
            command = task.get('command', [])
            env_vars = task.get('env', {})

            try:
                container = self.client.containers.run(
                    image=f'kettler-{service_name}:latest',
                    command=command,
                    environment=env_vars,
                    detach=True,
                    network='kettler-network',
                    volumes={
                        str(self.project_root / 'data'): {'bind': '/app/data', 'mode': 'rw'},
                        str(self.project_root / 'scripts'): {'bind': '/app/scripts', 'mode': 'ro'}
                    }
                )
                results.append({
                    'task_id': task.get('id'),
                    'container_id': container.id[:12],
                    'status': 'started'
                })
            except Exception as e:
                results.append({
                    'task_id': task.get('id'),
                    'status': 'error',
                    'error': str(e)
                })

        return results

    def get_service_logs(self, service_name: str, lines: int = 100) -> str:
        """Get logs from a service"""
        try:
            result = subprocess.run(
                ['docker-compose', 'logs', '--tail', str(lines), service_name],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            return f"Error getting logs: {str(e)}"

    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all services"""
        try:
            result = subprocess.run(
                ['docker-compose', 'ps', '--format', 'json'],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            services = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
            return {
                'status': 'success',
                'services': services
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Docker MCP Server')
    parser.add_argument('command', choices=['list', 'start', 'stop', 'scale', 'status', 'logs'])
    parser.add_argument('--service', type=str, help='Service name')
    parser.add_argument('--replicas', type=int, help='Number of replicas')
    parser.add_argument('--lines', type=int, default=100, help='Log lines')

    args = parser.parse_args()

    server = DockerMCPServer()

    if args.command == 'list':
        containers = server.list_containers()
        print(json.dumps(containers, indent=2))
    elif args.command == 'start' and args.service:
        result = server.start_service(args.service)
        print(json.dumps(result, indent=2))
    elif args.command == 'stop' and args.service:
        result = server.stop_service(args.service)
        print(json.dumps(result, indent=2))
    elif args.command == 'scale' and args.service and args.replicas:
        result = server.scale_service(args.service, args.replicas)
        print(json.dumps(result, indent=2))
    elif args.command == 'status':
        result = server.get_service_status()
        print(json.dumps(result, indent=2))
    elif args.command == 'logs' and args.service:
        logs = server.get_service_logs(args.service, args.lines)
        print(logs)

if __name__ == '__main__':
    main()
