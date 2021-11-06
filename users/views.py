from django.contrib.auth import authenticate
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.oauth2_validators import RefreshToken
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, ValidateUserSerializer
from rest_framework.pagination import PageNumberPagination


class RequiredQueryParam:
    _type_map = {
        int: openapi.TYPE_INTEGER,
        str: openapi.TYPE_STRING,
    }

    def __init__(self, parameters: list):
        self.params = []
        for param, param_type in parameters:
            self.params.append(openapi.Parameter(param,
                                                 in_=openapi.IN_QUERY,
                                                 description="user role",
                                                 type=self._type_map[param_type]))

    def params(self):
        return self.params


class UserView(GenericAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    @swagger_auto_schema(operation_summary="Add New User", tags=["User"])
    def post(self, request):
        body = request.data
        user = self.serializer_class(data=body)
        if user.is_valid():
            user.save()
            return Response(user.data, status=201)
        return Response(user.errors, status=422)

    params = RequiredQueryParam([('role', str)]).params

    @swagger_auto_schema(manual_parameters=params, operation_summary="User List", tags=["User"])
    def get(self, request):
        user_type = request.GET.get('role')
        users = User.objects.all()
        if user_type:
            users = users.filter(role=user_type)
        return self.get_paginated_response(self.paginate_queryset(self.serializer_class(users, many=True).data))


class TokenView(GenericAPIView):
    serializer_class = ValidateUserSerializer

    @swagger_auto_schema(tags=['OAuth'])
    def post(self, request):
        expire_seconds = 1800
        scopes = 'read write'

        user = authenticate(email=request.data['email'], password=request.data['password'])
        if not user:
            return Response({"error": "Invalid Login Credentials!"}, status=401)

        application = Application.objects.get(name="Authorization")
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            token=random_token_generator(request),
            expires=timezone.now() + timezone.timedelta(seconds=expire_seconds),
            scope=scopes)
        refresh_token = RefreshToken.objects.create(
            user=user,
            token=random_token_generator(request),
            access_token=access_token,
            application=application)

        token = {
            'access_token': access_token.token,
            'token_type': 'Bearer',
            'expires_in': expire_seconds,
            'refresh_token': refresh_token.token,
            'scope': scopes}
        return Response(token, status=201)
