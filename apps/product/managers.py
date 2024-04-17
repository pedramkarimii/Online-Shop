from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from django.db.models import F, Q


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
