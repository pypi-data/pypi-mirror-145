from .downloader import FeedDownloader, downloaders


class MetaRefreshDownloader(FeedDownloader):
    """Downloads updates as HTML files that redirect to the update's link"""

    def download_entry(self, entry):
        filename = FeedDownloader.fix_filename(entry.title)
        path = self.dest.joinpath(filename + '.html')

        with path.open('w') as f:
            contents = \
                '<html><head>' \
                '<meta http-equiv="refresh" content="0; url={}"/>' \
                '</head></html>'

            f.write(contents.format(entry.link))

        self.attach_metadata(path, entry)


downloaders['meta_refresh'] = MetaRefreshDownloader
