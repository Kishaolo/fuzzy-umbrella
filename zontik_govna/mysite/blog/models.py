from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    """kastomnii manager"""
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250) #zagolovok posta
    slug = models.SlugField(max_length=250, 
                            unique_for_date='publish') #korotkaia metka
    author = models.ForeignKey(
            User, 
            on_delete=models.CASCADE, 
            related_name='blog_posts'
            ) #dobavili svaz Many-To-One
    body = models.TextField() #telo posta
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
            max_length=2,
            choices=Status.choices,
            default=Status.DRAFT
            )

    objects = models.Manager() #manager po umolchaniu
    published = PublishedManager() #konkretno prikaldnoi manager
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish'] #sortiruet po polu publish. убывающий порядок указывается дефисом
        indexes = [
                models.Index(fields=['-publish']),
                ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
                'blog:post_detail', 
                args=[self.publish.year, 
                      self.publish.month, 
                      self.publish.day, 
                      self.slug]
                )

class Comment(models.Model):
    post = models.ForeignKey(Post, 
                      on_delete=models.CASCADE, 
                      related_name="comments") #svaz one-to-many nyshna dla privazke k opredelennomy posty
    #related_name nyshna dla imeni atribyta dla obratnoi svazi
    
    name = models.CharField(max_length=80) #ima chela kotorii ostavil coment
    email = models.EmailField() #email (xz zachem)
    body = models.TextField() #telo comenta
    created = models.DateTimeField(auto_now_add=True) #toshe avtosave
    updated = models.DateTimeField(auto_now=True) #avto save dati 
    active = models.BooleanField(default=True) #dla udalenia ploxix komentov

    class Meta:
        ordering = ['created'] #sortirovka po  attr created
        indexes = [models.Index(fields=['created'])] # indeksatsia v vozrastaushem poradke

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
