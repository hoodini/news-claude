"""
GitHub Explore Collections fetcher
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict


class GitHubCollectionsFetcher:
    """Fetches curated collections from GitHub Explore"""

    BASE_URL = "https://github.com/collections"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch(self, limit: int = 10) -> List[Dict]:
        """
        Fetch top curated collections from GitHub

        Args:
            limit: Maximum number of collections to fetch

        Returns:
            List of collection dictionaries
        """
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            collections = []

            # Find collection links
            collection_links = soup.find_all('a', href=lambda x: x and x.startswith('/collections/'))

            seen_urls = set()
            for link in collection_links:
                if len(collections) >= limit:
                    break

                try:
                    collection_url = link.get('href', '')
                    if collection_url in seen_urls or not collection_url:
                        continue

                    full_url = f"https://github.com{collection_url}"
                    seen_urls.add(collection_url)

                    # Get collection name from URL
                    collection_name = collection_url.replace('/collections/', '').strip('/')

                    # Try to find description
                    description = ""
                    parent = link.parent
                    if parent:
                        desc_elem = parent.find('p')
                        if desc_elem:
                            description = desc_elem.get_text(strip=True)

                    # Get title
                    title = link.get_text(strip=True)
                    if not title:
                        title = collection_name.replace('-', ' ').title()

                    collections.append({
                        'source': 'github',
                        'type': 'collection',
                        'name': collection_name,
                        'title': title,
                        'url': full_url,
                        'description': description,
                        'fetched_at': datetime.now().isoformat()
                    })

                except Exception as e:
                    continue

            return collections

        except Exception as e:
            print(f"⚠️ Error fetching GitHub collections: {e}")
            return []
