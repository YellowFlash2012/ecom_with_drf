from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import Product, ProductImages
from rest_framework.response import Response
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
    
    return Response({"success":True, "message":"Here are all the products...", "count":len(serializer.data), "products":serializer.data})
    
@api_view(['GET'])
def get_one_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    serializer = ProductSerializer(product, many=False)
    
    return Response({"success":True, "message":"Here is the product...", "product":serializer.data})


@api_view(['POST'])
def add_new_product(request):
    data  = request.data
    product = Product.objects.create(**data)
    
    serializer = ProductSerializer(product, many=False)
    
    return Response({"success":True, "message":"New product successfully added...", "product":serializer.data})
    

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