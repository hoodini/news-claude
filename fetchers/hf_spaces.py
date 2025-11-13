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
            from datetime import timedelta

            if not self.hf_api:
                self.hf_api = HfApi()

            # Fetch more spaces and filter by recency
            # Try to get recently modified spaces first
            spaces = self.hf_api.list_spaces(
                sort="lastModified",
                direction=-1,
                limit=limit * 3,  # Fetch more to filter
                full=True
            )

            result = []
            cutoff_date = datetime.now() - timedelta(days=60)  # Last 60 days

            for space in spaces:
                try:
                    space_data = self._parse_space(space)
                    if space_data:
                        # Check if space is recent enough
                        if hasattr(space, 'lastModified') and space.lastModified:
                            last_modified = space.lastModified
                            if hasattr(last_modified, 'replace'):
                                # It's a datetime, compare
                                if last_modified.replace(tzinfo=None) >= cutoff_date:
                                    result.append(space_data)
                            else:
                                result.append(space_data)
                        elif hasattr(space, 'created_at') and space.created_at:
                            created = space.created_at
                            if hasattr(created, 'replace'):
                                if created.replace(tzinfo=None) >= cutoff_date:
                                    result.append(space_data)
                            else:
                                result.append(space_data)
                        else:
                            # No date info, include it
                            result.append(space_data)

                    if len(result) >= limit:
                        break
                except Exception as e:
                    continue

            return result[:limit]

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

            # Last modified date
            last_modified = None
            if hasattr(space, 'lastModified'):
                if space.lastModified:
                    last_modified = space.lastModified.strftime('%Y-%m-%d') if hasattr(space.lastModified, 'strftime') else str(space.lastModified)

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
                'last_modified': last_modified,
                'fetched_at': datetime.now().isoformat()
            }

        except Exception as e:
            return None
