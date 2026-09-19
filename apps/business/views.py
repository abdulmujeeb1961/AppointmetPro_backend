from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny as AllowedAny
from apps.business.models import Business
from apps.business.serializers import BusinessSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Business objects.
    """

    # Only authenticated users can access these APIs
    permission_classes = [IsAuthenticated]
    

    # Serializer used for validation and conversion
    serializer_class = BusinessSerializer

    # Base queryset
    queryset = Business.objects.all()

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user
        as the owner of the business.
        """
        serializer.save(owner=self.request.user)
        
class BusinessListViewSet(viewsets.ModelViewSet):
    

    # Only authenticated users can access these APIs
      permission_classes = [IsAuthenticated]

    # Serializer used for validation and conversion
      serializer_class = BusinessSerializer
      
    # Base queryset
      queryset=Business.objects.all()
    
      def get_queryset(self):
       return self.queryset.filter(owner=self.request.user)