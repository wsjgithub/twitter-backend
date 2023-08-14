from rest_framework import serializers
from friendship.models import Friendship
from rest_framework.exceptions import ValidationError
from accounts.api.serializers import UserSerializer

class FriendshipSerializerForCreate(serializers.ModelSerializer):
    # do we need to explicity specify fields? what form will the foregnkey take?
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()
    class Meta:
        model = Friendship
        fields = ('from_user_id', 'to_user_id')
    
    def validate(self, data):
        if data['from_user_id'] == data['to_user_id']:
            raise ValidationError({
                "message": "Follower and following can't be the same"
            })
        return data
    
    def create(self, valid_data):
        return Friendship.objects.create(
            from_user_id=valid_data['from_user_id'],
            to_user_id=valid_data['to_user_id']
        )
    
class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='from_user')
    created_at = serializers.DateTimeField()
    class Meta:
        model = Friendship
        fields = ('user', 'created_at')

class FollowingSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='to_user')
    created_at = serializers.DateTimeField()
    class Meta:
        model = Friendship
        fields = ('user', 'created_at')