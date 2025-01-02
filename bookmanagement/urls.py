# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookmanagement.views.author_viewset import AuthorViewSet

from bookmanagement.views.book_viewset import BookViewSet
from bookmanagement.views.borrow_record_viewset import BorrowRecordViewSet
from bookmanagement.views.report_viewset import ReportViewSet
from bookmanagement.views.protected_views import ProtectedView
from bookmanagement.views.auth_views import CustomTokenObtainPairView, TokenRefreshView

# Initialize the router
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'borrow', BorrowRecordViewSet)

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),           # Default DRF route for viewsets
    path('reports/', ReportViewSet.as_view(), name='generate-report'),  # Custom report endpoint
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected_view'),
]
