"""
GitHub Trending repository fetcher
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional


class GitHubTrendingFetcher:
    """Fetches trending repositories from GitHub"""

    BASE_URL = "https://github.com/trending"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch(self, languages: List[str] = None, time_range: str = 'daily') -> List[Dict]:
        """
        Fetch trending repositories

        Args:
            languages: List of programming languages to filter by
            time_range: 'daily', 'weekly', or 'monthly'

        Returns:
            List of repository dictionaries
        """
        all_repos = []
        seen_urls = set()

        # Fetch overall trending
        repos = self._fetch_trending_page(None, time_range)
        for repo in repos:
            if repo['url'] not in seen_urls:
                all_repos.append(repo)
                seen_urls.add(repo['url'])

        # Fetch language-specific trending
        if languages:
            for lang in languages:
                repos = self._fetch_trending_page(lang, time_range)
                for repo in repos:
                    if repo['url'] not in seen_urls:
                        all_repos.append(repo)
                        seen_urls.add(repo['url'])

        return all_repos

    def _fetch_trending_page(self, language: Optional[str], time_range: str) -> List[Dict]:
        """Fetch a single trending page"""
        try:
            # Build URL
            if language:
                url = f"{self.BASE_URL}/{language}"
            else:
                url = self.BASE_URL

            params = {'since': time_range}

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            repos = []

            # Find all repository articles
            articles = soup.find_all('article', class_='Box-row')

            for article in articles:
                try:
                    repo = self._parse_repository(article)
                    if repo:
                        repos.append(repo)
                except Exception as e:
                    print(f"Error parsing repository: {e}")
                    continue

            return repos

        except Exception as e:
            print(f"⚠️ Error fetching GitHub trending: {e}")
            return []

    def _parse_repository(self, article) -> Optional[Dict]:
        """Parse a repository article element"""
        try:
            # Repository name and URL
            h2 = article.find('h2', class_='h3')
            if not h2:
                return None

            link = h2.find('a')
            if not link:
                return None

            repo_path = link.get('href', '').strip('/')
            repo_url = f"https://github.com/{repo_path}"

            # Description
            desc_elem = article.find('p', class_='col-9')
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            # Stars
            stars_elem = article.find('svg', {'aria-label': 'star'})
            stars = 0
            if stars_elem:
                parent = stars_elem.parent
                stars_text = parent.get_text(strip=True)
                stars = self._parse_number(stars_text)

            # Stars today (velocity)
            stars_today = 0
            span_today = article.find('span', class_='d-inline-block float-sm-right')
            if span_today:
                stars_today_text = span_today.get_text(strip=True)
                stars_today = self._parse_number(stars_today_text)

            # Forks
            forks = 0
            fork_elem = article.find('svg', {'aria-label': 'fork'})
            if fork_elem:
                parent = fork_elem.parent
                forks_text = parent.get_text(strip=True)
                forks = self._parse_number(forks_text)

            # Language
            language = ""
            lang_elem = article.find('span', {'itemprop': 'programmingLanguage'})
            if lang_elem:
                language = lang_elem.get_text(strip=True)

            # Topics/tags
            topics = []
            topic_tags = article.find_all('a', class_='topic-tag')
            for tag in topic_tags:
                topic = tag.get_text(strip=True)
                if topic:
                    topics.append(topic)

            # Contributors count
            contributors = 0
            built_by = article.find('span', string=lambda x: x and 'Built by' in x)
            if built_by:
                # Count avatar images
                avatars = article.find_all('img', class_='avatar')
                contributors = len(avatars)

            return {
                'source': 'github',
                'type': 'repository',
                'name': repo_path,
                'url': repo_url,
                'description': description,
                'stars': stars,
                'stars_today': stars_today,
                'forks': forks,
                'language': language,
                'topics': topics,
                'contributors': contributors,
                'fetched_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error parsing repository element: {e}")
            return None

    def _parse_number(self, text: str) -> int:
        """Parse a number from text like '1,234' or '1.2k'"""
        try:
            # Remove commas
            text = text.replace(',', '')

            # Handle k/m suffixes
            if 'k' in text.lower():
                return int(float(text.lower().replace('k', '')) * 1000)
            elif 'm' in text.lower():
                return int(float(text.lower().replace('m', '')) * 1000000)
            else:
                # Extract just the number
                import re
                match = re.search(r'(\d+)', text)
                if match:
                    return int(match.group(1))
            return 0
        except:
            return 0
