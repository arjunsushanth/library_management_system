from django.shortcuts import render
from .models import BorrowedBook,BookTransaction,Book
from rest_framework import viewsets,status
from .serializer import BookSerializer,BookTranscationSeralizer,BorrowedBookSerializer
from rest_framework import authentication,permissions
from rest_framework import viewsets,generics,status
from rest_framework.decorators import action
from rest_framework.response import Response
from user.permissions import IsLibrarian
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from user import models
from book.pricing import Pricing
import datetime



class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes =(AllowAny)


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]
    
    def post(self, request, *args, **kwargs):
        request.data ['user_type'] = 'librarian'
        request.data ['username']  = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error':'book not created'},status=status.HTTP_400_BAD_REQUEST)
    
    
class BookUpdateView(generics.UpdateAPIView):
    queryset =Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        request.data ['user_type'] = 'librarian'
        serializer = BookSerializer(book, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'successfully updated'}, status=status.HTTP_201_CREATED)
    

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message':'successfully deleted'},status=status.HTTP_204_NO_CONTENT)


class BorrowedBookView(viewsets.ModelViewSet):
    serializer_class = BorrowedBookSerializer
    queryset = BorrowedBook.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        book = Book.objects.filter(title=request.data['title']).first()

        if not book:
            return Response({"error": "Book is not available"}, status=status.HTTP_404_NOT_FOUND)

        if BorrowedBook.objects.filter(user_id=user, book_id=book).exists():
            return Response({"error": "Member already has the book"}, status=status.HTTP_400_BAD_REQUEST)

        if book.count == 0:
            return Response({"error": "Book is out of stock"}, status=status.HTTP_400_BAD_REQUEST)

        rental_request = BorrowedBook.objects.create(user_id=user, book_id=book)
        book.count = book.count - 1
        # rental_request.aproval = 'APPROVED'

        book.save()

        return Response({"message": "Rental request created", "rental_request_id": rental_request.id},
                        status=status.HTTP_201_CREATED)
    

class BookTranscationView(viewsets.ModelViewSet):   
    serializer_class = BookTranscationSeralizer
    queryset = BookTransaction.objects.all()
    authentication_classes =[BasicAuthentication]
    
    @action(detail=True, methods=['post'])
    def return_book(self, request,*args,**kwargs):
        rental_request = self.get_object()
        rental_request.status = 'returned'
        rental_request.returned_date = datetime.datetime.now()
        rental_request.save()

        # Calculate fine for late returns
        borroweddate = rental_request.borrowed_date
        returned_date = datetime.datetime.now()
        fine = Pricing.calculate_price(borroweddate, returned_date)
        rental_request.fine = fine if fine is not None else 0

        return Response({
            "id": rental_request.id,
            "status": rental_request.status,
            "borrowed_date": rental_request.borrowed_date,
            "returned_date": rental_request.returned_date,
            "book": rental_request.book.id,
            "user": rental_request.user.id,
            "fine": rental_request.fine,
        }, status=status.HTTP_200_OK)


class BorrowedBookListView(generics.ListAPIView):
    queryset =BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    authentication_classes =[authentication.TokenAuthentication]
    permission_classes = [IsLibrarian]

  







    
    


    


        

            
        
          
        
        
        







