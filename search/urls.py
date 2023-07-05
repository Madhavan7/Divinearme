from django.urls import path
from search.views.temple_view_set import temple_view_set

temple_list = temple_view_set.as_view({
    'get':'list'
})
temple_create = temple_view_set.as_view({
    'post':'create'
})
temple_detail = temple_view_set.as_view({
    'put':'update',
    'get':'retrieve',
})
urlpatterns = [
               path('temples/create/', temple_create, name= 'temple-create'),
               path('temples/', temple_list, name='temple-list'),
               path('temples/<str:pk>/', temple_detail, name = 'temple-detail'),
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
               #path('users/'),
               #path('users/create/'),
               #path('users/<str:user_pk>/')
               #path('users/<str:user_pk>/events')
               path('users/<str:user_pk>/temples',temple_list, name = 'temple-list'),
               ]