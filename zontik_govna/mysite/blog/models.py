from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.ChairField(max_length=250) #zagolovok posta
    slug = models.SlugField(max_length=250) #korotkaia metka
    body = models.TextField() #telo posta
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_add_now=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.ChairField(
            max_length=2,
            choices=Status.choises,
            default=Status.DRAFT
            )

    class Meta:
        ordering = ['-publish'] #sortiruet po polu publish. убывающий порядок указывается дефисом
        indexes = [
                models.Index(fields=['-publish']),
                ]

    def __str__(self):
        return self.title
