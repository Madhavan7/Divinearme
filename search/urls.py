from django.urls import path
from search.views.temple_view_set import TempleViewSet
from search.views.user_view_set import UserViewSet

temple_list = TempleViewSet.as_view({
    'get':'list'
})
temple_create = TempleViewSet.as_view({
    'post':'create'
})
temple_detail = TempleViewSet.as_view({
    'put':'update',
    'get':'retrieve',
})

user_list = UserViewSet.as_view({
    'get':'list',
})
user_create = UserViewSet.as_view({
    'post':'create'
})
user_detail = UserViewSet.as_view({
    'put':'update',
    'get':'retrieve',
})
urlpatterns = [
               path('temples/create/', temple_create, name= 'temple-create'),
               path('temples/', temple_list, name='temple-list'),
               path('temples/<str:pk>/', temple_detail, name = 'temple-detail'),
               path('temples/<str:temple_pk>/users/', user_list, name ='user-list'),
               #path('temples/<str:temple_pk>/posts/create/),
               #path('temples/<str:temple_pk>/events/create/'),
               #path('temples/<str:temple_pk>/events/'),
               #path('temples/<str:temple_pk>/posts/'),
               #path('temples/<str:temple_pk>/posts/<str:post_pk>/'),
               #path('temples/<str:temple_pk>/posts/create/'),
               #path('events/<str:event_pk>/),
               #path('events/<str:event_pk>/users/'),
               #path('events/<str:event_pk>/posts/'),
               #path('events/<str:event_pk>/posts/create/'),
               #path('events/<str:event_pk>/posts/<str:post_pk>/'),
               path('users/', user_list, name='user-list'),
               path('users/create/', user_create, name='user-create'),
               path('users/<str:pk>/', user_detail, name='user-detail'),
               #path('users/<str:user_pk>/events')
               path('users/<str:user_pk>/temples',temple_list, name = 'temple-list'),
               ]