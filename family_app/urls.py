from django.urls import path
from .views import (
    MemberView,
    MemberDetailView,
    RelationshipView,
    PathApiView,
)

urlpatterns = [
    path("members/", MemberView.as_view(), name="member-list-create"),
    path("members/<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
    path("relationships/", RelationshipView.as_view(), name="relationship-list-create"),
    path("find_paths/", PathApiView.as_view(), name="find-paths"),
]
