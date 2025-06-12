from rest_framework import serializers
from .models import Category, Product, Order, OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) # Display category details
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    ) # For creating/updating product with category ID

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image',
            'stock', 'available', 'created_at', 'updated_at',
            'category', 'category_id'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) # Simplified product representation
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'price', 'quantity']
        read_only_fields = ['price'] # Price should be set from product at order creation

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) # Order items are read-only here, managed separately or nested write
    user = serializers.ReadOnlyField(source='user.username') # Display username, set user from request context in view

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email',
            'address', 'postal_code', 'city', 'created_at',
            'updated_at', 'paid', 'items', 'get_total_cost'
        ]
        read_only_fields = ['created_at', 'updated_at', 'paid', 'get_total_cost']


# Basic User Serializer for user context (e.g. who created an order)
# This might be expanded or moved to a dedicated auth app later
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user
