from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

########## ค้นหาหนังสือ ##########
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        category = self.request.query_params.get('category', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if category:
            queryset = queryset.filter(category__icontains=category)
        return queryset

########## ยืมหนังสือ ##########
    @action(detail=True, methods=['post'])
    def rent(self, request, pk=None):
        book = self.get_object()
        if not book.is_rent:
            book.is_rent = True
            book.rent_count += 1
            book.save()
            return Response({ 'Book rent successfully.'})
        return Response({ 'Book is already rent.'},)

########## คืนหนังสือ ##########
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        if book.is_rent:
            book.is_rent = False
            book.save()
            return Response({ 'Book returned successfully.'})
        return Response({ 'Book was not rent.'},)

########## หนังสือที่ถูกยืมมากที่สุด ##########
    @action(detail=False, methods=['get'])
    def most_rent(self, request):
        most_rent_books = Book.objects.order_by('-rent_count')[:10]
        serializer = self.get_serializer(most_rent_books, many=True)
        return Response(serializer.data)