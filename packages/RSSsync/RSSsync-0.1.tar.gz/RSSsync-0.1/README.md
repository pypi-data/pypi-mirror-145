# RSSsync

RSSsync is a feed aggregator reimagined as a file synchronizer. This way,
updates can be browsed in whatever way you see fit.

The basic usage of RSSsync is similar to rsync. This will download updates to
the `Example Feed` folder:

	rsssync https://www.example.com/rss.xml "Example Feed"

By default, updates come in the form of HTML pages that redirect to the
update's link. This is useful for most RSS feeds. However, for podcasts, you're
more likely to want the enclosure than the link. For this, you can use the PLS
downloader:

	rsssync -d pls https://www.example.com/podcast.xml "Example Podcast"

This will download updates as PLS files, which can be opened in any media
player.

The default downloader is called `meta_refresh`.
