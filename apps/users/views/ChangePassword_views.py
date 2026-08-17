from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.changepassword_serializer import ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )
