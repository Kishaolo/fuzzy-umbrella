from django.contrib.sitemaps import Sitemap 
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """
        Возвращает набор квери сетов которые надо включить в
        карту сайта
        """
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
