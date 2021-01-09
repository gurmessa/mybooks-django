from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import unique_slugify

class User(AbstractUser):
    is_admin=models.BooleanField(default=False)

    def __str__(self):
    	return self.first_name +" "+ self.username

class PublishedManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(status='p', **kwargs)

class Author(models.Model):
    full_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="author",blank=True,null=True)
    def __str__(self):
        return self.full_name

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS = (
        ('p', 'published'),
        ('d', 'draft'),
    )
    LANGUAGE = (
        ('o', 'Afaan Oromoo'),
        ('e', 'English'),
        ('a', 'Amharic'),
    )
    FORMAT = (
            ('p', 'PDF'),
            ('e', 'epub'),
    )
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="photos",blank=True)
    file = models.FileField(upload_to="files")
    description = models.TextField(blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250,unique=True)
    status = models.CharField(max_length=1, choices=STATUS)
    langauge = models.CharField(max_length=1, choices=LANGUAGE)
    pages = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publisher = models.CharField(max_length=200,blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    format = models.CharField(max_length=1, choices=FORMAT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = PublishedManager()
    #{{download.file.size|filesizeformat}}<
    class Meta:
        ordering =('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        super(Book, self).save(*args, **kwargs)

    @property
    def download_count(self):
        return Download.objects.filter(book = self.pk).count()



    #def get_absolute_url(self):
        #return reverse("books:detail", kwargs={"slug": self.slug})


class Download(models.Model):
    date = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address + " "+ self.book.title
