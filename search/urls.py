from django.urls import path
from search.views.temple_view_set import TempleViewSet
from search.views.user_view_set import UserViewSet
from search.views.event_view_set import EventViewSet
from search.views.post_view_set import PostViewSet

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

event_list = EventViewSet.as_view({
    'get':'list'
})
event_create = EventViewSet.as_view({
    'post':'create'
})
event_detail = EventViewSet.as_view({
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

post_list = PostViewSet.as_view({
    'get':'list'
})
post_create = PostViewSet.as_view({
    'post':'create'
})
post_detail = PostViewSet.as_view({
    'put':'update',
    'get':'retrieve',
})

urlpatterns = [
               path('temples/create/', temple_create, name= 'temple-create'),
               path('temples/', temple_list, name='temple-list'),
               path('temples/<str:pk>/', temple_detail, name = 'temple-detail'),
               path('temples/<str:temple_pk>/users/', user_list, name ='temple-user-list'),
               path('temples/<str:temple_pk>/posts/create/', post_create, name='temple-post-create'),
               path('temples/<str:temple_pk>/events/create/', event_create, name='temple-event-create'),
               path('temples/<str:temple_pk>/events/', event_list, name='temple-event-list'),
               path('temples/<str:temple_pk>/events/<str:pk>/', event_detail, name='temple-event-detail'),
               path('temples/<str:temple_pk>/posts/', post_list, name='temple-post-list'),
               path('temples/<str:temple_pk>/posts/<str:pk>/', post_detail, name='temple-post-detail'),
               path('events/<str:pk>/', event_detail, name='event-detail'),
               path('events/', event_list, name='event-list'),
               #path('events/<str:event_pk>/users/'),
               path('events/<str:event_pk>/posts/', post_list, name='event-post-list'),
               path('events/<str:event_pk>/posts/create/', post_create, name='event-post-create'),
               path('events/<str:event_pk>/posts/<str:pk>/', post_detail, name='event-post-detail'),
               path('users/', user_list, name='user-list'),
               path('users/create/', user_create, name='user-create'),
               path('users/<str:pk>/', user_detail, name='user-detail'),
               path('users/<str:user_pk>/events', event_list, name='user-event-list'),
               path('users/<str:user_pk>/temples',temple_list, name = 'user-temple-list'),
               ]