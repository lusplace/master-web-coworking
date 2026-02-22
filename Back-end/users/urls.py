"""
URLs para la gestión de usuarios.
"""

from django.urls import path

from .views import (
    RegisterView, LoginView, LogoutView,
    UserListView, UserDetailView, CurrentUserView, PasswordChangeView,
    assign_group_view, list_groups_view,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('', UserListView.as_view(), name='user-list'),
    path('me/', CurrentUserView.as_view(), name='user-current'),
    path('change-password/', PasswordChangeView.as_view(), name='user-change-password'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('groups/', list_groups_view, name='group-list'),
    path('<int:user_id>/assign-group/', assign_group_view, name='user-assign-group'),
]

