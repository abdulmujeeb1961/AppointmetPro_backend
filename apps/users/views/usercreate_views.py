from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.serializers.usercreate_serializer import UserCreateSerializer
from rest_framework.permissions import AllowAny


class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        serializer = UserCreateSerializer(data=request.data)
      
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User created successfully",
                    "data": {
                        "first_name": serializer.validated_data.get('first_name'),
                        "username": serializer.validated_data.get('username'),
                        "role": serializer.validated_data.get('role')
                    }
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                "message": "User creation failed",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )