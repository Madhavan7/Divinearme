from django.urls import path
from search.views.temple_view_set import TempleViewSet
from search.views.user_view_set import UserViewSet
from search.views.event_view_set import EventViewSet
from search.views.post_view_set import PostViewSet
from search.views.invitation_view import InvitationView

temple_list = TempleViewSet.as_view({
    'get':'list'
})
temple_create_destroy = TempleViewSet.as_view({
    'post':'create',
    'delete':'destroy',
})
temple_detail = TempleViewSet.as_view({
    'put':'update',
    'get':'retrieve',
})

event_list = EventViewSet.as_view({
    'get':'list'
})
event_create_destroy = EventViewSet.as_view({
    'post':'create',
    'delete':'destroy',
})
event_detail = EventViewSet.as_view({
    'put':'update',
    'get':'retrieve',
})

user_list = UserViewSet.as_view({
    'get':'list',
})
user_create_destroy = UserViewSet.as_view({
    'post':'create',
    'delete': 'destroy',
})
user_detail = UserViewSet.as_view({
    'put':'update',
    'get':'retrieve',
})

post_list = PostViewSet.as_view({
    'get':'list'
})
post_create_destroy = PostViewSet.as_view({
    'post':'create',
    'delete':'destroy'
})
post_detail = PostViewSet.as_view({
    'put':'update',
    'get':'retrieve',
})

invitation_detail = InvitationView.as_view({
  'get':'retrieve'
})
invitation_list = InvitationView.as_view({
  'get':'list'
})

urlpatterns = [
               path('temples/create/', temple_create_destroy, name= 'temple-create'),
               path('temples/', temple_list, name='temple-list'),
               path('temples/<str:pk>/', temple_detail, name = 'temple-detail'),
               path('temples/<str:temple_pk>/users/', user_list, name ='temple-user-list'),
               path('temples/<str:temple_pk>/requests/', user_list, name = 'temple-user-list'),
               path('temples/<str:temple_pk>/posts/create/', post_create_destroy, name='temple-post-create'),
               path('temples/<str:temple_pk>/events/create/', event_create_destroy, name='temple-event-create'),
               path('temples/<str:temple_pk>/events/', event_list, name='temple-event-list'),
               path('temples/<str:temple_pk>/events/<str:pk>/', event_detail, name='temple-event-detail'),
               path('temples/<str:temple_pk>/posts/', post_list, name='temple-post-list'),
               path('temples/<str:temple_pk>/posts/<str:pk>/', post_detail, name='temple-post-detail'),
               path('events/<str:pk>/', event_detail, name='event-detail'),
               path('events/', event_list, name='event-list'),
               path('events/<str:event_pk>/users/', user_list, name='event-user-list'),
               path('events/<str:event_pk>/posts/', post_list, name='event-post-list'),
               path('events/<str:event_pk>/posts/create/', post_create_destroy, name='event-post-create'),
               path('events/<str:event_pk>/posts/<str:pk>/', post_detail, name='event-post-detail'),
               path('users/', user_list, name='user-list'),
               path('users/create/', user_create_destroy, name='user-create'),
               path('users/<str:pk>/destroy/', user_create_destroy, name='user-destroy'),
               path('users/<str:pk>/', user_detail, name='user-detail'),
               path('users/<str:user_pk>/events/', event_list, name='user-event-list'),
               path('users/<str:user_pk>/temples/',temple_list, name = 'user-temple-list'),
               path('users/<str:user_pk>/invitations/', invitation_list, name='invitation-list'),
               path('users/<str:user_pk>/invitations/<str:pk>/', invitation_detail, name='invitation-detail'),
               ]