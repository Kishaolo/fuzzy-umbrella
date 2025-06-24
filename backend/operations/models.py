from django.db import models
from datetime import datetime
#class Operation sozdaet table v db pod nozvaniem Operation
class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazvanie category')
    class Meta:
        #class meta otvechaet za meta dannie primer ato verbose_name to est nazvanie table v db
        verbose_name = "Category"
        verbose_name_plural = "Categoryes"
    def __str__(self):
            return f'{self.name}'
class Operation(models.Model):

    name = models.TextField(
        verbose_name="naimenovanie operatsii"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="opisaniae opiratsii",
    )
    cost = models.FloatField(
        verbose_name = "stoimost",
    )
    operation_at = models.DateTimeField(
        default=datetime.now, verbose_name="Date of operation"
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="operations",
        verbose_name="Category of operation"
    )

    class Meta:
        verbose_name = "operatsia" #chelovekochitaemoe nazvania dla modeli 
        verbose_name_plural = "operatsii" #mnoshestvennoe nazvanie modeli
        ordering = [] #poradok v kotorom zapis vozvarashaetsa iz db
        unique_together = () #opredelaet pola kotorie dolshni bit ynikalnimi
    def __str__(self):
            return f"At-{self.operation_at}-{self.name}"
class Order(models.Model):
    created = []

class Product(models.Model):
    name = models.TextField(verbose_name="nazvanie producta")
    descriptions = models.TextField(
        verbose_name= "naimenovanie producta",
        blank=True,
        null=True,
    )
    #parametr blank oznochaet chto pole moshet bit pystim
    #parametr null pole moshet sodershat parametr null to est bit pystim
    price = models.FloatField(
        verbose_name="stoimost",
    )
    kolvo_na_sklade = models.TextField(
        verbose_name = int(99)
    )
    order = models.ManyToManyField(
        Order, 
    )

    def __str__(self):
        return f"{self.name}, {self.price}" #vozvrashaet method v stroky

class Books(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.CharField(max_length=200)
    author = models.OneToOneField(
        Author
    )
    def __str__(self):
        return f"{self.title}, by {self.author} ({self.published_date})"
    
class Author(models.Model):
    name = models.CharField(max_length=255)
    # sdelali svaz one-to-many
    books = models.ForeignKey(
        Books, 
        on_delete=models.CASCADE,
        related_name='books', 
        null=True,
    )

    def __str__(self):
        return f"{self.name}"

class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    kreditka = models.IntegerField()

    def __str__(self):
         return f"{self.name}, {self.password}, {self.kreditka}"
    
class Xron(models.Model):
    name = models.CharField(
         max_length=255, 
         null=True, 
         blank=True,                         
    )
    kreditka = models.IntegerField()
    user = models.OneToOneField(
         User, 
         blank=True, 
         null=True, 
         on_delete=models.CASCADE, 
    )

    def __str__(self):
         return f"{self.name}, {self.kreditka}"

