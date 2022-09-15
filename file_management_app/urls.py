from django.urls import path
from file_management_app import views

urlpatterns = [
    path("imports", views.ImportsView.as_view()),
    path("delete/<str:pk>", views.DeleteView.as_view()),
    path("nodes/<str:pk>", views.NodesView.as_view()),
]
