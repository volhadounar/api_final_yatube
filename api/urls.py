from django.urls import path

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet


router = DefaultRouter()
router.register(r'v1/posts', PostViewSet)
router.register(r'v1/posts/(?P<post>\d+)/comments', CommentViewSet,
                basename='Comment')
router.register(r'v1/follow', FollowViewSet)
router.register(r'v1/group', GroupViewSet, basename='Group')

urlpatterns = [
   path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls

for url in router.urls:
    print(url)
