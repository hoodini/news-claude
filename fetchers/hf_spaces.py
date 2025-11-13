"""
Hugging Face Spaces fetcher
"""

from datetime import datetime
from typing import List, Dict


class HFSpacesFetcher:
    """Fetches trending spaces from Hugging Face"""

    def __init__(self):
        self.hf_api = None

    def fetch(self, limit: int = 20) -> List[Dict]:
        """
        Fetch trending spaces from Hugging Face

        Args:
            limit: Maximum number of spaces to fetch

        Returns:
            List of space dictionaries
        """
        try:
            # Import here to make it optional
            from huggingface_hub import HfApi

            if not self.hf_api:
                self.hf_api = HfApi()

            # List spaces sorted by likes
            spaces = self.hf_api.list_spaces(
                sort="likes",
                direction=-1,
                limit=limit,
                full=True
            )

            result = []
            for space in spaces:
                try:
                    space_data = self._parse_space(space)
                    if space_data:
                        result.append(space_data)
                except Exception as e:
                    continue

            return result

        except ImportError:
            print("⚠️ huggingface_hub not installed. Skipping spaces.")
            return []
        except Exception as e:
            print(f"⚠️ Error fetching HF spaces: {e}")
            return []

    def _parse_space(self, space) -> Dict | None:
        """Parse a space object from HF API"""
        try:
            space_id = space.id if hasattr(space, 'id') else str(space)
            author = space.author if hasattr(space, 'author') else space_id.split('/')[0]

            # Build space URL
            space_url = f"https://huggingface.co/spaces/{space_id}"

            # Get card data for description
            description = ""
            if hasattr(space, 'card_data') and space.card_data:
                if isinstance(space.card_data, dict):
                    description = space.card_data.get('description', '')
                    if not description:
                        description = space.card_data.get('title', '')

            # Fallback to checking other attributes
            if not description and hasattr(space, 'description'):
                description = space.description or ""

            # Likes
            likes = 0
            if hasattr(space, 'likes'):
                likes = space.likes or 0

            # SDK
            sdk = "unknown"
            if hasattr(space, 'sdk'):
                sdk = space.sdk or "unknown"

            # Creation date
            created_at = None
            if hasattr(space, 'created_at'):
                if space.created_at:
                    created_at = space.created_at.strftime('%Y-%m-%d') if hasattr(space.created_at, 'strftime') else str(space.created_at)

            return {
                'source': 'huggingface',
                'type': 'space',
                'space_id': space_id,
                'author': author,
                'url': space_url,
                'description': description,
                'likes': likes,
                'sdk': sdk,
                'created_at': created_at,
                'fetched_at': datetime.now().isoformat()
            }

        except Exception as e:
            return None
