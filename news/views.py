from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Category, Area, News, Comment, District
from .serializers import CategorySerializer, AreaSerializer, NewsSerializer, CommentSerializer, UserRegisterSerializer, UserLoginSerializer, AdminRegisterSerializer, DistrictSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAdminUser]

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'content', 'category__name', 'area__name', 'area__district__name']
    ordering_fields = ['created_at']
    filterset_fields = ['category__name', 'area__name', 'area__district__name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        area = self.request.query_params.get('area')
        district = self.request.query_params.get('district')
        if category:
            queryset = queryset.filter(category_id=category)
        if area:
            queryset = queryset.filter(area_id=area)
        if district:
            queryset = queryset.filter(area__district_id=district)
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        news_id = self.request.query_params.get('news')
        if news_id:
            queryset = queryset.filter(news_id=news_id)
        return queryset

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

# @method_decorator(csrf_exempt, name='dispatch')
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    @extend_schema(request=UserLoginSerializer, responses={200: None})
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='access_token',
                    value=str(refresh.access_token),
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                    max_age=60*60*24,  # 1 day
                )
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                    max_age=60*60*24*7,  # 7 days
                )
                return response
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterView(APIView):
    @extend_schema(request=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_409_CONFLICT)
        user = serializer.save()
        user.role = 'user'
        user.save(update_fields=['role'])
        return Response({
            'payload': serializer.data,
            'role': user.role,
        }, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class AdminRegisterView(APIView):
    @extend_schema(request=AdminRegisterSerializer)
    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_409_CONFLICT)
        user = serializer.save()
        user.role = 'admin'
        user.save(update_fields=['role'])
        return Response({
            'payload': serializer.data,
            'role': user.role,
        }, status=status.HTTP_200_OK)

class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role,
            'last_login': user.last_login,
            'date_joined': user.date_joined,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
        }, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserRegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)