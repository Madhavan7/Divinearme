from django.contrib.gis.db import models

class location(models.Model):
    address = models.CharField(max_length=200)
    coordinates = models.PointField()

    def __str__(self):
        return self.address