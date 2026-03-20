from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    UserPatchSerializer, 
    UserRetrieveSerializer, 
)


class UserViewSet(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UserPatchSerializer
        return UserRetrieveSerializer
    
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
