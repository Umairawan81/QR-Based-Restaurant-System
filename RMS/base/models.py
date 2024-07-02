from django.db import models
class MenuItem(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    img = models.ImageField(upload_to='Menu/menu_images/' , default='')
    price = models.IntegerField()
    category = models.ManyToManyField('Category' , related_name='item')

    def __str__(self):
        return self.name



class Order(models.Model):
    items = models.ForeignKey(MenuItem , on_delete=models.SET_NULL , null=True)  
    quantity = models.IntegerField(default=0 , null=True , blank=True)
    price = models.IntegerField(default=0 )
    table_no = models.IntegerField(default=0 )


class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    

class QRGen(models.Model):
    imag = models.ImageField(upload_to='media')

  




  


