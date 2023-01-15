from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .utils import Util

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Passwords must be equal'}
            )
        return attrs

    def create(self, validated_data):
        relative_link = self.context['request'].META['HTTP_HOST'] \
                        + reverse('email-verify')

        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        token = RefreshToken().for_user(user)
        finish_link = 'http://' + relative_link + "?token=" + str(token)

        data = {
            'subject': 'Email confirmation',
            'link': finish_link,
            'body': 'Press the {} to activate your account',
            'to': user.email
        }
        Util.send_email(data)
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    payload = serializers.CharField(max_length=555, read_only=True)

    def save(self, **kwargs):
        user = User.objects.get(pk=kwargs['user_id'])
        user.is_active = True
        user.save()

    class Meta:
        model = User
        fields = ['payload']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=555)

    default_error_messages = {
        'bad_token': "Token is expired or invalid"
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            pass
