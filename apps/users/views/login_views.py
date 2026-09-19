from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.login_serializer import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    
    

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
                
        return Response (
            {
                "message": "User logged in successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user" : {
                    "id": user.id,
                    "username": user.username,
                    "mobile_number": user.mobile_number,
                    "role": user.role
                    
                }
                
                
                
            } ,
            status=status.HTTP_200_OK
            
            
        )
    
    
    class LogoutView(APIView):
        permission_classes = [AllowAny]
        def post(self, request):
            return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)