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

        if BorrowedBook.objects.filter(book_id=book,status ='aproved').exists():
            return Response({"error": "Book is already rented"}, status=status.HTTP_400_BAD_REQUEST)

        if book.count == 0:
            return Response({"error": "Book is out of stock"}, status=status.HTTP_400_BAD_REQUEST)

        rental_request = BorrowedBook.objects.create(user_id=user, book_id=book, approval_status ='pending')
        book.count = book.count - 1

        book.save()

        return Response({"message": "Rental request created", "rental_request_id": rental_request.id},
                        status=status.HTTP_201_CREATED)
    

class BookTranscationView(viewsets.ModelViewSet):   
    serializer_class = BorrowedBookSerializer
    queryset = BorrowedBook.objects.all()
    authentication_classes =[authentication.TokenAuthentication]
    
    @action(detail=True, methods=['post'])
    def return_book(self, request,*args,**kwargs):
        borrowed_book = self.get_object()
        transaction_obj = BookTransaction()
        transaction_obj.status = 'returned'
        transaction_obj.returned_date = datetime.datetime.now()
        transaction_obj.borrowed_book = borrowed_book
        transaction_obj.user = request.user
        book =borrowed_book.book_id
        book.count += 1
        book.save()
        transaction_obj.save()

        # Calculate fine for late returns
        borroweddate = transaction_obj.borrowed_date
        returned_date = datetime.datetime.now()
        fine = Pricing.calculate_price(borroweddate, returned_date)
        transaction_obj.fine = fine if fine is not None else 0
        return Response({
            "id": transaction_obj.id,
            "status": transaction_obj.status,
            "borrowed_date": transaction_obj.borrowed_date,
            "returned_date": transaction_obj.returned_date,
            "book": book.id,
            "user": transaction_obj.user.id,
            "fine": transaction_obj.fine,
        }, status=status.HTTP_200_OK)


class BorrowedBookListView(generics.ListAPIView):
    queryset =BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    authentication_classes =[authentication.TokenAuthentication]
    permission_classes = [IsLibrarian]


class BookBorrowAproveRejectView(generics.UpdateAPIView):
    queryset =BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsLibrarian]

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        print("book1",book)
        serializer = BorrowedBookSerializer(book, partial=True, data=request.data)
        if serializer.is_valid():
           obj = serializer.save()
           return Response(serializer.data)
        return Response({'message':f'successfully {obj.approval_status}' }, status=status.HTTP_201_CREATED)
    


  







    
    


    


        

            
        
          
        
        
        







