from django.db import models
from user.models import User



class Book(models.Model):

    title = models.CharField(max_length=100,unique=True)
    author = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='book_images',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    language = models.CharField(max_length=250)


    def __str__(self):
        return self.title
    

class BorrowedBook(models.Model):
    APROVAL_STATUS =[('aproved','APROVED'),
                     ('pending','PENDING'),
                     ('rejected','REJECTED'),
                   ]
     
    book_id = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_details')
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_details')
    approval_status = models.CharField(max_length=200,choices=APROVAL_STATUS,default='pending',blank=True,null=True)

    def __str__(self):
        return self.book_id.title
    

class BookTransaction(models.Model):

    STATUS = [
              ('returned','RETURNED'),
              ('rented','RENTED'),
              ]

    borrowed_book = models.ForeignKey( BorrowedBook, on_delete=models.CASCADE, related_name='transcation_borrowedbook',null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_user')
    status = models.CharField(max_length=20,choices=STATUS)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.borrowed_book.book_id.title

    

