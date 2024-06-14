from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import Product
from rest_framework.response import Response
from .serializers import ProductSerializer

# Create your views here.
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    
    serializer = ProductSerializer(products, many=True)
    
    print(len(serializer.data))
    
    return Response({"success":True, "message":"Here are all the products...", "count":len(serializer.data), "products":serializer.data})
    
@api_view(['GET'])
def get_one_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    serializer = ProductSerializer(product, many=False)
    
    return Response({"success":True, "message":"Here is the product...", "product":serializer.data})