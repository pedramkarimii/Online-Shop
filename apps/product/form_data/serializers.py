from rest_framework import serializers
from apps.core import validators
from apps.product.models import Product, Wishlist


class WishlistProductSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new wishlist product.
    """
    class Meta:
        model = Wishlist
        fields = [
            'user', 'product', 'quantity', 'total_price'
        ]
        extra_kwargs = {
            'user': {
                'required': True,
                'error_messages': {
                    'required': 'User is required.',
                    'invalid': 'Invalid user.'
                }
            },
            'product': {
                'required': True,
                'error_messages': {
                    'required': 'Product is required.',
                    'invalid': 'Invalid product.'
                }
            },
            'quantity': {
                'required': True,
                'min_value': 1,
                'error_messages': {
                    'required': 'Quantity is required.',
                    'min_value': 'Quantity must be at least 1.'
                }
            },
            'total_price': {
                'required': True,
                'validators': [validators.PriceValidator()],
                'error_messages': {
                    'required': 'Total price is required.',
                    'invalid': 'Total price must be a valid number.'
                }
            }
        }


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new product.
    """
    product_picture = serializers.ImageField(source='product_picture.url', read_only=True)

    class Meta:
        model = Product
        fields = [
            'brand', 'name', 'price', 'color', 'product_picture'
        ]
        extra_kwargs = {
            'brand': {
                'required': True,
                'max_length': 50,
                'error_messages': {
                    'required': 'Brand name is required.',
                    'max_length': 'Brand name cannot exceed 50 characters.'
                }
            },
            'name': {
                'required': True,
                'min_length': 2,
                'allow_blank': False,
                'validators': [validators.NameValidator()],
                'error_messages': {
                    'required': 'Product name is required.',
                    'min_length': 'Product name must be at least 2 characters long.',
                    'allow_blank': 'Product name cannot be blank.'
                }
            },
            'price': {
                'required': True,
                'allow_null': False,
                'validators': [validators.PriceValidator()],
                'error_messages': {
                    'required': 'Price is required.',
                    'invalid': 'Price must be a valid number.',
                    'allow_null': 'Price cannot be null.'
                }
            },
            'color': {
                'required': True,
                'validators': [validators.ColorValidator()],
                'error_messages': {
                    'required': 'Color is required.',
                    'invalid_choice': 'Invalid color choice.'
                }
            },
            'product_picture': {
                'write_only': True,
                'required': True,
                'validators': [validators.PictureValidator()],
                'error_messages': {
                    'required': 'Product picture is required.'
                }
            }
        }

