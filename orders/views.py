from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from .filters import *
from products.models import Product

from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    
    # filter config
    filterset = OrdersFilter(request.GET, queryset=Order.objects.all().order_by('id'))
    
    count = filterset.qs.count()
    
    # pagination config
    resPerPage = 9
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    
    queryset = paginator.paginate_queryset(filterset.qs, request)
    
    serializer = OrderSerializer(queryset, many=True)
    
    return Response({"success":True, "count":len(serializer.data), "page":resPerPage, "message":"Here are all the orders you placed on our site", "data":serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_single_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    serializer = OrderSerializer(order, many=False)
    
    return Response({"success":True, "message":"Here is the order you requested", "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    
    order_items = data["orderItems"]
    
    if order_items and len(order_items) == 0:
        return Response({"error":"Your cart is empty. Kindly add at least 1 product!"}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        total_amount = sum(item['price'] * item['quantity'] for item in order_items)
        
        order = Order.objects.create(
            user=user,
            street=data['street'],
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            phone_number=data['phone_number'],
            country=data['country'],
            total_amount=total_amount
        )
        
        # create order item and set order to order item
        for i in order_items:
            product = Product.objects.get(id=i["product"])
            
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i['quantity'],
                price=i['price']
            )
            
            # update product qty
            product.stock -= item.quantity
            product.save()
        
        serializer = OrderSerializer(order, many=False)
        
        return Response({"success":True, "message":"Order placed successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
