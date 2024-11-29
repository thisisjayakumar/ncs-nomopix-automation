from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source='get_user_type_display', read_only=True)
    subscription = serializers.CharField(source='get_subscription_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'organisation', 'user_type', 'subscription', 'created_at']
