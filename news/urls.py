from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CategoryViewSet, AreaViewSet, NewsViewSet, CommentViewSet, AdminRegisterView, LoginView, DistrictViewSet, UserRegisterView, AdminRegisterView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'news', NewsViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'districts', DistrictViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('auth/register/user/', UserRegisterView.as_view(), name='register-user'),
    path('auth/register/admin/', AdminRegisterView.as_view(), name='register-admin'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
