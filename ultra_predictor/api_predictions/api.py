from rest_framework import generics, permissions
from .serializers import PredictionSerializer


class PredictionAPI(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PredictionSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)
