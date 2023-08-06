import logging
import re

from os import utime
from pathlib import Path
from time import mktime
from urllib.error import URLError

import feedparser


class FeedDownloader():
    """Handles the downloading of a feed.

    Attributes:
        src (str): URL of the feed.
        dest (Path): Path where feed will be downloaded.
        feed (FeedParserDict): The feed, once it's downloaded.
        cache (dict): Info to prevent redownloading feeds/entries.
    """

    def fix_filename(filename):
        """Removes forbidden characters from filename"""

        return re.sub(r'[\\/*?:"<>|]', '', filename)


    def __init__(self, src, dest, cache):
        self.src = src
        self.dest = dest
        self.feed = {}
        self.cache = cache


    @property
    def new_entries(self):
        return [e for e in self.feed.entries if not self.is_cached(e)]


    @property
    def has_response(self):
        return 'status' in self.feed


    @property
    def has_good_response(self):
        return self.feed.get('status') == 200 or self.feed.get('status') == 304


    @property
    def is_feed_modified(self):
        return self.feed.get('status') == 200 and len(self.new_entries) > 0


    def is_cached(self, entry):
        return entry.get('guid') in self.cache.get('entries', {}) \
            or entry.get('title') in self.cache.get('entries', {})


    def download_feed(self):
        """Downloads the RSS/Atom feed itself."""

        try:
            self.feed = feedparser.parse(
                self.src,
                etag=self.cache.get('etag'),
                modified=self.cache.get('modified'))

            if self.has_good_response:
                if 'etag' in self.feed:
                    self.cache['etag'] = self.feed.etag
                if 'modified' in self.feed:
                    self.cache['modified'] = self.feed.modified

            elif self.has_response:
                status = self.feed.status
                logging.error(f"Error {status}: Feed couldn't be downloaded.")

            else:
                logging.error("Error: No response.")

        except URLError:
            logging.error("Error: URL could not be resolved.")


    def create_subfolder(self):
        """Creates subfolder for feed entries."""

        folder_name = FeedDownloader.fix_filename(self.feed.feed.title)
        self.dest = self.dest.joinpath(folder_name)
        self.dest.mkdir(exist_ok=True)


    def download_entries(self, num_entries):
        """Iterates over entries in the feed, calling download_entry on each.

        Probably won't need to be overridden, unless you want to download
        entries in parallel.

        Args:
            num_entries (int): Number of entries to download.
        """
 
        entries = self.feed.entries[:num_entries] \
                if num_entries > 0 else self.feed.entries
        self.cache.setdefault('entries', [])

        for e in self.new_entries:
            self.download_entry(e)
            self.cache['entries'].append(e.get('guid') or e.get('title'))


    def attach_metadata(self, path, entry):
        """Attaches various metadata to the file representing an entry."""

        # Set date modified/accessed to publication date
        pub_time = mktime(entry.published_parsed)
        utime(path, (pub_time, pub_time))


    def download_entry(self, entry):
        """Downloads an individual entry.

        This method must be overridden to actually create any files. Note that
        in many cases, it's perfectly acceptable to simply create a file
        containing a link to the actual entry -- no downloading required.

        Args:
            entry (FeedParserDict): Data on the entry to download.
        """

        raise NotImplementedError()


downloaders = {}
