from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<int:article_id>/',views.article_detail, name='article_detail'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('note/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('api/summarize/', views.summarize_text, name='summarize_text'),
    path('upload/', views.upload_article, name='upload_article'),
]