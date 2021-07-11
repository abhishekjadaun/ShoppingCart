from django.db import models

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=100, default="")    
    sub_category=models.CharField(max_length=100,default="")   
    price=models.IntegerField(default="0")
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    image=models.ImageField(upload_to='shop/images',default="")

    def __str__(self) -> str:
        return self.product_name
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField( max_length=254)
    desc=models.CharField(max_length=5000)
    created=models.DateField()

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    address=models.CharField(max_length=500)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    item_json=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id=models.IntegerField()
    update_desc=models.CharField(max_length=1000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:40]+'--'+str(self.update_id)


    