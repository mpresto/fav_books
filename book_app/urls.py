from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('create', views.add_book),
    path('<int:id>', views.book_detail),
    path('update/<int:id>', views.update_book),
    path('destroy/<int:id>', views.delete_book),
    path('favorite/<int:id>', views.add_favorite),
    path('destroy_favorite/<int:id>', views.remove_favorite),
    path('profile/<int:id>', views.user_detail),
]