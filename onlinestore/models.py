from django.contrib.auth.models import User
from django.db import models
class BankTransfer(models.Model):
    idbank_transfer = models.IntegerField(primary_key=True)
    origin_bank = models.CharField(max_length=45, blank=True, null=True)
    destination_bank = models.CharField(max_length=45, blank=True, null=True)
    acount_number = models.CharField(max_length=45, blank=True, null=True)
    destination_account_number = models.CharField(max_length=45, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    order_idorder = models.ForeignKey('Order', models.DO_NOTHING, db_column='order_idorder')

    class Meta:
        managed = False
        db_table = 'bank_transfer'


class Buyer(models.Model):
    idbuyer = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=60, blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.idbuyer

    class Meta:
        managed = False
        db_table = 'buyer'


class Card(models.Model):
    idcreditcard = models.IntegerField(primary_key=True)
    card_number = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    expiration_date = models.CharField(max_length=45, blank=True, null=True)
    cvv = models.IntegerField(blank=True, null=True)
    card_type = models.CharField(max_length=45, blank=True, null=True)
    order_idorder = models.ForeignKey('Order', models.DO_NOTHING, db_column='order_idorder')

    class Meta:
        managed = False
        db_table = 'card'


class Cart(models.Model):
    iddetails = models.IntegerField(primary_key=True)
    product_idproduct = models.ForeignKey('Product', models.DO_NOTHING, db_column='product_idproduct')
    buyer_idbuyer = models.ForeignKey(Buyer, models.DO_NOTHING, db_column='buyer_idbuyer')
    product_units = models.IntegerField(blank=True, null=True)
    subtotal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart'


class Category(models.Model):
    idcategory = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'

    def __str__(self):
        return self.name


class Company(models.Model):
    idcompany = models.IntegerField(primary_key=True)
    rut = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    phone_number = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=45, blank=True, null=True)
    message = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class Order(models.Model):
    idorder = models.AutoField(primary_key=True)
    buyer_idbuyer = models.ForeignKey(Buyer, models.DO_NOTHING, db_column='buyer_idbuyer')
    status = models.CharField(max_length=45, blank=True, null=True)
    subtotal = models.IntegerField(blank=True, null=True)
    products_amount = models.IntegerField(blank=True, null=True)
    method = models.CharField(max_length=45, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'
    def __str__(self):
        return self.idorder

class Paypal(models.Model):
    idpaypal = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    details = models.CharField(max_length=45, blank=True, null=True)
    order_idorder = models.ForeignKey(Order, models.DO_NOTHING, db_column='order_idorder')

    class Meta:
        managed = False
        db_table = 'paypal'


class Product(models.Model):
    idproduct = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    code = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available_quantity = models.IntegerField(blank=True, null=True)
    quantity_sold = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='productos/',blank=True, null=True)
    tags = models.CharField(max_length=90, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    brand = models.CharField(max_length=45, blank=True, null=True)
    category_idcategory = models.ForeignKey(Category, models.DO_NOTHING, db_column='category_idcategory')

    class Meta:
        managed = False
        db_table = 'product'
    def __str__(self):
        return self.name
    def __int__(self):
        return self.idproduct
    def minus(self):
        return self.tags.lower()


class ProductOrder(models.Model):
    idproducto_order = models.AutoField(primary_key=True)
    product_idproduct = models.ForeignKey(Product, models.DO_NOTHING, db_column='product_idproduct')
    order_idorder = models.ForeignKey(Order, models.DO_NOTHING, db_column='order_idorder')
    quantity = models.IntegerField(blank=True, null=True)
    nondiscounted_unit_price = models.IntegerField(blank=True, null=True)
    discounted_unit_price = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_order'
    



class Review(models.Model):
    idreview = models.IntegerField(primary_key=True)
    stars = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    product_idproduct = models.ForeignKey(Product, models.DO_NOTHING, db_column='product_idproduct')
    buyer_idbuyer = models.ForeignKey(Buyer, models.DO_NOTHING, db_column='buyer_idbuyer')

    class Meta:
        managed = False
        db_table = 'review'


class Wishlist(models.Model):
    idwishlist = models.IntegerField(primary_key=True,null=False)
    product_idproduct = models.ForeignKey(Product, models.DO_NOTHING, db_column='product_idproduct')
    buyer_idbuyer = models.ForeignKey(Buyer, models.DO_NOTHING, db_column='buyer_idbuyer')
    

    class Meta:
        managed = False
        db_table = 'wishlist'
        
    def __int__(self):
        return self.idwishlist