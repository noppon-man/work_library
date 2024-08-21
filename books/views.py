from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer


# เพิ่ม/แก้ไข/ลบ/ดูรายละเอียดหนังสือ
class BookListCreateView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ค้นหาหนังสือ
class BookSearchView(APIView):
    def get(self, request):
        queryset = Book.objects.all()
        title = request.query_params.get('title')
        author = request.query_params.get('author')
        category = request.query_params.get('category')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

# มากที่สุด
class MostRentBooksView(APIView):
    def get(self, request):
        books = Book.objects.order_by('rent_count')[:10]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# ยืม-คืน
class RentBookView(APIView):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if not book.is_rent:
            book.is_rent = True
            book.rent_count += 1
            book.save()
            return Response({'status': 'book rent'})
        else:
            return Response({'status': 'book already rent'}, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(APIView):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book.is_rent:
            book.is_rent = False
            book.save()
            return Response({'status': 'book returned'})
        else:
            return Response({'status': 'book was not rent'}, status=status.HTTP_400_BAD_REQUEST)
