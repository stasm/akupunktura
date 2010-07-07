from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

class PointManager(models.Manager):
    """Manager for Pressure Points."""
    def recently_added(self, count=10):
        return self.order_by('-time_added')[:count]

class City(models.Model):
    """City the Pressure Point belong to."""
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    lat = models.FloatField()
    lon = models.FloatField()

    def __unicode__(self):
        return self.name

class Point(models.Model):
    """Pressure Point model.

    The pressure points are the core concept of the app. They're small cases
    that the community shares, discusses about and eventually, take action
    upon in order to improve the quality of life.

    """
    title = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    description = models.TextField()
    # descriptive address or directions on how to find the Point
    directions = models.TextField()
    time_added = models.DateTimeField()

    # simple voting mechanism (like/dislike)
    thumbsup = models.IntegerField()
    thumbsdown = models.IntegerField()
    
    # foreign keys
    poster = models.ForeignKey(User)
    city = models.ForeignKey(City)
    
    # managers
    objects = PointManager()

    def __unicode__(self):
        return "%s x %s" % (self.lat, self.lon)

class Photo(models.Model):
    """Photo objects illustrating Pressure Points."""
    time_added = models.DateTimeField()
    thumbnail = models.ImageField(upload_to='upload/thumbnails', blank=True)
    original = models.ImageField(upload_to='upload/original')
    is_main = models.BooleanField()

    poster = models.ForeignKey(User)
    point = models.ForeignKey(Point, related_name='photos')

    def save(self, *args, **kwargs):
       if self.id is None:
           self.thumbnail = self.original
       super(Photo, self).save(*args, **kwargs)

class FeatureManager(models.Manager):
    """Manager for Feature objects."""
    def current(self):
        now = datetime.now()
        return self.filter(start_time__lt=now, end_time__gt=now)

class Feature(models.Model):
    """Pressure Point features on the home page."""
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    point = models.ForeignKey(Point, related_name='features')
    
    objects = FeatureManager()

class Resolution(models.Model):
    """Resolution objects describe how a Pressure Point was closed."""
    description = models.TextField()
    time_resolved = models.DateTimeField()

    point = models.OneToOneField(Point, related_name='resolution')
