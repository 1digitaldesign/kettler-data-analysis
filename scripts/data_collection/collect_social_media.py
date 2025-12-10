#!/usr/bin/env python3
"""
Collect Social Media and Online Presence

Script to help document company online presence and social media.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
ONLINE_DIR = PROJECT_ROOT / 'research/online'

# Company websites
COMPANY_WEBSITES = [
    {
        'name': 'Kettler Management',
        'url': None,  # To be filled
        'purpose': 'Service descriptions, geographic scope',
    },
]

# Social media platforms
SOCIAL_MEDIA_PLATFORMS = [
    {
        'platform': 'LinkedIn',
        'url': 'https://www.linkedin.com/',
        'search_for': ['Kettler Management', 'Company page', 'Employee profiles'],
    },
    {
        'platform': 'Facebook',
        'url': 'https://www.facebook.com/',
        'search_for': ['Kettler Management'],
    },
    {
        'platform': 'Twitter/X',
        'url': 'https://twitter.com/',
        'search_for': ['Kettler Management'],
    },
    {
        'platform': 'Instagram',
        'url': 'https://www.instagram.com/',
        'search_for': ['Kettler Management'],
    },
]

# Review platforms
REVIEW_PLATFORMS = [
    {
        'platform': 'Google Business',
        'url': 'https://www.google.com/maps/',
        'search_for': 'Kettler Management',
    },
    {
        'platform': 'Yelp',
        'url': 'https://www.yelp.com/',
        'search_for': 'Kettler Management',
    },
]


def create_social_media_template():
    """Create template for social media and online presence."""
    ONLINE_DIR.mkdir(parents=True, exist_ok=True)

    # Social media template
    social_file = ONLINE_DIR / 'social_media.json'
    social_data = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Social media and online presence documentation',
        },
        'company_websites': [],
        'linkedin': {
            'company_page': None,
            'employee_profiles': [],
            'role_descriptions': [],
        },
        'social_media_accounts': {},
        'platforms_searched': SOCIAL_MEDIA_PLATFORMS,
    }

    for platform in SOCIAL_MEDIA_PLATFORMS:
        social_data['social_media_accounts'][platform['platform']] = {
            'url': None,
            'content': [],
            'posts': [],
            'followers': None,
        }

    social_file.write_text(json.dumps(social_data, indent=2) + '\n')
    print(f"Created {social_file}")

    # Reviews template
    reviews_file = ONLINE_DIR / 'reviews.json'
    reviews_data = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Online reviews and ratings',
        },
        'google_reviews': [],
        'yelp_reviews': [],
        'other_reviews': [],
        'platforms_searched': REVIEW_PLATFORMS,
    }
    reviews_file.write_text(json.dumps(reviews_data, indent=2) + '\n')
    print(f"Created {reviews_file}")

    # Property listings template
    listings_file = ONLINE_DIR / 'property_listings.json'
    listings_data = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Properties advertised for management',
        },
        'listings': [],
        'sources': [
            'Company website',
            'Property management directories',
            'Real estate websites',
        ],
    }
    listings_file.write_text(json.dumps(listings_data, indent=2) + '\n')
    print(f"Created {listings_file}")

    return social_file


def print_search_instructions():
    """Print search instructions."""
    print("=== Social Media and Online Presence Search Instructions ===\n")

    print("Company Websites:")
    print("  - Search for Kettler Management website")
    print("  - Document service descriptions")
    print("  - Note geographic scope statements")
    print()

    print("LinkedIn:")
    print("  - Company LinkedIn page")
    print("  - Key employee profiles")
    print("  - Role descriptions")
    print()

    print("Social Media Platforms:")
    for platform in SOCIAL_MEDIA_PLATFORMS:
        print(f"  {platform['platform']}: {platform['url']}")
    print()

    print("Review Platforms:")
    for platform in REVIEW_PLATFORMS:
        print(f"  {platform['platform']}: {platform['url']}")
    print()


if __name__ == '__main__':
    create_social_media_template()
    print_search_instructions()
