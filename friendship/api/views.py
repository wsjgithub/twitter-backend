from rest_framework import viewsets, permissions
from friendship.models import Friendship
from rest_framework.decorators import action
from friendship.api.serializers import FollowerSerializer, FollowingSerializer, FriendshipSerializerForCreate
from rest_framework.response import Response

class FriendshipViewSet(viewsets.GenericViewSet):
    queryset = Friendship.objects.all()
    
    @action(methods=["GET"], detail=True, permission_classes=[permissions.AllowAny])
    def followers(self, request, pk):
        friendships = Friendship.objects.filter(to_user_id=pk).order_by('-created_at')  
        serializer = FollowerSerializer(friendships, many=True, context={'request': request})
        return Response(
            {"followers": serializer.data},
            status=200
        )
    
    @action(methods=["GET"], detail=True, permission_classes=[permissions.AllowAny])
    def followings(self, request, pk):
        friendships = Friendship.objects.filter(from_user_id=pk).order_by('-created_at')  
        serializer = FollowingSerializer(friendships, many=True, context={'request': request})
        return Response(
            {"followings": serializer.data},
            status=200
        )
    
    @action(methods=["POST"], detail=True, permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk):
        if Friendship.objects.filter(from_user=request.user, to_user=pk).exists():
            return Response({
                'success': True,
                'duplicate': True
            }, status=201)
        serializer = FriendshipSerializerForCreate(data={
            "from_user_id": request.user.id,
            "to_user_id": pk
        })
        if not serializer.is_valid():
            return Response({
                "success": False,
                "error": serializer.errors
            }, status=400)
        serializer.save()
        return Response({
            "success": True
        }, status=201)
    
    @action(methods=["POST"], detail=True, permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk):
        if request.user.id == int(pk):
            return Response({
                "success": False,
                "error": "Can't unfollow yourself"
            }, status=400)
        deleted, _ = Friendship.objects.filter(from_user=request.user, to_user=pk).delete()
        return Response({
            "success": True,
            "deleted": deleted
        }, status=200)




