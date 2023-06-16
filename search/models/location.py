from django.db import models

import googlemaps
import pprint
import time

API_KEY = 'AIzaSyCHTvQBwInGkU1J3caU7H3dTBAR78PnN_w'
gmaps = googlemaps.Client(key = API_KEY)

class location(models.Model):
    address = models.CharField(max_length=200)
    def __str__(self):
        return self.address