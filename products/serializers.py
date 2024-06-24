
from rest_framework import serializers

from .models import Product, ProductImages, Review
class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(method_name="get_all_reviews", read_only=True)
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "brand", "category", "ratings", "stock", "user", "images", "reviews")
        
        extra_kwargs = {
            "name": {"required":True, "allow_blank":False},
            "description": {"required":True, "allow_blank":False},
            "brand": {"required":True, "allow_blank":False},
            "category": {"required":True, "allow_blank":False},
        }
        
    def get_all_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
