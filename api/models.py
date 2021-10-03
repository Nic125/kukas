from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"

    def __str__(self):
        return self.name


class Expenses(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    type_value = models.CharField(max_length=10)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self):
        return self.name


def upload_path(instance, filename):
    return '/'.join(['image', str(instance.title), filename])


class Product(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=350)
    is_active = models.CharField(max_length=10, default='yes')
    subcategory_id = models.ForeignKey(Subcategory, null=True, on_delete=models.PROTECT)
    expenses = models.ManyToManyField(Expenses)
    on_sale = models.CharField(max_length=30, default="0")
    highlight = models.CharField(max_length=2, default="0")
    cost = models.CharField(max_length=20, default="0")
    profit = models.CharField(max_length=20, default="0")
    photo_file_name = models.CharField(max_length=50)
    photo_file_name2 = models.CharField(max_length=50)
    photo_file_name3 = models.CharField(max_length=50)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name + ", " + self.subcategory_id.name


class Stock(models.Model):
    name = models.CharField(max_length=30)
    amount = models.CharField(max_length=30)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stock"

    def __str__(self):
        return self.name + ", " + self.amount


class PendingSell(models.Model):
    total = models.CharField(max_length=20)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Compra pendiente"
        verbose_name_plural = "Compras pendientes"

    def __str__(self):
        return self.total + ", " + self.date_posted


class SellDetails(models.Model):
    sell = models.ForeignKey(PendingSell, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, default=0)
    amount = models.CharField(max_length=20, default=0)
    price = models.CharField(max_length=20, default=0)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Detalle compra"
        verbose_name_plural = "Detalles compras"

    def __str__(self):
        return self.sell + ", " + self.amount


class Sell(models.Model):
    shipping = models.CharField(max_length=20)
    total = models.CharField(max_length=20)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return self.date


class CloseSellDetails(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=20, default=100)
    size = models.CharField(max_length=20, default=0)
    amount = models.CharField(max_length=20, default=0)
    price = models.CharField(max_length=20, default=0)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Detalle compra"
        verbose_name_plural = "Detalles compras"

    def __str__(self):
        return self.sell + ", " + self.amount


class ClientData(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    province = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50)
    cp = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    date_posted = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)





