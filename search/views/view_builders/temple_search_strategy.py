from django.forms import ValidationError

from search.models.temple import temple
from search.models.user_profile import UserModel
import googlemaps as gmaps
import googlemaps.places as places
from search.apikeys import GOOGLE_PLACES_API_KEY

class SearchStrategy():
  def __init__(self) -> None:
    self.search_class = None
    self.queryset = None
    self.client = gmaps.Client(key=GOOGLE_PLACES_API_KEY)
  
  def construct_location_sql(self, lattitude, longitude, radius):
    processing = f'Create extension if not exists postgis;'
    new_processing = f'Select * from search_temple where ST_DistanceSphere(ST_MakePoint(longitude, lattitude), ST_MakePoint({longitude},{lattitude})) < {radius};'
    return processing + new_processing
  
  def search_location(self, **search_params):
    location = search_params.get('location', None)
    radius = min(int(search_params.get('radius', 50000)), 50000) 
    if location and radius:
      response_coordinates = places.find_place(client=self.client, input=location, fields=['place_id', 'geometry'], input_type='textquery')
      if response_coordinates['status'] != 'OK' or not response_coordinates['candidates']:
            raise ValidationError("cannot find this address", code = "error")
      lattitude = response_coordinates['candidates'][0]['geometry']['location']['lat']
      longitude = response_coordinates['candidates'][0]['geometry']['location']['lng']
      self.queryset = self.queryset.raw(self.construct_location_sql(lattitude, longitude, radius))

  def search_country(self, **search_params):
    country = search_params.get('country')
    if country:
      self.queryset = self.queryset.filter(country="country")
  
  def search_city(self, **search_params):
    city = search_params.get('city')
    if city:
      self.queryset = self.queryset.filter(city = 'city')

class TempleSearchStrategy(SearchStrategy):
  def __init__(self):
    super(TempleSearchStrategy, self).__init__()
    self.search_class = temple
    self.queryset = None

  def search(self,search_params):
    self.search_user_temples(**search_params)
    filters = [self.search_location, self.search_city, self.search_country]
    for filter in filters: 
      filter(**search_params)
    return self.queryset

  def search_user_temples(self,**search_params):
    if 'user_pk' in search_params:
      self.queryset = UserModel.objects.get(id=search_params['user_pk']).temples.all()
    else:
      self.queryset = temple.objects.all()
