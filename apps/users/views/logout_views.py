from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.logout_serializer import LogoutSerializer

from rest_framework.permissions import AllowAny

class LogoutView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LogoutSerializer

    def post(self, request):
        print("CONTENT TYPE:", request.content_type)
        print("BODY:", request.body)
        print("REQUEST.DATA:", request.data)
        print("TYPE:", type(request.data))

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(
            {
               "message": "User logged out successfully",
                              
            },
            
            status=status.HTTP_205_RESET_CONTENT
            
            )