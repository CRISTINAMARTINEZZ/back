from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Producto
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def list_products(request):#listamos los productos
    if request.method == 'GET':#Verificamos que el metodo sea GET
        products = Producto.objects.all()#Obtenemos todos los productos
        data = {"products": list(products.values())}#Mostramos la lista
        return JsonResponse(data)#lo enviamos como Json
    else:
        return JsonResponse({"error": "Método no permitido"})#Si es cualquier otro metodo

@csrf_exempt
def search_product(request):
    if 'name' in request.GET:#si es el metodo GET
        name = request.GET['name']#buscamos que en la quere tenga el campo name
        products = Producto.objects.filter(name__icontains=name)#buscamos coincidir el name con los nombres de los productos
        data = {"products": list(products.values())}#listamos todas las coincidencias
        return JsonResponse(data)#devolvemos la data como Json
    else:
        return JsonResponse({"error": "Nombre del producto no proporcionado"})#Si el nombre no fue proporcionado en la query

@csrf_exempt
def create_product(request):
    if request.method == 'POST':#verificamos que sea el metodo POST
        try:#control de error
            data = json.loads(request.body) #sacamos toda la data del request.body
            name = data.get('name', '')#seteamos el name del name
            description = data.get('description', '')#seteamos el description del description
            price = data.get('price', '')#price el description del price
            quantity = data.get('quantity', '')#quantity el description del quantity
            if name and description and price and quantity:#validamos que los campos no sean vacios
                price = float(price)#precio como decimal
                quantity = int(quantity)#cantidad como entero
                if price > 0 and quantity > 0:#verificamos que sean positivos mayores que 0
                    product = Producto.objects.create(name=name, description=description, price=price, quantity=quantity)#creamos el producto
                    return JsonResponse({"message": "Producto creado correctamente"})#retornamos en json con respuesta correcta creacion
                else:
                    return JsonResponse({"error": "El precio y la cantidad deben ser valores numéricos positivos"})#Si el precio o la cantidad son negativos o 0
            else:
                return JsonResponse({"error": "Todos los campos son obligatorios"}) #Si te falta un campo llenar
        except ValueError:
            return JsonResponse({"error": "El precio y la cantidad deben ser valores numéricos"})#si en lugar de numeros pones texto
    else:
        return JsonResponse({"error": "Método no permitido"})#si es otro metodo 

@csrf_exempt
def update_product(request, product_id):
    product = get_object_or_404(Producto, pk=product_id)#obtenemos el producto con la key de la query
    if request.method == 'PUT':#verificamos el metodo PUT
        try:#control de errores
            data = json.loads(request.body)#sacamos toda la data del request
            name = data.get('name', '')#seteamos name
            description = data.get('description', '')#seteamos description
            price = data.get('price', '')#seteamos price
            quantity = data.get('quantity', '')#seteamos quantity
            if name and description and price and quantity:#que todos los valores esten ingresados
                price = float(price)
                quantity = int(quantity)
                if price > 0 and quantity > 0:
                    product.name = name#reemplazamos del producto.name por name
                    product.description = description#reemplazamos del producto.description por description
                    product.price = price#reemplazamos del producto.price por price
                    product.quantity = quantity#reemplazamos del producto.quantity por quantity
                    product.save()#guardamos el producto actualziado
                    return JsonResponse({"message": "Producto actualizado correctamente"})#json de respuesta
                else:
                    return JsonResponse({"error": "El precio y la cantidad deben ser valores numéricos positivos"})
            else:
                return JsonResponse({"error": "Todos los campos son obligatorios"})
        except ValueError:
            return JsonResponse({"error": "El precio y la cantidad deben ser valores numéricos"})
    else:
        return JsonResponse({"error": "Método no permitido"})

@csrf_exempt
def delete_product(request, product_id):
    product = get_object_or_404(Producto, pk=product_id)#Obtenemos el producto con el ID de la query, si no hay retorna 404
    if request.method == 'DELETE':#verificamos que sea el metodo DELETE
        product.delete()#borramos el producto
        return JsonResponse({"message": "Producto eliminado correctamente"})#mensaje como json 
    else:
        return JsonResponse({"error": "Método no permitido"})#si es otro metodo
