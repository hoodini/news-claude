#!/usr/bin/env python3
"""
Gen AI News Aggregator
A stunning news aggregator for AI/ML content

Author: Yuval Avidani
Website: https://yuv.ai
"""

import argparse
import os
import sys
import webbrowser
from datetime import datetime

import config
from fetchers import (
    GitHubTrendingFetcher,
    HFPapersFetcher,
    HFSpacesFetcher,
    GitHubCollectionsFetcher
)
from ranking import NewsRanker


def format_number(num):
    """Format numbers for display (e.g., 1234 -> 1,234)"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}k"
    return str(num)


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Generate a stunning AI/ML news digest',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --range daily --open
  %(prog)s --range weekly --limit 30
  %(prog)s --days 14 --output custom.html
  %(prog)s --range monthly

Created by Yuval Avidani • https://yuv.ai
        """
    )

    parser.add_argument(
        '--range',
        choices=['daily', 'weekly', 'monthly'],
        default='daily',
        help='Time range for trending items (default: daily)'
    )

    parser.add_argument(
        '--days',
        type=int,
        help='Custom number of days (overrides --range)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=config.DEFAULT_DIGEST_LIMIT,
        help=f'Maximum items in digest (default: {config.DEFAULT_DIGEST_LIMIT})'
    )

    parser.add_argument(
        '--open',
        action='store_true',
        help='Auto-open generated file in browser'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Custom output filename (default: digest_<range>_<timestamp>.html)'
    )

    return parser.parse_args()


def fetch_all_data(time_range='daily'):
    """
    Fetch data from all sources

    Args:
        time_range: Time range for GitHub trending

    Returns:
        List of all items
    """
    all_items = []

    # GitHub Trending
    print("🔥 Fetching GitHub trending repositories...")
    github_fetcher = GitHubTrendingFetcher()
    github_repos = github_fetcher.fetch(
        languages=config.GITHUB_LANGUAGES,
        time_range=time_range
    )
    print(f"   Found {len(github_repos)} repositories")
    all_items.extend(github_repos)

    # GitHub Collections
    print("📚 Fetching GitHub curated collections...")
    collections_fetcher = GitHubCollectionsFetcher()
    collections = collections_fetcher.fetch(limit=config.GITHUB_COLLECTIONS_LIMIT)
    print(f"   Found {len(collections)} collections")
    all_items.extend(collections)

    # Hugging Face Papers
    print("📄 Fetching Hugging Face papers...")
    papers_fetcher = HFPapersFetcher()
    papers = papers_fetcher.fetch(limit=config.HF_PAPERS_LIMIT)
    print(f"   Found {len(papers)} papers")
    all_items.extend(papers)

    # Hugging Face Spaces
    print("🚀 Fetching Hugging Face spaces...")
    spaces_fetcher = HFSpacesFetcher()
    spaces = spaces_fetcher.fetch(limit=config.HF_SPACES_LIMIT)
    print(f"   Found {len(spaces)} spaces")
    all_items.extend(spaces)

    return all_items


def generate_html(items, output_path, time_range='daily'):
    """
    Generate HTML from template

    Args:
        items: Grouped items dictionary
        output_path: Path to output file
        time_range: Time range string for display
    """
    from jinja2 import Environment, FileSystemLoader

    # Set up Jinja2 environment with custom filters
    env = Environment(loader=FileSystemLoader(config.TEMPLATE_DIR))
    env.filters['format_number'] = format_number

    # Load template
    template = env.get_template('digest.html')

    # Prepare context
    context = {
        'brand': config.CREATOR['brand'],
        'creator_name': config.CREATOR['name'],
        'creator_title': config.CREATOR['title'],
        'creator_website': config.CREATOR['website'],
        'date': datetime.now().strftime('%B %d, %Y'),
        'time_range': time_range.title() + ' Update',
        'github_repos': items['github_repos'],
        'papers': items['papers'],
        'spaces': items['spaces'],
        'collections': items['github_collections'],
        'total_items': sum(len(v) for v in items.values()),
        'github_count': len(items['github_repos']) + len(items['github_collections']),
        'papers_count': len(items['papers']),
        'spaces_count': len(items['spaces']),
        'generated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p')
    }

    # Render template
    html = template.render(**context)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    """Main entry point"""
    args = parse_args()

    # Print header
    print("\n" + "=" * 60)
    print("🤖 Gen AI News Aggregator")
    print("   Created by Yuval Avidani • https://yuv.ai")
    print("=" * 60 + "\n")

    # Determine time range
    if args.days:
        time_range = 'daily'  # Use daily for GitHub, filter by days later
        days = args.days
        range_text = f"{days} days"
    else:
        time_range = args.range
        range_map = {'daily': 1, 'weekly': 7, 'monthly': 30}
        days = range_map[time_range]
        range_text = time_range

    print(f"Time range: {range_text}")
    print(f"Item limit: {args.limit}\n")

    # Fetch all data
    print("Fetching data from sources...\n")
    all_items = fetch_all_data(time_range)
    print(f"\n✅ Total items fetched: {len(all_items)}\n")

    # Rank and filter items
    print("Ranking and filtering items...")
    ranker = NewsRanker()

    # Apply time filter if needed
    if days:
        all_items = ranker.filter_by_time_range(all_items, days)

    # Rank all items
    ranked_items = ranker.rank_items(all_items, limit=args.limit)

    # Group by source
    grouped_items = ranker.group_by_source(ranked_items)

    print(f"✅ Ranked {len(ranked_items)} items\n")

    # Generate output filename
    if args.output:
        output_filename = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"digest_{time_range}_{timestamp}.html"

    # Ensure output directory exists
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(config.OUTPUT_DIR, output_filename)

    # Generate HTML
    print("Generating HTML digest...")
    generate_html(grouped_items, output_path, range_text)
    print(f"✅ Generated: {output_path}\n")

    # Open in browser if requested
    if args.open:
        print("Opening in browser...")
        webbrowser.open(f'file://{os.path.abspath(output_path)}')

    # Success message
    print("=" * 60)
    print("✨ Success! Your stunning AI news digest is ready!")
    print(f"📄 File: {output_path}")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
