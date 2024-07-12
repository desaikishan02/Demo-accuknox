from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
from apps.friendrequests.models import FriendRequest
from apps.users.serializers import UserSerializer
from apps.friendrequests.serializers import FriendRequestSerializer
from rest_framework.permissions import IsAuthenticated


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from_user = request.user
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(from_user=from_user,
                                                             created_at__gte=one_minute_ago).count()

        if recent_requests_count >= 3:
            return Response({'detail': 'You cannot send more than 3 friend requests within a minute.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        friend_request = FriendRequest.objects.get(id=pk, to_user=request.user)
        action = request.data.get('action')

        if action == 'accept':
            friend_request.accepted = True
            friend_request.save()
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)


class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = User.objects.filter(
            Q(sent_requests__to_user=request.user, sent_requests__accepted=True) |
            Q(received_requests__from_user=request.user, received_requests__accepted=True)
        ).distinct()
        return Response(UserSerializer(friends, many=True).data, status=status.HTTP_200_OK)


class PendingFriendRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        return Response(FriendRequestSerializer(pending_requests, many=True).data, status=status.HTTP_200_OK)
