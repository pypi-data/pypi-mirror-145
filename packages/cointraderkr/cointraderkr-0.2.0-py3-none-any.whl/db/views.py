from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework import pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

import db.models as models
from db import string_models
import db.serializers as serializers


class StandardResultPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'


for model in string_models:
    vars()[f'{model}APIView'] = type(
        f'{model}APIView', # class name
        (generics.ListAPIView,), # inheritance (parent class)
        {
            'queryset': getattr(models, model).objects.all(),
            'serializer_class': getattr(serializers, f'{model}Serializer'),
            'pagination_class': StandardResultPagination,
            'filter_backends': [SearchFilter, OrderingFilter]
        }
    )


class LoginView(APIView):
    def post(self, request):
        id = request.data.get('username')
        pw = request.data.get('password')
        user = authenticate(username=id, password=pw)
        if user is not None:
            try:
                return Response({'Token': user.auth_token.key, 'id': user.id})
            except:
                return Response({'success': 'login success, but no token available'})
        else:
            return Response({'fail': 'no such user'})


class AccessTokenView(APIView):
    def post(self, request):
        id = request.data.get('username')
        pw = request.data.get('password')
        user = authenticate(username=id, password=pw)
        if user is not None:
            try:
                username = user.email
                access_token = models.AccessToken.objects.filter(username=username).first()
                return Response({'status': 'SUCCESS', 'access_token': access_token.token})
            except:
                return Response({'status': 'FAILED', 'access_token': '', 'message': 'no token'})
        else:
            return Response({'status': 'FAILED', 'access_token': '', 'message': 'no such user'})


class SaveLogView(APIView):
    def post(self, request):
        try:
            source = request.data.get('source')
            ip_address = request.data.get('ip_address')
            log_level = request.data.get('log_level')
            timestamp = request.data.get('timestamp')
            filename = request.data.get('filename')
            message = request.data.get('message')
            log_inst = models.Log(source=source,
                                  ip_address=ip_address,
                                  log_level=log_level,
                                  timestamp=timestamp,
                                  filename=filename,
                                  message=message)
            log_inst.save()
            return Response({'status': 'SUCCESS', 'message': 'Successfully saved log data'})
        except Exception as e:
            return Response({'status': 'FAILED', 'message': str(e)})