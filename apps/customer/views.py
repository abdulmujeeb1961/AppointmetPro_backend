from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from apps.customer.models import Customer
from apps.customer.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Customer.objects.filter(business__owner=self.request.user)
    
    def perform_create(self, serializer):
        
                
        # Get the selected business from the validated serializer data
        business = serializer.validated_data["business"]

        # Ensure the logged-in user owns the selected business
        if business.owner != self.request.user:
            raise PermissionDenied(
                "You are not allowed to add customer to this business."
            )
        last_customer=Customer.objects.filter(business=business).order_by("-id").first()
        
        if not last_customer:
            customer_code="CUS001"
        else:
            last_number=int(last_customer.customer_code[3:])
            customer_code=f"CUS{last_number+1:03d}" # :03 means keep 3 digits i.e 003,099,100 and so on.  So last number will become CUS004 if the previous code was EMP003
        serializer.save(customer_code=customer_code)

        