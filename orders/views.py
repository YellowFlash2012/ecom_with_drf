from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from products.models import Product

# Create your views here.
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
