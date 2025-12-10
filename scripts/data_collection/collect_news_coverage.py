#!/usr/bin/env python3
"""
Collect News and Media Coverage

Script to help search news databases and media sources.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
NEWS_DIR = PROJECT_ROOT / 'research/news'

# News sources to search
NEWS_SOURCES = [
    {
        'name': 'Washington Post',
        'url': 'https://www.washingtonpost.com/',
        'search_method': 'Website search or archive',
    },
    {
        'name': 'Washington City Paper',
        'url': 'https://washingtoncitypaper.com/',
        'search_method': 'Website search',
    },
    {
        'name': 'Alexandria Times',
        'url': 'https://alextimes.com/',
        'search_method': 'Website search',
    },
    {
        'name': 'Northern Virginia Magazine',
        'url': 'https://www.northernvirginiamag.com/',
        'search_method': 'Website search',
    },
    {
        'name': 'Virginia Business',
        'url': 'https://www.virginiabusiness.com/',
        'search_method': 'Website search',
    },
    {
        'name': 'Richmond Times-Dispatch',
        'url': 'https://www.richmond.com/',
        'search_method': 'Website search or archive',
    },
    {
        'name': 'Multi-Housing News',
        'url': 'https://www.multihousingnews.com/',
        'search_method': 'Website search',
    },
    {
        'name': 'National Real Estate Investor',
        'url': 'https://www.nreionline.com/',
        'search_method': 'Website search',
    },
]

# Search terms
SEARCH_TERMS = [
    'Kettler Management violation',
    'Kettler Management complaint',
    'Kettler Management discrimination',
    'Kettler Management fraud',
    'Edward Hyland',
    '800 Carlyle violation',
    'Kettler Management unlicensed',
    'Kettler Management license',
]


def create_news_template():
    """Create template for news coverage."""
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    
    template = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'News and media coverage documentation',
        },
        'violation_coverage': [],
        'company_announcements': [],
        'legal_proceedings': [],
        'regulatory_actions': [],
        'industry_publications': [],
        'sources_searched': NEWS_SOURCES,
        'search_terms': SEARCH_TERMS,
    }
    
    filepath = NEWS_DIR / 'violations_coverage.json'
    filepath.write_text(json.dumps(template, indent=2) + '\n')
    print(f"Created {filepath}")
    
    # Legal proceedings template
    legal_file = NEWS_DIR / 'legal_proceedings.json'
    legal_data = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Legal proceedings and court cases',
        },
        'court_cases': [],
        'lawsuits': [],
        'search_sources': [
            'Public court records',
            'PACER (federal courts)',
            'State court databases',
        ],
    }
    legal_file.write_text(json.dumps(legal_data, indent=2) + '\n')
    print(f"Created {legal_file}")
    
    return filepath


def print_search_instructions():
    """Print search instructions."""
    print("=== News and Media Coverage Search Instructions ===\n")
    
    print("Search Terms:")
    for term in SEARCH_TERMS:
        print(f"  - {term}")
    print()
    
    print("Sources to Search:")
    for source in NEWS_SOURCES:
        print(f"  {source['name']}: {source['url']}")
        print(f"    Method: {source['search_method']}")
    print()


if __name__ == '__main__':
    create_news_template()
    print_search_instructions()
