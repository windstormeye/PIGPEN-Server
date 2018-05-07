import time

from .models import User
from .serializers import UserSerializer

from rest_framework import generics, status
from rest_framework.response import Response


# 创建用户
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        paramsDict = request.data
        if 'phone' in paramsDict.keys() and 'pass_word' in paramsDict.keys() and 'salt' in paramsDict.keys():
            serializer = UserSerializer(data=request.data)
            print(serializer)
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


# id查用户
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'actor': serializer.data,
            'timestamp': time.time(),
        })