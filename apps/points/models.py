from django.db import models

class PointManager(models.Manager):
    def recent(self, count=10):
        return self.order_by('-added')[:count]

class City(models.Model):
    name = models.CharField(max_length=200)
    #slug = models.SlugField()

    def __unicode__(self):
        return self.name

class Point(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    added = models.DateTimeField()
    #votes = models.IntegerField()
    #fixed = models.BooleanField()
    #rating = models.FloatField()
    
    # foreign keys
    city = models.ForeignKey(City)
    
    # managers
    objects = PointManager()

    def __unicode__(self):
        return "%s x %s" % (self.lat, self.lon)
