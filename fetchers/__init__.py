"""
Data fetchers for various AI/ML sources
"""

from .github_trending import GitHubTrendingFetcher
from .hf_papers import HFPapersFetcher
from .hf_spaces import HFSpacesFetcher
from .github_collections import GitHubCollectionsFetcher

__all__ = [
    'GitHubTrendingFetcher',
    'HFPapersFetcher',
    'HFSpacesFetcher',
    'GitHubCollectionsFetcher'
]
