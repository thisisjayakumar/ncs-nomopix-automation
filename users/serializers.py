from rest_framework import serializers
from users.models import UserFeedback
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source='get_user_type_display', read_only=True)
    subscription = serializers.CharField(source='get_subscription_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'organisation', 'user_type', 'subscription', 'created_at']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = ['name', 'organisation', 'feedback', 'rating']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            validated_data['name'] = request.user.get_full_name() or request.user.username
        return super().create(validated_data)


class FeedbackListSerializer(serializers.ModelSerializer):
    is_registered_user = serializers.BooleanField(source='user.is_active', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = UserFeedback
        fields = ['id', 'name', 'is_registered_user', 'organisation',
                  'feedback', 'rating', 'created_at']