#!/usr/bin/env python3
"""
Health Check Service
Monitors all services and provides health status
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List

class HealthChecker:
    """Health check service for all APIs"""

    def __init__(self):
        self.services = {
            'vector-api': {
                'url': 'http://localhost:8000',
                'endpoints': ['/health', '/api/v1/stats']
            },
            'r-api': {
                'url': 'http://localhost:8001',
                'endpoints': ['/health']
            }
        }

    def check_service(self, name: str, config: Dict) -> Dict:
        """Check health of a single service"""
        result = {
            'name': name,
            'status': 'unknown',
            'timestamp': datetime.now().isoformat(),
            'endpoints': {}
        }

        try:
            # Check main health endpoint
            health_url = f"{config['url']}/health"
            response = requests.get(health_url, timeout=5)

            if response.status_code == 200:
                result['status'] = 'healthy'
                result['endpoints']['health'] = {
                    'status': 'ok',
                    'response': response.json()
                }
            else:
                result['status'] = 'unhealthy'
                result['endpoints']['health'] = {
                    'status': 'error',
                    'status_code': response.status_code
                }
        except requests.exceptions.RequestException as e:
            result['status'] = 'unreachable'
            result['endpoints']['health'] = {
                'status': 'error',
                'error': str(e)
            }

        # Check additional endpoints
        for endpoint in config.get('endpoints', []):
            if endpoint == '/health':
                continue

            try:
                endpoint_url = f"{config['url']}{endpoint}"
                response = requests.get(endpoint_url, timeout=5)

                result['endpoints'][endpoint] = {
                    'status': 'ok' if response.status_code == 200 else 'error',
                    'status_code': response.status_code
                }
            except Exception as e:
                result['endpoints'][endpoint] = {
                    'status': 'error',
                    'error': str(e)
                }

        return result

    def check_all(self) -> Dict:
        """Check health of all services"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'services': {}
        }

        for name, config in self.services.items():
            results['services'][name] = self.check_service(name, config)

        # Overall status
        all_healthy = all(
            s['status'] == 'healthy'
            for s in results['services'].values()
        )
        results['overall_status'] = 'healthy' if all_healthy else 'degraded'

        return results

    def print_report(self, results: Dict):
        """Print human-readable health report"""
        print("=" * 60)
        print("Health Check Report")
        print("=" * 60)
        print(f"Timestamp: {results['timestamp']}")
        print(f"Overall Status: {results['overall_status'].upper()}")
        print()

        for name, service in results['services'].items():
            status_icon = "✅" if service['status'] == 'healthy' else "❌"
            print(f"{status_icon} {name}: {service['status']}")

            for endpoint, endpoint_data in service['endpoints'].items():
                endpoint_status = "✓" if endpoint_data['status'] == 'ok' else "✗"
                print(f"   {endpoint_status} {endpoint}: {endpoint_data['status']}")
            print()

def main():
    """Main entry point"""
    checker = HealthChecker()
    results = checker.check_all()

    # Output JSON for programmatic use
    if '--json' in sys.argv:
        print(json.dumps(results, indent=2))
        return

    checker.print_report(results)

    # Exit with error code if unhealthy
    if results['overall_status'] != 'healthy':
        sys.exit(1)

if __name__ == '__main__':
    main()
