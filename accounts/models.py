# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 'symmetrical=False'로 설정하면 A가 B를 팔로우한다고 해서 자동으로 B가 A를 팔로우하지는 않습니다.
    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers', 
        blank=True
    )
    bio = models.TextField(blank=True)  # 선택사항: 자기소개 등을 저장할 수 있음.
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # 선택사항: 프로필 사진

    def __str__(self):
        return f"{self.user.username} Profile"

# 새로운 사용자가 생성되면 자동으로 Profile을 생성하도록 시그널 등록
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
