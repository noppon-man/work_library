from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookListCreateView,BookDetailView,BookSearchView,MostRentBooksView,RentBookView,ReturnBookView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/search/', BookSearchView.as_view(), name='book-search'),
    path('books/<int:pk>/rent/', RentBookView.as_view(), name='rent-book'),
    path('books/<int:pk>/return/', ReturnBookView.as_view(), name='return-book'),
    path('books/most-rent/', MostRentBooksView.as_view(), name='most-rent-books'),]