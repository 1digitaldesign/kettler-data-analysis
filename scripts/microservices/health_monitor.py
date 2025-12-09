#!/usr/bin/env python3
"""
Health Monitor for Microservices
Monitors all services and reports health status
"""

import os
import time
import requests
import json
from datetime import datetime
from typing import Dict, List

SERVICE_DISCOVERY_URL = os.getenv('SERVICE_DISCOVERY_URL', 'http://service-discovery:8080')

def check_all_services() -> Dict:
    """Check health of all services"""
    try:
        response = requests.get(f"{SERVICE_DISCOVERY_URL}/api/v1/services", timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error checking services: {e}")

    return {'services': {}, 'timestamp': datetime.now().isoformat()}

def print_health_report(data: Dict):
    """Print human-readable health report"""
    print("=" * 60)
    print("Microservices Health Report")
    print("=" * 60)
    print(f"Timestamp: {data.get('timestamp', 'unknown')}")
    print()

    services = data.get('services', {})
    healthy_count = 0
    total_count = len(services)

    for service_name, service_data in services.items():
        status = service_data.get('status', 'unknown')
        status_icon = "✅" if status == 'healthy' else "❌" if status == 'unhealthy' else "⚠️"

        print(f"{status_icon} {service_name}: {status}")

        if status == 'healthy':
            healthy_count += 1

        health = service_data.get('health', {})
        if 'response_time' in health:
            print(f"   Response time: {health['response_time']:.3f}s")
        if 'error' in health:
            print(f"   Error: {health['error']}")
        print()

    print("=" * 60)
    print(f"Overall: {healthy_count}/{total_count} services healthy")
    print("=" * 60)

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Microservices Health Monitor')
    parser.add_argument('--watch', action='store_true', help='Watch mode (continuous monitoring)')
    parser.add_argument('--interval', type=int, default=30, help='Check interval in seconds')
    parser.add_argument('--json', action='store_true', help='Output JSON')

    args = parser.parse_args()

    if args.watch:
        print("Starting health monitor in watch mode...")
        print(f"Checking every {args.interval} seconds")
        print("Press Ctrl+C to stop")
        print()

        try:
            while True:
                data = check_all_services()
                print_health_report(data)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopping health monitor...")
    else:
        data = check_all_services()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print_health_report(data)

if __name__ == '__main__':
    main()
