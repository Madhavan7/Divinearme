from django.urls import path
from search.views.temple_view_set import temple_view_set
from search.views.user_view_set import user_view_set

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

user_list = user_view_set.as_view({
    'get':'list',
})
user_create = user_view_set.as_view({
    'post':'create'
})
user_detail = user_view_set.as_view({
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