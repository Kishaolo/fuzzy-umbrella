from django.db import models

#class Operation sozdaet table v db pod nozvaniem Operation
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

    class Meta:
        db_table = 'my_table1' #nazvanie table
        verbose_name = "operatsia" #chelovekochitaemoe nazvania dla modeli 
        verbose_name_plural = "operatsii" #mnoshestvennoe nazvanie modeli
        ordering = [] #poradok v kotorom zapis vozvarashaetsa iz db
        unique_together = () #opredelaet pola kotorie dolshni bit ynikalnimi
class Order(models.Model):
    created = [],

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
    
    def __str__(self):
        return f"{self.name}" #vozvrashaet method v stroky
