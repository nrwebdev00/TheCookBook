from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.utlis.responses import standard_response

class CheckStatusView(APIView):
    def get(self, request):
        return standard_response(
            success=True,
            msg="API is running",
            note="The API is operational and ready to handle requests.",
            status_code=200
        )

class CheckCurrentUserView(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': getattr(user, 'name', ''),
        }

        return standard_response(
            success=True,
            msg="Current user fetched successfully",
            data=user_data,
            status_code=200
        )