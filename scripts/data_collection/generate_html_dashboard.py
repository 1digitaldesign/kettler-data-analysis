#!/usr/bin/env python3
"""
Generate an HTML progress dashboard for data collection.
Creates a visual, interactive progress report that can be opened in a browser.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
RESEARCH_DIR = BASE_DIR / "research"
OUTPUT_DIR = BASE_DIR / "outputs" / "reports"

def count_license_searches():
    """Count license search files."""
    license_dir = RESEARCH_DIR / "license_searches"
    if not license_dir.exists():
        return 0, 0

    # Count state directories
    states = [d for d in license_dir.iterdir() if d.is_dir()]
    total_states = 15  # Expected states
    completed_states = len(states)

    # Count total files
    total_files = sum(1 for f in license_dir.rglob("*.json") if f.is_file())

    return completed_states, total_states, total_files

def count_company_registrations():
    """Count company registration files."""
    reg_dir = RESEARCH_DIR / "company_registrations"
    if not reg_dir.exists():
        return 0, 12, 0

    # Count JSON files
    files = list(reg_dir.rglob("*.json"))
    complete = len([f for f in files if f.stat().st_size > 100])  # Non-empty files
    templates = len([f for f in files if f.stat().st_size <= 100])  # Template files

    return complete, 12, templates

def count_employee_roles():
    """Count employee role files."""
    emp_dir = RESEARCH_DIR / "employees"
    if not emp_dir.exists():
        return 0, 2

    files = list(emp_dir.glob("*.json"))
    return len(files), 2

def count_template_files(category_dir, expected_templates):
    """Count template files for a category."""
    if not category_dir.exists():
        return 0, expected_templates

    files = list(category_dir.rglob("*.json"))
    templates = len([f for f in files if f.stat().st_size <= 500])  # Template files
    return templates, expected_templates

def get_all_stats():
    """Get statistics for all categories."""
    stats = {}

    # License Searches
    completed_states, total_states, total_files = count_license_searches()
    stats['license_searches'] = {
        'completed': completed_states,
        'total': total_states,
        'files': total_files,
        'progress': int((completed_states / total_states) * 100) if total_states > 0 else 0,
        'status': 'complete' if completed_states == total_states else 'in_progress'
    }

    # Company Registrations
    complete, total, templates = count_company_registrations()
    stats['company_registrations'] = {
        'completed': complete,
        'total': total,
        'templates': templates,
        'progress': int((complete / total) * 100) if total > 0 else 0,
        'status': 'complete' if complete == total else ('templates_ready' if templates > 0 else 'not_started')
    }

    # Employee Roles
    emp_files, emp_total = count_employee_roles()
    stats['employee_roles'] = {
        'completed': emp_files,
        'total': emp_total,
        'progress': int((emp_files / emp_total) * 100) if emp_total > 0 else 0,
        'status': 'complete' if emp_files == emp_total else 'in_progress'
    }

    # Template categories
    template_categories = {
        'property_contracts': (RESEARCH_DIR / "contracts", 1),
        'regulatory_complaints': (RESEARCH_DIR / "complaints", 1),
        'financial_records': (RESEARCH_DIR / "financial", 1),
        'news_coverage': (RESEARCH_DIR / "news", 2),
        'fair_housing': (RESEARCH_DIR / "discrimination", 3),
        'professional_memberships': (RESEARCH_DIR / "professional", 2),
        'social_media': (RESEARCH_DIR / "online", 3),
    }

    for key, (dir_path, expected) in template_categories.items():
        templates, total_templates = count_template_files(dir_path, expected)
        stats[key] = {
            'templates': templates,
            'total_templates': total_templates,
            'progress': int((templates / total_templates) * 100) if total_templates > 0 else 0,
            'status': 'templates_ready' if templates > 0 else 'not_started'
        }

    return stats

def generate_html_dashboard():
    """Generate HTML dashboard."""
    stats = get_all_stats()

    # Calculate overall progress
    categories = [
        stats['license_searches'],
        stats['company_registrations'],
        stats['employee_roles'],
        stats['property_contracts'],
        stats['regulatory_complaints'],
        stats['financial_records'],
        stats['news_coverage'],
        stats['fair_housing'],
        stats['professional_memberships'],
        stats['social_media'],
    ]

    overall_progress = sum(cat['progress'] for cat in categories) / len(categories)
    complete_count = sum(1 for cat in categories if cat['status'] == 'complete')
    in_progress_count = sum(1 for cat in categories if cat['status'] in ['in_progress', 'templates_ready'])
    not_started_count = sum(1 for cat in categories if cat['status'] == 'not_started')

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Collection Progress Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }}
        .overall-progress {{
            background: #f5f5f5;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 40px;
            text-align: center;
        }}
        .overall-progress h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        .progress-bar-container {{
            background: #e0e0e0;
            border-radius: 25px;
            height: 40px;
            margin: 20px 0;
            overflow: hidden;
            position: relative;
        }}
        .progress-bar-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            border-radius: 25px;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .stat-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}
        .stat-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .categories {{
            display: grid;
            gap: 20px;
            margin-top: 30px;
        }}
        .category-card {{
            background: #f9f9f9;
            border-radius: 10px;
            padding: 25px;
            border-left: 5px solid #667eea;
        }}
        .category-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .category-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}
        .category-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        .status-complete {{
            background: #4caf50;
            color: white;
        }}
        .status-in-progress {{
            background: #ff9800;
            color: white;
        }}
        .status-templates-ready {{
            background: #2196f3;
            color: white;
        }}
        .status-not-started {{
            background: #9e9e9e;
            color: white;
        }}
        .category-progress-bar {{
            background: #e0e0e0;
            border-radius: 15px;
            height: 25px;
            margin: 10px 0;
            overflow: hidden;
        }}
        .category-progress-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            border-radius: 15px;
            transition: width 0.5s ease;
        }}
        .category-details {{
            margin-top: 10px;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Data Collection Progress Dashboard</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

        <div class="overall-progress">
            <h2>Overall Progress</h2>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: {overall_progress:.1f}%">
                    {overall_progress:.1f}%
                </div>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Complete</h3>
                    <div class="number">{complete_count}</div>
                </div>
                <div class="stat-card">
                    <h3>In Progress</h3>
                    <div class="number">{in_progress_count}</div>
                </div>
                <div class="stat-card">
                    <h3>Not Started</h3>
                    <div class="number">{not_started_count}</div>
                </div>
            </div>
        </div>

        <div class="categories">
            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">1. License Searches</div>
                    <div class="category-status status-{stats['license_searches']['status']}">
                        {'✅ Complete' if stats['license_searches']['status'] == 'complete' else '⚠️ In Progress'}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['license_searches']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['license_searches']['completed']}/{stats['license_searches']['total']} states complete | {stats['license_searches']['files']} files collected
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">2. Company Registrations</div>
                    <div class="category-status status-{stats['company_registrations']['status']}">
                        {'✅ Complete' if stats['company_registrations']['status'] == 'complete' else ('⚠️ Templates Ready' if stats['company_registrations']['status'] == 'templates_ready' else '⚠️ In Progress')}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['company_registrations']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['company_registrations']['completed']}/{stats['company_registrations']['total']} complete | {stats['company_registrations']['templates']} templates ready
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">3. Property Contracts</div>
                    <div class="category-status status-{stats['property_contracts']['status']}">
                        {'⚠️ Templates Ready' if stats['property_contracts']['status'] == 'templates_ready' else '❌ Not Started'}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['property_contracts']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['property_contracts']['templates']}/{stats['property_contracts']['total_templates']} templates created
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">4. Employee Roles</div>
                    <div class="category-status status-{stats['employee_roles']['status']}">
                        ✅ Complete
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['employee_roles']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['employee_roles']['completed']}/{stats['employee_roles']['total']} files complete
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">5. Regulatory Complaints</div>
                    <div class="category-status status-{stats['regulatory_complaints']['status']}">
                        {'⚠️ Templates Ready' if stats['regulatory_complaints']['status'] == 'templates_ready' else '❌ Not Started'}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['regulatory_complaints']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['regulatory_complaints']['templates']}/{stats['regulatory_complaints']['total_templates']} templates created
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">6. Financial Records</div>
                    <div class="category-status status-{stats['financial_records']['status']}">
                        {'⚠️ Templates Ready' if stats['financial_records']['status'] == 'templates_ready' else '❌ Not Started'}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['financial_records']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['financial_records']['templates']}/{stats['financial_records']['total_templates']} templates created
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">7. News Coverage</div>
                    <div class="category-status status-{stats['news_coverage']['status']}">
                        {'⚠️ Templates Ready' if stats['news_coverage']['status'] == 'templates_ready' else '❌ Not Started'}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['news_coverage']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['news_coverage']['templates']}/{stats['news_coverage']['total_templates']} templates created
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">8. Fair Housing</div>
                    <div class="category-status status-{stats['fair_housing']['status']}">
                        {'⚠️ Templates Ready' if stats['fair_housing']['status'] == 'templates_ready' else '❌ Not Started'}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['fair_housing']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['fair_housing']['templates']}/{stats['fair_housing']['total_templates']} templates created
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">9. Professional Memberships</div>
                    <div class="category-status status-{stats['professional_memberships']['status']}">
                        {'⚠️ Templates Ready' if stats['professional_memberships']['status'] == 'templates_ready' else '❌ Not Started'}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['professional_memberships']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['professional_memberships']['templates']}/{stats['professional_memberships']['total_templates']} templates created
                </div>
            </div>

            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">10. Social Media</div>
                    <div class="category-status status-{stats['social_media']['status']}">
                        {'⚠️ Templates Ready' if stats['social_media']['status'] == 'templates_ready' else '❌ Not Started'}
                    </div>
                </div>
                <div class="category-progress-bar">
                    <div class="category-progress-fill" style="width: {stats['social_media']['progress']}%"></div>
                </div>
                <div class="category-details">
                    {stats['social_media']['templates']}/{stats['social_media']['total_templates']} templates created
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write HTML file
    html_path = OUTPUT_DIR / "progress_dashboard.html"
    html_path.write_text(html)

    print(f"✅ HTML dashboard generated: {html_path}")
    print(f"   Open in browser: open {html_path}")

    return html_path

if __name__ == "__main__":
    generate_html_dashboard()
