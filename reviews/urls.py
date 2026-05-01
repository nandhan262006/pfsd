from django.urls import path
from . import views

urlpatterns = [
    path('review/add/<int:booking_id>/', views.add_review_view, name='add_review'),
    path('review/<int:pk>/', views.review_detail_view, name='review_detail'),
]
