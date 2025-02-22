from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .utils import convert_price_to_eur

def book_list(request):
    books = [
        {"tittle": "The Great Gatsby", "author": "F. Scott Fitzenrald"},
        {"tittle": "To Kill a mockingbird", "author": "Harperr Lee"},
        {"tittle": "1984", "author": "George Orwell"}
    ]
    return JsonResponse({"books": books})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    eur_rate = 0.82 #tekyshii kyrs euro
    price_eur = convert_price_to_eur(product.price_usd, eur_rate)
    context = {'product': product, 'price_eur': price_eur}
    return render(request, 'product_detail.html', context)