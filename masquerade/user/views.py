import time

from .models import User
from .serializers import UserSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# 创建用户
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        paramsDict = request.data
        if 'username' in paramsDict.keys() and 'password' in paramsDict.keys() and 'salt' in paramsDict.keys():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'id': serializer.data['id'],
                    'timestamp': time.time(),
                    'code': status.HTTP_200_OK,
                    'msg': "OK",
                })
            return Response({
                'msg' : 'create error',
                'code' : status.HTTP_400_BAD_REQUEST,
            })
        return Response({
            'code' : status.HTTP_400_BAD_REQUEST,
            'msg' : "missing parameter",
        })


# 有问题
class UserLogin(generics.RetrieveAPIView):
    permission_classes = IsAuthenticated

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        if serializer.is_valid():

            currentUser = serializer.save()
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(currentUser)
            token = jwt_encode_handler(payload)

            return Response({
                'code': status.HTTP_200_OK,
                'msg': "OK",
                'token': token,
                'actor': serializer.data,
                'timestamp': time.time(),
            })

# 有问题
# id查用户
class UserDetailView(generics.RetrieveAPIView):
    permission_classes = IsAuthenticatedOrReadOnly

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset)
        return Response({
            'code': status.HTTP_200_OK,
            'msg' : "OK",
            'actor': serializer.data,
            'timestamp': time.time(),
        })