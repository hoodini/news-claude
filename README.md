# 🤖 Gen AI News Aggregator

A stunning, Apple-inspired news aggregator that creates beautiful HTML digests of trending AI/ML content from GitHub, Hugging Face Papers, and Hugging Face Spaces.

**Created by [Yuval Avidani](https://yuv.ai)** - AI Builder & Speaker

---

## ✨ Features

- **Beautiful Design**: Apple Newsroom-inspired layout with smooth animations and premium feel
- **Multi-Source Aggregation**: Combines GitHub Trending, HF Papers, HF Spaces, and GitHub Collections
- **Smart Ranking**: Sophisticated scoring algorithm that ranks items by relevance and popularity
- **Responsive**: Mobile-first design that looks stunning on all devices
- **Zero Dependencies in Output**: Self-contained HTML files that work anywhere
- **Customizable**: Flexible CLI options for time ranges, limits, and more

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd news-claude

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Generate daily digest
python main.py

# Generate daily digest and open in browser
python main.py --open

# Generate weekly digest with limit
python main.py --range weekly --limit 30

# Custom time range (14 days)
python main.py --days 14

# Monthly digest with custom output
python main.py --range monthly --output my_digest.html
```

---

## 📋 CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--range` | Time range: `daily`, `weekly`, or `monthly` | `daily` |
| `--days N` | Custom number of days (overrides --range) | - |
| `--limit N` | Maximum items in digest | 50 |
| `--open` | Auto-open generated file in browser | False |
| `--output FILE` | Custom output filename | `digest_<range>_<timestamp>.html` |

---

## 🎨 Design Philosophy

The design is inspired by premium products like:
- **Apple Newsroom**: Clean typography, generous whitespace
- **Medium**: Card-based layout, excellent readability
- **Stripe**: Subtle animations, sophisticated gradients

### Key Design Elements

- **Typography**: Perfect hierarchy using system fonts
- **Colors**: Purple/blue gradients (#667eea to #764ba2)
- **Animations**: Smooth 300ms transitions on all interactions
- **Whitespace**: Breathing room between all elements
- **Shadows**: Subtle depth that elevates on hover
- **Responsiveness**: Adapts beautifully to all screen sizes

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# GitHub languages to track
GITHUB_LANGUAGES = ["python", "jupyter-notebook", "typescript", "javascript"]

# Topics of interest
GITHUB_TOPICS = ["machine-learning", "deep-learning", "llm", "generative-ai"]

# Scoring weights
GITHUB_STARS_WEIGHT = 0.4
GITHUB_VELOCITY_WEIGHT = 0.3
GITHUB_RECENCY_WEIGHT = 0.3

# Limits
HF_SPACES_LIMIT = 20
HF_PAPERS_LIMIT = 20
DEFAULT_DIGEST_LIMIT = 50
```

---

## 📊 How It Works

### 1. Data Collection

**GitHub Trending**
- Scrapes trending repositories
- Supports multiple languages
- Deduplicates across languages
- Extracts: stars, velocity, forks, topics, contributors

**Hugging Face Papers**
- Fetches from HF papers page
- Parses arXiv IDs and dates
- Extracts: title, authors, upvotes

**Hugging Face Spaces**
- Uses official HF Hub API
- Sorted by likes
- Extracts: description, SDK, creation date

**GitHub Collections**
- Scrapes curated collections
- Handpicked by GitHub

### 2. Smart Ranking

Each item gets a 0-100 score based on:

**GitHub Repos:**
- Stars (logarithmic scale)
- Velocity (stars gained today)
- Recency

**Papers:**
- Upvotes
- Publication date

**Spaces:**
- Likes (logarithmic scale)
- Recency

**Collections:**
- Fixed high score (curated content)

### 3. HTML Generation

- Jinja2 templating
- Inline CSS (no external dependencies)
- Self-contained output files
- Mobile-responsive design

---

## 🎯 Project Structure

```
news-claude/
├── main.py                 # CLI entry point
├── config.py              # Configuration settings
├── ranking.py             # Scoring algorithm
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── fetchers/             # Data fetchers
│   ├── __init__.py
│   ├── github_trending.py
│   ├── github_collections.py
│   ├── hf_papers.py
│   └── hf_spaces.py
├── templates/            # HTML templates
│   └── digest.html
└── output/               # Generated HTML files
    └── digest_*.html
```

---

## 🌟 Examples

### Daily AI News Digest
```bash
python main.py --range daily --open
```

Perfect for your morning routine - see what's trending in AI today!

### Weekly Roundup
```bash
python main.py --range weekly --limit 40
```

Great for weekend reading - catch up on the week's best AI content.

### Custom Research Report
```bash
python main.py --days 30 --limit 100 --output research_report.html
```

Deep dive into the last month of AI developments.

---

## 🤝 Contributing

This project was created by Yuval Avidani. Feel free to:
- Open issues for bugs or suggestions
- Submit pull requests for improvements
- Share your generated digests!

---

## 📱 Connect

**Yuval Avidani** - AI Builder & Speaker

- 🌐 Website: [yuv.ai](https://yuv.ai)
- 🔗 Linktree: [linktr.ee/yuvai](https://linktr.ee/yuvai)
- 📸 Instagram: [@yuval_770](https://instagram.com/yuval_770)
- 🐦 Twitter/X: [@yuvalav](https://twitter.com/yuvalav)
- 💻 GitHub: [@hoodini](https://github.com/hoodini)
- 📺 YouTube: [@yuv-ai](https://youtube.com/@yuv-ai)
- 🎵 TikTok: [@yuval.ai](https://tiktok.com/@yuval.ai)

---

## 📄 License

Created by Yuval Avidani • YUV.AI

---

## 💡 Tips

1. **Run daily**: Set up a cron job to generate fresh digests automatically
2. **Share**: The HTML files are beautiful - share them with your team!
3. **Customize**: Edit `config.py` to focus on your specific interests
4. **Archive**: Keep old digests to track AI trends over time
5. **Mobile**: The design is mobile-first - view on any device

---

**Made with ❤️ by Yuval Avidani**

*Bringing you the best of AI/ML, beautifully presented.*
