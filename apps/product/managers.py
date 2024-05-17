from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from django.db.models import F, Q, Sum
import pytz
from django.utils import timezone


class WishlistQuerySet(models.QuerySet):
    def available(self):
        return self.filter(available=True)

    def unavailable(self):
        return self.filter(available=False)

    def with_quantity_greater_than(self, quantity):
        return self.filter(quantity__gt=quantity)

    def with_quantity_less_than(self, quantity):
        return self.filter(quantity__lt=quantity)

    def for_user(self, user):
        return self.filter(user=user)

    def for_product(self, product):
        return self.filter(product=product)


class WishlistManager(models.Manager):
    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = WishlistQuerySet(self.model)
        return self.__queryset

    def available(self):
        return self.get_queryset().available()

    def unavailable(self):
        return self.get_queryset().unavailable()

    def with_quantity_greater_than(self, quantity):
        return self.get_queryset().with_quantity_greater_than(quantity)

    def with_quantity_less_than(self, quantity):
        return self.get_queryset().with_quantity_less_than(quantity)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def for_product(self, product):
        return self.get_queryset().for_product(product)


class CodeDiscountQuerySet(models.QuerySet):
    """QuerySet for handling code discounts."""

    def get_discount(self, code):
        """Retrieve a discount by its code."""
        return self.get(code=code)

    def is_valid(self):
        """Check if the discount code is currently valid."""
        now = timezone.now()
        return self.filter(
            is_expired=False,
            expiration_date__gte=now
        )

    def active_and_valid_discounts(self):
        """Retrieve active and currently valid discounts."""
        now = timezone.now().astimezone(pytz.timezone('Asia/Tehran'))
        return self.filter(is_active=True, expiration_date__gte=now)

    def valid_discounts(self):
        """Retrieve currently valid discounts."""
        now = timezone.now().astimezone(pytz.timezone('Asia/Tehran'))
        return self.filter(is_active=True, expiration_date__gte=now, is_expired=False)

    def expired_discounts(self):
        """Retrieve expired discounts."""
        now = timezone.now().astimezone(pytz.timezone('Asia/Tehran'))
        return self.filter(expiration_date__lt=now)

    def get_discount_by_code_and_user(self, code, user):
        """Retrieve a discount by its code and associated user."""
        now = timezone.now().astimezone(pytz.timezone('Asia/Tehran'))
        return self.filter(code=code, user=user, expiration_date__gte=now).first()


class CodeDiscountManager(models.Manager):
    """Manager for handling code discounts."""

    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = CodeDiscountQuerySet(self.model)
        return self.__queryset

    def get_discount(self, code):
        """Retrieve a discount by its code."""
        return self.get_queryset().get_discount(code)

    def is_valid(self):
        """Check if a discount is valid."""
        return self.get_queryset().is_valid()

    def get_discounts(self, codes):
        """Retrieve discounts by a list of codes."""
        return self.get_queryset().filter(code__in=codes)

    def active_discounts(self):
        """Retrieve active discounts."""
        return self.get_queryset().filter(is_active=True)

    def inactive_discounts(self):
        """Retrieve inactive discounts."""
        return self.get_queryset().filter(is_active=False)

    def expired_discounts(self):
        """Retrieve expired discounts."""
        return self.get_queryset().expired_discounts()

    def active_and_valid_discounts(self):
        """Retrieve active and valid discounts."""
        return self.get_queryset().active_and_valid_discounts()

    def valid_discounts(self):
        """Retrieve valid discounts."""
        return self.get_queryset().valid_discounts()

    def get_discount_by_code_and_user(self, code, user):
        """Retrieve a discount by its code and associated user."""
        return self.get_queryset().get_discount_by_code_and_user(code, user)


class AddToInventoryQuerySet(models.QuerySet):
    def available_products(self):
        """
        Returns warehouse keepers with available products.
        """
        return self.filter(quantity__gt=0)

    def by_brand(self, brand_id):
        """
        Returns warehouse keepers by a specific brand.
        """
        return self.filter(brand_id=brand_id)

    def active_products(self):
        """
        Returns warehouse keepers with active products.
        """
        return self.filter(product__is_active=True)

    def not_active_products(self):
        """
        Returns warehouse keepers with inactive products.
        """
        return self.filter(product__is_active=False)

    def delete_products(self):
        """
        Deletes warehouse keepers with zero quantity products.
        """
        return self.filter(quantity=0).delete()

    def total_quantity_lower_than(self, value):
        """
        Returns warehouse keepers with a total quantity lower than the specified value.
        """
        return self.annotate(total_quantity=Sum('quantity')).filter(total_quantity__lt=value)


class AddToInventoryManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = AddToInventoryQuerySet(self.model)
        return self.__queryset

    def available_products(self):
        """
        Returns warehouse keepers with available products using the custom queryset.
        """
        return self.get_queryset().available_products()

    def by_brand(self, brand_id):
        """
        Returns warehouse keepers by a specific brand using the custom queryset.
        """
        return self.get_queryset().by_brand(brand_id)

    def active_products(self):
        """
        Returns warehouse keepers with active products using the custom queryset.
        """
        return self.get_queryset().active_products()

    def not_active_products(self):
        """
        Returns warehouse keepers with inactive products using the custom queryset.
        """
        return self.get_queryset().not_active_products()

    def delete_products(self):
        """
        Deletes warehouse keepers with zero quantity products using the custom queryset.
        """
        return self.get_queryset().delete_products()

    def total_quantity_lower_than(self, value):
        """
        Returns warehouse keepers with a total quantity lower than the specified value using the custom queryset.
        """
        return self.get_queryset().total_quantity_lower_than(value)


class InventoryQuerySet(models.QuerySet):
    pass


class InventoryManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = InventoryQuerySet(self.model)
        return self.__queryset


class BrandQuerySet(models.QuerySet):
    def active_brands(self):
        """
        Returns active brands.
        """
        return self.filter(is_active=True)

    def inactive_brands(self):
        """
        Returns inactive brands.
        """
        return self.filter(is_active=False)

    def popular_brands(self):
        """
        Returns popular brands (e.g., based on sales or views).
        """
        # Replace this with your logic for determining popular brands
        return self.order_by('-sales')[:5]

    def alphabetical_order(self):
        """
        Returns brands in alphabetical order.
        """
        return self.order_by('name')

    def with_products_count(self):
        """
        Annotates each brand with the count of associated products.
        """
        return self.annotate(products_count=models.Count('product'))

    def with_active_products_count(self):
        """
        Annotates each brand with the count of associated active products.
        """
        return self.annotate(
            active_products_count=models.Count('product', filter=models.Q(product__is_active=True))
        )


class BrandManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = BrandQuerySet(self.model)
        return self.__queryset

    def active_brands(self):
        """
        Returns active brands using the custom queryset.
        """
        return self.get_queryset().active_brands()

    def inactive_brands(self):
        """
        Returns inactive brands using the custom queryset.
        """
        return self.get_queryset().inactive_brands()

    def popular_brands(self):
        """
        Returns popular brands using the custom queryset.
        """
        return self.get_queryset().popular_brands()

    def alphabetical_order(self):
        """
        Returns brands in alphabetical order using the custom queryset.
        """
        return self.get_queryset().alphabetical_order()

    def with_products_count(self):
        """
        Annotates each brand with the count of associated products using the custom queryset.
        """
        return self.get_queryset().with_products_count()

    def with_active_products_count(self):
        """
        Annotates each brand with the count of associated active products using the custom queryset.
        """
        return self.get_queryset().with_active_products_count()


class MediaQuerySet(models.QuerySet):
    def for_product(self, product):
        """
        Returns a queryset of media items associated with a specific product.
        """
        return self.filter(product=product)

    def images(self):
        """
        Returns a queryset of media items that are images.
        """
        return self.filter(media_picture__isnull=False)

    def ordered_by_creation(self):
        """
        Returns a queryset of media items ordered by their creation date.
        """
        return self.order_by('-created_at')

    def active(self):
        """
        Returns a queryset of active media items.
        """
        return self.filter(is_active=True)

    def inactive(self):
        """
        Returns a queryset of inactive media items.
        """
        return self.filter(is_active=False)


class MediaManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = MediaQuerySet(self.model)
        return self.__queryset

    def for_product(self, product):
        """
        Returns a queryset of media items associated with a specific product.
        """
        return self.get_queryset().for_product(product)

    def images(self):
        """
        Returns a queryset of media items that are images.
        """
        return self.get_queryset().images()

    def ordered_by_creation(self):
        """
        Returns a queryset of media items ordered by their creation date.
        """
        return self.get_queryset().ordered_by_creation()

    def active(self):
        """
        Returns a queryset of active media items.
        """
        return self.get_queryset().active()

    def inactive(self):
        """
        Returns a queryset of inactive media items.
        """
        return self.get_queryset().inactive()


class CategoryQuerySet(models.QuerySet):
    def main_categories(self):
        """
        Returns a queryset of main categories (not sub-categories).
        """
        return self.filter(is_sub_category=False)

    def sub_categories(self):
        """
        Returns a queryset of sub-categories.
        """
        return self.filter(is_sub_category=True)

    def with_parent(self, parent_category):
        """
        Returns a queryset of categories with a specific parent category.
        """
        return self.filter(parent_category=parent_category)

    def with_name(self, name):
        """
        Returns a queryset of categories with a specific name.
        """
        return self.filter(name=name)


class CategoryManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = CategoryQuerySet(self.model)
        return self.__queryset

    def main_categories(self):
        """
        Returns a queryset of main categories (not sub-categories).
        """
        return self.get_queryset().main_categories()

    def sub_categories(self):
        """
        Returns a queryset of sub-categories.
        """
        return self.get_queryset().sub_categories()

    def with_parent(self, parent_category):
        """
        Returns a queryset of categories with a specific parent category.
        """
        return self.get_queryset().with_parent(parent_category)

    def with_name(self, name):
        """
        Returns a queryset of categories with a specific name.
        """
        return self.get_queryset().with_name(name)

    def get_category_tree(self):
        """
        Returns a hierarchical representation of categories.
        """
        categories = self.get_queryset().prefetch_related('pcategory').all()
        category_tree = {}

        for category in categories:
            if not category.parent_category:
                category_tree[category] = {}
            else:
                parent = category.parent_category
                if parent not in category_tree:
                    category_tree[parent] = {}
                category_tree[parent][category] = {}

        return category_tree


class ProductQuerySet(models.QuerySet):
    def discounted(self, code_discount):
        """
        Annotates each product in the queryset with its discounted price based on the given code_discount.
        """
        if code_discount:
            percentage_discount = code_discount.percentage_discount
            numerical_discount = code_discount.numerical_discount

            if percentage_discount is not None:
                return self.annotate(discounted_price=F('price') - (F('price') * (percentage_discount / 100)))
            elif numerical_discount is not None:
                return self.annotate(discounted_price=F('price') - numerical_discount)

        return self.annotate(discounted_price=F('price'))


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = ProductQuerySet(self.model)
        return self.__queryset

    def discounted(self, code_discount=None):
        """
        Returns a queryset with products annotated with their discounted prices.
        """
        return self.get_queryset().discounted(code_discount)

    def in_stock(self):
        """
        Returns a queryset of products that are in stock.
        """
        return self.get_queryset().filter(stock__gt=0)

    def by_category(self, category):
        """
        Returns a queryset of products filtered by category.
        """
        return self.get_queryset().filter(category=category)

    def by_brand(self, brand):
        """
        Returns a queryset of products filtered by brand.
        """
        return self.get_queryset().filter(brand=brand)

    def top_selling(self):
        """
        Returns a queryset of top selling products.
        """
        # You need to define the logic for determining top selling products
        return self.get_queryset().order_by('-sales_count')[:10]

    def new_arrivals(self):
        """
        Returns a queryset of new arrival products.
        """
        from django.utils import timezone
        from datetime import timedelta
        return self.get_queryset().filter(created_at__gte=timezone.now() - timedelta(days=30))

    def with_images(self):
        """
        Returns a queryset of products with images.
        """
        return self.get_queryset().exclude(product_picture__isnull=True)

    def search(self, query):
        """
        Returns a queryset of products matching the given search query.
        """
        return self.annotate(
            similarity=TrigramSimilarity('name', query) +
                       TrigramSimilarity('brand__name', query) +  # noqa
                       TrigramSimilarity('description', query) +
                       TrigramSimilarity('price', query)
        ).filter(similarity__gt=0.3).order_by('-similarity')


class CommentQuerySet(models.QuerySet):
    def search(self, keyword):
        """
        Search comments by keyword.
        """
        return self.filter(Q(comment__icontains=keyword))

    def with_user(self):
        """
        Include user information in the queryset.
        """
        return self.select_related('user')

    def with_product(self):
        """
        Include product information in the queryset.
        """
        return self.select_related('product')

    def with_reply(self):
        """
        Include reply information in the queryset.
        """
        return self.select_related('reply')

    def active(self):
        """
        Filter active comments.
        """
        return self.filter(is_active=True)

    def inactive(self):
        """
        Filter inactive comments.
        """
        return self.filter(is_active=False)


class CommentManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = CommentQuerySet(self.model)
        return self.__queryset

    def search(self, keyword):
        """
        Search comments by keyword.
        """
        return self.get_queryset().search(keyword)

    def get_comments_by_user(self, user_id):
        """
        Get all comments created by a specific user.
        """
        return self.get_queryset().filter(user_id=user_id)

    def get_comments_by_product(self, product_id):
        """
        Get all comments related to a specific product.
        """
        return self.get_queryset().filter(product_id=product_id)

    def get_reply_comments(self):
        """
        Get all reply comments.
        """
        return self.get_queryset().filter(is_reply=True)

    def with_user(self):
        """
        Include user information in the queryset.
        """
        return self.get_queryset().with_user()

    def with_product(self):
        """
        Include product information in the queryset.
        """
        return self.get_queryset().with_product()

    def with_reply(self):
        """
        Include reply information in the queryset.
        """
        return self.get_queryset().with_reply()

    def active(self):
        """
        Get all active comments.
        """
        return self.get_queryset().active()

    def inactive(self):
        """
        Get all inactive comments.
        """
        return self.get_queryset().inactive()
