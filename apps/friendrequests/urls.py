from django.urls import path
from apps.friendrequests.views import FriendRequestView, FriendsListView, PendingFriendRequestsView


urlpatterns = [
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<int:pk>/', FriendRequestView.as_view(), name='respond-friend-request'),
    path('list-of-friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),

]
