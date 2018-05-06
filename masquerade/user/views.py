from .models import User
from .serializers import UserSerializer

from rest_framework import generics, status
from rest_framework.response import Response



class UserListViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.datam, status=status.HTTP_400_BAD_REQUEST)


class UserDetailViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response({
            'data' : serializer.data
        })