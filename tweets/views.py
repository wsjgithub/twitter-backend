from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from tweets.models import Tweet
from tweets.api.serializers import TweetCreateSerializer, TweetSerializer
from rest_framework.response import Response


# Create your views here.
class TweetViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer  # try the other serializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = TweetCreateSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                data={
                    "success": False,
                    "message": "Check input",
                    "errors": serializer.errors,
                },
                status=400,
            )
        tweet = serializer.save()
        return Response(data=TweetSerializer(tweet, context={"request": request}).data, status=201)
    
    def list(self, request, *args, **kwargs):
        if 'user_id' not in request.query_params:
            return Response('Missing user id.', status=400)
        tweets = Tweet.objects.filter(user_id=request.query_params['user_id'])
        serializer = TweetSerializer(tweets, many=True, context={"request": request})
        return Response({"tweets": serializer.data}, status=200)
