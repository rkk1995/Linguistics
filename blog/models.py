from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# from django.conf import settings # AUTH_USER_MODEL
from django.utils import timezone

# many-to-many category-to-articles
class Category(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.PROTECT)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s: %s\t%s\t%s" % (
            self.post.__unicode__()[0:14], 
            self.id, self.text,
            self.user.__str__()
            )
    
    def __unicode__(self):
        return self.__str__()

    class Meta:
        ordering = ['-id']

# still need to add image.
class Post(models.Model):
    title        = models.CharField(max_length=120)
    article_text = models.TextField()
    author       = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    categories   = models.ManyToManyField(Category, related_name='posts')
    text_preview = models.TextField(blank=True)
    date         = models.DateField(auto_now_add=True, blank=True)
    slug         = models.TextField(blank=True, unique=True)

    def get_absolute_url(self):
        return reverse('article_detail', args=(self.slug))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.text_preview:
            self.generate_text_preview()
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

    # can we abstract to not be bound to the self?
    def generate_text_preview(self):
        if(len(str(self.article_text)) <= 150):
            self.text_preview = '"' + str(self.article_text)[0:] + '"'
        else:
            self.text_preview = '"' + str(self.article_text)[0:150] + '..."'
