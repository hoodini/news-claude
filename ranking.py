"""
Smart ranking algorithm for AI news items
"""

import math
from datetime import datetime, timedelta
from typing import List, Dict
import config


class NewsRanker:
    """Ranks news items using a sophisticated scoring algorithm"""

    def __init__(self):
        self.weights = {
            'github_stars': config.GITHUB_STARS_WEIGHT,
            'github_recency': config.GITHUB_RECENCY_WEIGHT,
            'github_velocity': config.GITHUB_VELOCITY_WEIGHT,
            'paper_upvote': config.PAPER_UPVOTE_WEIGHT,
            'paper_recency': config.PAPER_RECENCY_WEIGHT,
            'space_likes': config.SPACE_LIKES_WEIGHT,
            'space_recency': config.SPACE_RECENCY_WEIGHT,
        }

    def rank_items(self, items: List[Dict], limit: int = None) -> List[Dict]:
        """
        Rank all items by calculated score

        Args:
            items: List of items from various sources
            limit: Maximum number of items to return

        Returns:
            Sorted list of items with scores
        """
        # Calculate score for each item
        for item in items:
            item['score'] = self.calculate_score(item)

        # Sort by score descending
        sorted_items = sorted(items, key=lambda x: x['score'], reverse=True)

        # Apply limit if specified
        if limit:
            sorted_items = sorted_items[:limit]

        return sorted_items

    def calculate_score(self, item: Dict) -> float:
        """
        Calculate a 0-100 score for an item based on its type

        Args:
            item: Item dictionary

        Returns:
            Score between 0 and 100
        """
        item_type = item.get('type', '')
        source = item.get('source', '')

        if source == 'github' and item_type == 'repository':
            return self._score_github_repo(item)
        elif source == 'github' and item_type == 'collection':
            return self._score_collection(item)
        elif source == 'huggingface' and item_type == 'paper':
            return self._score_paper(item)
        elif source == 'huggingface' and item_type == 'space':
            return self._score_space(item)
        else:
            return 0.0

    def _score_github_repo(self, repo: Dict) -> float:
        """Score a GitHub repository - heavily favor velocity"""
        stars = repo.get('stars', 0)
        stars_today = repo.get('stars_today', 0)

        # Velocity is KING - this is what makes it trending!
        # Score heavily based on stars gained today
        if stars_today > 0:
            # Exponential scoring for velocity
            velocity_score = min(70, stars_today * 5)
        else:
            velocity_score = 0

        # Stars score: much lower weight, log scale
        # Only matters if velocity is present
        stars_score = min(20, math.log10(stars + 1) * 3)

        # Recency bonus for trending items
        recency_score = 10

        # Weighted combination - velocity dominates
        total_score = (
            velocity_score * 0.7 +  # Velocity is 70% of score
            stars_score * 0.2 +      # Total stars is 20%
            recency_score * 0.1      # Recency is 10%
        )

        return min(100, total_score)

    def _score_paper(self, paper: Dict) -> float:
        """Score a research paper - upvotes show recent popularity"""
        upvotes = paper.get('upvotes', 0)

        # Upvote score: higher multiplier for popular papers
        upvote_score = min(70, upvotes * 5)

        # Recency score: all papers on HF are recent
        recency_score = 30

        # Weighted combination
        total_score = (
            upvote_score * 0.7 +
            recency_score * 0.3
        )

        return min(100, total_score)

    def _score_space(self, space: Dict) -> float:
        """Score a Hugging Face space - recently modified matters"""
        likes = space.get('likes', 0)

        # Check if recently modified (we filtered for this)
        last_modified = space.get('last_modified')

        # Likes score: log scale
        likes_score = min(50, math.log10(likes + 1) * 12)

        # Recency bonus: spaces in our list are already recent
        recency_score = 40

        # Weighted combination
        total_score = (
            likes_score * 0.5 +
            recency_score * 0.5
        )

        return min(100, total_score)

    def _score_collection(self, collection: Dict) -> float:
        """Score a curated collection (fixed high score)"""
        return 70.0  # Curated content gets consistent good score

    def filter_by_time_range(self, items: List[Dict], days: int) -> List[Dict]:
        """
        Filter items by time range

        Args:
            items: List of items
            days: Number of days to look back

        Returns:
            Filtered list of items
        """
        cutoff = datetime.now() - timedelta(days=days)
        filtered = []

        for item in items:
            # Check fetched_at timestamp (all items should have this)
            fetched_at = item.get('fetched_at')
            if fetched_at:
                try:
                    fetched_date = datetime.fromisoformat(fetched_at.replace('Z', '+00:00'))
                    if fetched_date >= cutoff:
                        filtered.append(item)
                except:
                    # If parsing fails, include the item
                    filtered.append(item)
            else:
                # No timestamp, include by default
                filtered.append(item)

        return filtered

    def group_by_source(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group items by source type

        Args:
            items: List of items

        Returns:
            Dictionary with source types as keys
        """
        groups = {
            'github_repos': [],
            'github_collections': [],
            'papers': [],
            'spaces': []
        }

        for item in items:
            source = item.get('source', '')
            item_type = item.get('type', '')

            if source == 'github' and item_type == 'repository':
                groups['github_repos'].append(item)
            elif source == 'github' and item_type == 'collection':
                groups['github_collections'].append(item)
            elif source == 'huggingface' and item_type == 'paper':
                groups['papers'].append(item)
            elif source == 'huggingface' and item_type == 'space':
                groups['spaces'].append(item)

        return groups
