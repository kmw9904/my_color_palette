# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from .models import Profile
from .serializers import RegisterSerializer  # 이전에 만든 회원가입 시리얼라이저가 있다면 함께 사용

class RegisterView(APIView):
    """
    회원가입 API 뷰 (이전에 작성한 내용)
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(APIView):
    """
    요청한 사용자가 URL로 전달된 username을 가진 사용자를 팔로우합니다.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # 현재 사용자의 프로필에서 target_user의 프로필을 팔로우에 추가
        request.user.profile.following.add(target_user.profile)
        return Response({"message": f"You are now following {username}."}, status=status.HTTP_200_OK)

class UnfollowUserView(APIView):
    """
    요청한 사용자가 URL로 전달된 username을 가진 사용자를 언팔로우합니다.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        request.user.profile.following.remove(target_user.profile)
        return Response({"message": f"You have unfollowed {username}."}, status=status.HTTP_200_OK)
