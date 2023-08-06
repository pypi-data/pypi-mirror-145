from .downloader import FeedDownloader, downloaders


class PlsDownloader(FeedDownloader):
    """Downloads podcast episodes as individual PLS files"""

    def download_entry(self, entry):
        if 'enclosures' in entry and len(entry.enclosures) > 0:
            filename = FeedDownloader.fix_filename(entry.title)
            path = self.dest.joinpath(filename + '.pls')

            with path.open('w') as f:
                contents = \
                    '[playlist]\n' \
                    'File1={}\n' \
                    'NumberOfEntries=1'

                f.write(contents.format(entry.enclosures[0].href))

            self.attach_metadata(path, entry)


downloaders['pls'] = PlsDownloader
