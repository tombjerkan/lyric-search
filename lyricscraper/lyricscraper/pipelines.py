from scrapy.exceptions import DropItem


class LyricsPipeline:
    def process_item(self, item, spider):
        if 'lyrics' not in item:
            raise DropItem('Missing lyrics for {}'.format(item))
        else:
            return item
