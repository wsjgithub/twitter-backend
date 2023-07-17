from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, SignupSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ViewSet):
    @action(methods=["POST"], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({
                "success": True,
                "user": UserSerializer(user, context={"request": request}).data
            })
        else:
            return Response({
                "success": False,
                "message": "Sign up failed",
                "errors": serializer.errors,
            }, status=400)
