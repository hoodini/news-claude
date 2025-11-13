"""
Hugging Face Papers fetcher
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict


class HFPapersFetcher:
    """Fetches trending papers from Hugging Face"""

    BASE_URL = "https://huggingface.co/papers"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch(self, limit: int = 20) -> List[Dict]:
        """
        Fetch trending papers from Hugging Face

        Args:
            limit: Maximum number of papers to fetch

        Returns:
            List of paper dictionaries
        """
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            papers = []

            # Find all paper articles
            # HF uses article or div elements with specific classes
            paper_elements = soup.find_all(['article', 'div'], limit=limit * 2)  # Get extra in case some fail

            for elem in paper_elements:
                if len(papers) >= limit:
                    break

                try:
                    paper = self._parse_paper(elem)
                    if paper:
                        papers.append(paper)
                except Exception as e:
                    continue

            return papers[:limit]

        except Exception as e:
            print(f"⚠️ Error fetching HF papers: {e}")
            return []

    def _parse_paper(self, elem) -> Dict | None:
        """Parse a paper element"""
        try:
            # Find the link to the paper
            link = elem.find('a', href=re.compile(r'/papers/'))
            if not link:
                return None

            paper_url = link.get('href', '')
            if not paper_url.startswith('http'):
                paper_url = f"https://huggingface.co{paper_url}"

            # Extract arXiv ID from URL
            arxiv_match = re.search(r'(\d+\.\d+)', paper_url)
            arxiv_id = arxiv_match.group(1) if arxiv_match else ""

            # Title
            title_elem = elem.find(['h3', 'h4', 'h2'])
            if not title_elem:
                # Try to find it in the link
                title_elem = link
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"

            # Authors
            authors = []
            # Look for author links or author text
            author_elems = elem.find_all('a', href=re.compile(r'/(?:papers|users)/'))
            for author_elem in author_elems:
                author_text = author_elem.get_text(strip=True)
                if author_text and author_text not in ['', title]:
                    authors.append(author_text)

            # If no authors found, look for text containing "by"
            if not authors:
                text = elem.get_text()
                if ' by ' in text.lower():
                    author_text = text.split(' by ')[-1].split('\n')[0].strip()
                    if author_text:
                        authors = [author_text]

            # Upvotes
            upvotes = 0
            upvote_text = elem.get_text()
            # Look for numbers followed by upvote-related text
            upvote_match = re.search(r'(\d+)\s*(?:upvote|like|👍)', upvote_text, re.IGNORECASE)
            if upvote_match:
                upvotes = int(upvote_match.group(1))
            else:
                # Try to find number elements
                for text_elem in elem.find_all(string=True):
                    text = text_elem.strip()
                    if text.isdigit() and int(text) < 10000:  # Reasonable upvote range
                        upvotes = int(text)
                        break

            # Publication date from arXiv ID
            pub_date = None
            if arxiv_id:
                pub_date = self._parse_arxiv_date(arxiv_id)

            # If no date, try to find time element
            if not pub_date:
                time_elem = elem.find('time')
                if time_elem:
                    datetime_attr = time_elem.get('datetime', '')
                    if datetime_attr:
                        pub_date = datetime_attr

            return {
                'source': 'huggingface',
                'type': 'paper',
                'title': title,
                'authors': authors,
                'url': paper_url,
                'upvotes': upvotes,
                'arxiv_id': arxiv_id,
                'publication_date': pub_date,
                'fetched_at': datetime.now().isoformat()
            }

        except Exception as e:
            return None

    def _parse_arxiv_date(self, arxiv_id: str) -> str | None:
        """
        Parse publication date from arXiv ID
        Format: YYMM.NNNNN (e.g., 2311.12345 → Nov 2023)
        """
        try:
            match = re.match(r'(\d{2})(\d{2})', arxiv_id)
            if match:
                year_short = int(match.group(1))
                month = int(match.group(2))

                # Determine century (arXiv started in 1991)
                if year_short >= 91:
                    year = 1900 + year_short
                else:
                    year = 2000 + year_short

                # Create date string
                return f"{year}-{month:02d}-01"

        except Exception:
            pass

        return None
