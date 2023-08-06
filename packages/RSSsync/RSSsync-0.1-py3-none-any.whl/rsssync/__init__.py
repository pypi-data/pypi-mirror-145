"""
TODO:
- Downloaders from .config/rsssync/config.py
- Add metadata to entries via xattrs
- Allow renaming subfolder
- Get RSS feed URLs from YouTube channels, etc.
- Only download entries that match query
- Stay open and update feeds periodically
- Man page
- Sphinx docs
- List downloaders in help text
- Option to simply print out feed metadata
- Set default downloader based on URL in config.py
- Import/export OPML
- Start date option
- Notifications for new updates
- Human-readable cache
- Make cache depend on files
- Multiple downloaders based on eg whether an update has an enclosure
- Handle redirects
"""


from .downloader import FeedDownloader, downloaders
from . import meta_refresh_downloader, pls_downloader
