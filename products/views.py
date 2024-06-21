from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Product, ProductImages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, ProductImagesSerializer
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET'])
def get_products(request):
    # filtering config
    filterset = ProductsFilter(request.GET, queryset=Product.objects.all().order_by("id"))
    
    # products = Product.objects.all()
    
    # pagination config
    resPerPage=9
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    

    queryset = paginator.paginate_queryset(filterset.qs, request)
    
    serializer = ProductSerializer(queryset, many=True)
    
    # print(len(serializer.data))
    
    return Response({"success":True, "message":"Here are all the products...", "count":len(serializer.data), "products":serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_one_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    serializer = ProductSerializer(product, many=False)
    
    return Response({"success":True, "message":"Here is the product...", "product":serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_new_product(request):
    data  = request.data
    
    serializer = ProductSerializer(data=data)
    
    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
    
        res = ProductSerializer(product, many=False)
    
        return Response({"success":True, "message":"New product successfully added...", "product":res.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors)
    
    

@api_view(['POST'])
def upload_product_images(request):
    data = request.data
    files = request.FILES.getlist("images")
    
    images = []
    for f in files:
        image = ProductImages.objects.create(product = Product(data['product']), image=f)
        
        images.append(image)
        
    serializer = ProductImagesSerializer(images, many=True)
    
    return Response({"success":True, "message":"Image uploaded successfully", 'images':serializer.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    if product.user != request.user:
        return Response({"success":False, "error":"You can NOT update this product"}, status=status.HTTP_403_FORBIDDEN)
    
    product.name=request.data["name"]
    product.description=request.data["description"]
    product.brand=request.data["brand"]
    product.price=request.data["price"]
    product.category=request.data["category"]
    product.ratings=request.data["ratings"]
    product.stock=request.data["stock"]
    
    product.save()
    
    serializer = ProductSerializer(product, many=False)
    
    return Response({"success":True, "message": f"Product {product.id} was successfully updated...", "product":serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    if product.user != request.user:
        return Response({"success":False, "error":"You can NOT delete this product"}, status=status.HTTP_403_FORBIDDEN)
    
    args = {"product":pk}
    images = ProductImages.objects.filter(args)
    for i in images:
        i.delete()
    
    product.delete()
    
    return Response({"success":True, "message": f"Product {product.id} was successfully deleted..."}, status=status.HTTP_200_OK)