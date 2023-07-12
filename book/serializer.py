from rest_framework import serializers
from .models import Book,BookTransaction,BorrowedBook
from .models import User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    
class UserSeralizer(serializers.ModelSerializer):
    model = User
    fields = '__all__'

class BorrowedBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowedBook
        fields = '__all__'

class BookTranscationSeralizer(serializers.ModelSerializer):

    class Meta:
        model = BookTransaction
        fields ='__all__'




  
    