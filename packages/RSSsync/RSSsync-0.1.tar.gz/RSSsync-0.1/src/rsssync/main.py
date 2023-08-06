import logging

from argparse import ArgumentParser
from pathlib import Path

import feedparser
import toml

from .downloader import downloaders


def main():
    """Downloads RSS updates based on command line arguments."""

    # Parse args
    parser = ArgumentParser(description="Download RSS updates")

    parser.add_argument('-n', '--num-entries', type=int, default=0,
        metavar='N', help="Download last N updates")
    parser.add_argument('-s', '--subfolders', action='store_true',
        help="Store each feed's updates in its own subfolder")
    parser.add_argument('-d', '--downloader', type=str, default='meta_refresh',
        help="Download handler")
    parser.add_argument('-m', '--mkpath', action='store_true',
        help="Create destination path, if it doesn't exist")
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help="Print messages to console")
    parser.add_argument('-r', '--redownload', action='store_true',
        help="Ignore cache and redownload all entries")
    parser.add_argument('srcs', nargs='+', metavar='src',
        help="URL of an RSS or Atom feed")
    parser.add_argument('dest', type=Path,
        help="Directory feeds are downloaded to")

    args = parser.parse_args()

    # Setup logger
    logging.basicConfig(
        level = logging.WARNING - 10 * args.verbose,
        format = "%(message)s")

    # Mkpath option
    if args.mkpath:
        args.dest.mkdir(parents=True, exist_ok=True)

    # Open/create cache
    cache_path = args.dest.joinpath('.cache').with_suffix('.toml')

    if cache_path.exists() and not args.redownload:
        cache = toml.load(cache_path)
    else:
        cache = {}

    # Set user-agent string
    feedparser.USER_AGENT = "RSSsync/0.1"

    # Download feeds
    for src in args.srcs:
        cache.setdefault(src, {})
        downloader = downloaders[args.downloader](src, args.dest, cache[src])

        if args.verbose:
            logging.info(f"Updating {src}...")

        downloader.download_feed()

        if downloader.is_feed_modified:
            if args.subfolders:
                downloader.create_subfolder()

            downloader.download_entries(args.num_entries)
            logging.info("Done.")
        else:
            logging.info("Feed is up to date.")

    # Save cache
    with cache_path.open('w') as f:
        toml.dump(cache, f)
