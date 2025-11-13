"""
Configuration settings for Gen AI News Aggregator
"""

# GitHub Configuration
GITHUB_LANGUAGES = ["python", "jupyter-notebook", "typescript", "javascript"]
GITHUB_TOPICS = ["machine-learning", "deep-learning", "llm", "generative-ai", "transformers"]

# Scoring Weights
GITHUB_STARS_WEIGHT = 0.4
GITHUB_RECENCY_WEIGHT = 0.3
GITHUB_VELOCITY_WEIGHT = 0.3

PAPER_UPVOTE_WEIGHT = 0.6
PAPER_RECENCY_WEIGHT = 0.4

SPACE_LIKES_WEIGHT = 0.5
SPACE_RECENCY_WEIGHT = 0.5

# Limits
HF_SPACES_LIMIT = 20
HF_PAPERS_LIMIT = 20
GITHUB_COLLECTIONS_LIMIT = 10
DEFAULT_DIGEST_LIMIT = 50

# Directories
OUTPUT_DIR = "output"
TEMPLATE_DIR = "templates"

# Creator Information
CREATOR = {
    "name": "Yuval Avidani",
    "title": "AI Builder & Speaker",
    "website": "https://yuv.ai",
    "brand": "YUV.AI Developers AI Trends",
    "social": {
        "linktree": "https://linktr.ee/yuvai",
        "instagram": "@yuval_770",
        "twitter": "@yuvalav",
        "github": "@hoodini",
        "youtube": "@yuv-ai",
        "tiktok": "@yuval.ai"
    }
}
