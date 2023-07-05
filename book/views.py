from django.shortcuts import render
from .models import BorrowedBook,BookTransaction,Book
from rest_framework import viewsets,status
from .serializer import BookSerializer,BookTransaction,BorrowedBookSerializer
from rest_framework import authentication,permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from user.permissions import IsLibrarian



class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset =Book.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = []


class BorrowedBookView(viewsets.ModelViewSet):
    serializer_class =BookSerializer
    queryset =Book.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsLibrarian]

#count has to be decreased
    @action(detail=True, methods=['post'])
    def approval(self,request,*args,**kwargs):
        user = request.user
        # book = self.get_object
        book = Book.objects.filter(title=request.data['title'])
        book_count = book.count
        if book_count == 0:
              return Response({"error": "book is not available"}, status=status.HTTP_404_NOT_FOUND)

        
        if BorrowedBook.objects.filter(user = user,book =book).exists():
            return Response({"error": "Member already has the book"}, status=status.HTTP_404_NOT_FOUND)

        rental_request = BorrowedBook.objects.create(user =user,book = book) 
        book.count = book.count - 1
        book.save()
    
        return Response({"message": "Rental request created", "rental_request_id": rental_request}, status=status.HTTP_201_CREATED)
    
    
    


    


        

            
        
          
        
        
        







