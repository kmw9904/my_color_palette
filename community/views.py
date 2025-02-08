# community/views.py
from rest_framework import viewsets, permissions, generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class UserFeedView(generics.ListAPIView):
    """
    현재 사용자가 팔로우하는 사용자들의 게시글을 보여주는 피드 API
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 사용자가 팔로우하는 사용자의 프로필을 가져옵니다.
        following_profiles = self.request.user.profile.following.all()
        # following_profiles는 Profile 객체들의 QuerySet입니다.
        # 이제 이들에 연결된 사용자의 게시글(Post)를 필터링합니다.
        users_followed = [profile.user for profile in following_profiles]
        return Post.objects.filter(user__in=users_followed).order_by('-created_at')
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
