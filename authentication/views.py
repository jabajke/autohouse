import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import (EmailVerificationSerializer, LogoutSerializer,
                          RegistrationSerializer)

User = get_user_model()


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class EmailVerifyAPIView(generics.RetrieveAPIView):
    serializer_class = EmailVerificationSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_id = payload['user_id']
            serializer.save(user_id=user_id)

            return Response({
                'email': 'Successfully activated!'
            }, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link has expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
