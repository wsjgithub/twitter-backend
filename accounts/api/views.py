from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, authenticate as django_authenticate, logout as django_logout
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, SignupSerializer, LoginSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer
    
    @action(methods=["GET"], detail=False)
    def login_status(self, request):
        data = {"has_logged_in": request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(instance=request.user, context={'request': request}).data
        return Response(data)


    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "error": serializer.errors
            }, status=400)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = django_authenticate(username=username, password=password)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "Username and password don't match.",
            }, status=400)
        django_login(request, user)
        return Response({
           "success": True, 
           "user": UserSerializer(instance=user, context={'request': request}).data
        })
    
    @action(methods=["POST"], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({"sucess": True})
    
    @action(methods=["POST"], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            django_login(request, user)
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
