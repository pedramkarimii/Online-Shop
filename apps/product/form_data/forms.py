from django import forms
from apps.core import validators
from django.utils.translation import gettext_lazy as _
from apps.product.models import Brand, Product, Comment, Category, Discount, AddToInventory, Inventory, Wishlist


class BrandCreateForm(forms.ModelForm):
    """
    Form for creating a new brand.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor method to initialize form fields.
        """
        super(BrandCreateForm, self).__init__(*args, **kwargs)
        self.fields['logo'].widget.attrs['accept'] = 'image/*'

    class Meta:
        model = Brand
        fields = [
            'name', 'phone_number', 'description', 'location', 'logo'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'location': forms.Textarea(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'logo': forms.FileInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'name': _('Name'),
            'phone_number': _('Phone Number'),
            'description': _('Description'),
            'location': _('Location'),
            'logo': _('Logo')
        }
        help_texts = {
            'name': _('Enter the name of the brand .'),
            'phone_number': _('(021 4444 44 44) Enter the phone number of the brand.'),
            'description': _('Enter the description of the brand.'),
            'location': _('Enter the location of the brand.'),
            'logo': _('Enter the logo of the brand.')
        }
        error_messages = {
            'name': {
                'required': _('Name is required.'),
                'max_length': _('Name must be at most 50 characters long.'),
                'unique': _('Name must be unique.'),
            },
            'phone_number': {
                'required': _('Phone number is required.'),
                'max_length': _('Phone number must be at most 11 characters long.'),
                'unique': _('Phone number must be unique.'),
            },
            'description': {
                'required': _('Description is required.'),
                'max_length': _('Description must be at most 200 characters long.'),
            },
            'location': {
                'required': _('Location is required.'),
                'max_length': _('Location must be at most 200 characters long.'),
            },
            'logo': {
                'required': _('Logo is required.'),
                'invalid_image': _('Invalid image.'),
            },
        }
        required = {
            'name': True,
            'phone_number': True,
            'description': True,
            'location': True,
            'logo': True,
        }
        validators = {
            'name': [validators.NameValidator()],
            'phone_number': [validators.PhoneNumberValidator()],
            'description': [validators.NotesValidator()],
            'location': [validators.NotesValidator()],
            'logo': [validators.PictureValidator()],
        }

    def save(self, commit=True):
        """
        Method to save the Brand object.
        """
        brand = super().save(commit=False)  # noqa
        brand.name = self.cleaned_data['name']
        brand.phone_number = self.cleaned_data['phone_number']
        brand.description = self.cleaned_data['description']
        brand.location = self.cleaned_data['location']
        brand.logo = self.cleaned_data['logo']

        if commit:
            brand.save()
        return brand

    def logo_picture(self, user_id, commit=True):
        """
        Creates a brand instance with the logo picture.
        """
        brand = Brand.objects.get(user_id=user_id)
        if 'logo' in self.files:
            brand.logo = self.files['logo']
            if commit:
                brand.save()

        return brand


class BrandUpdateForm(BrandCreateForm):
    """
    Form for updating an existing brand.
    """
    def __init__(self, *args, **kwargs):
        self.brand_instance = kwargs.pop('brand_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Saves the updated brand instance.
        """
        brand = super().save(commit=False)  # noqa
        brand.name = self.cleaned_data['name']
        brand.phone_number = self.cleaned_data['phone_number']
        brand.description = self.cleaned_data['description']
        brand.location = self.cleaned_data['location']
        brand.logo = self.cleaned_data['logo']
        if self.brand_instance:
            if brand.name == self.brand_instance.name:  # noqa
                brand.name = self.brand_instance.name
            if brand.phone_number == self.brand_instance.phone_number:
                brand.phone_number = self.brand_instance.phone_number
            if brand.description == self.brand_instance.description:
                brand.description = self.brand_instance.description
            if brand.location == self.brand_instance.location:
                brand.location = self.brand_instance.location
            if not brand.logo:
                brand.logo = self.brand_instance.logo

        if commit:
            brand.save()
        return brand


class CategoryCreateForm(forms.ModelForm):
    """
    Form for creating a new category.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor method to initialize form fields.
        """
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['category_picture'].widget.attrs['accept'] = 'image/*'

    class Meta:
        model = Category
        fields = [
            'name', 'category_picture', 'is_sub_category', 'parent_category'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'parent_category': forms.Select(attrs={
                'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'category_picture': forms.FileInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'is_sub_category': forms.CheckboxInput(attrs={
                'class': 'form-check-input mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'name': _('Name'),
            'parent_category': _('Parent Category'),
            'category_picture': _('Category Picture'),
            'is_sub_category': _('Is Sub Category')
        }
        help_texts = {
            'name': _('Enter the name of the category.'),
            'parent_category': _('Enter the parent category of the category.'),
            'category_picture': _('Enter the category picture of the category.'),
            'is_sub_category': _('Enter the is sub category of the category.')
        }
        error_messages = {
            'name': {
                'required': _('Name is required.'),
                'max_length': _('Name must be at most 50 characters long.'),
                'unique': _('Name must be unique.'),
                'invalid_name': _('Invalid name.'),
            },
            'parent_category': {
                'invalid_choice': _('Invalid choice.'),
            },
            'category_picture': {
                'required': _('Category picture is required.'),
                'invalid_image': _('Invalid image.'),
            },
            'is_sub_category': {
                'invalid_boolean': _('Invalid boolean.'),
            },
        }
        required = {
            'name': True,
            'parent_category': False,
            'category_picture': True,
            'is_sub_category': False
        }

    def category_pictures(self, category_id, commit=True):
        """
        Creates a category instance with the category picture.
        """
        category = Category.objects.get(category_id=category_id)
        if 'category_picture' in self.files:
            category.category_picture = self.files['category_picture']
            if commit:
                category.save()

        return category

    def save(self, commit=True):
        """
        Method to save the Category object.
        """
        category = super(CategoryCreateForm, self).save(commit=False)
        category.name = self.cleaned_data['name']
        category.parent_category = self.cleaned_data['parent_category']
        category.category_picture = self.cleaned_data['category_picture']
        category.is_sub_category = self.cleaned_data['is_sub_category']
        if commit:
            category.save()
        return category


class CategoryUpdateForm(CategoryCreateForm):
    """
    Form for updating an existing category.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form fields with instance data.
        """
        self.category_instance = kwargs.pop('category_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Saves the updated category instance.
        """
        category = super().save(commit=False)  # noqa
        category.name = self.cleaned_data['name']
        category.parent_category = self.cleaned_data['parent_category']
        category.category_picture = self.cleaned_data['category_picture']
        category.is_sub_category = self.cleaned_data['is_sub_category']
        if self.category_instance:  # noqa
            if category.name == self.category_instance.name:  # noqa
                category.name = self.category_instance.name
            if category.parent_category == self.category_instance.parent_category:
                category.parent_category = self.category_instance.parent_category
            if category.category_picture == self.category_instance.category_picture:
                category.category_picture = self.category_instance.category_picture
            if category.is_sub_category == self.category_instance.is_sub_category:
                category.is_sub_category = self.category_instance.is_sub_category

        if commit:
            category.save()
        return category


class ProductCreateForm(forms.ModelForm):
    """
    Form for creating a new product.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['product_picture'].widget.attrs['multiple'] = True

    category = forms.ModelChoiceField(label=_('Category'), queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={
                                          'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                   'focus:border-indigo-500 '
                                                   'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    brand = forms.ModelChoiceField(label=_('Brand'),
                                   queryset=Brand.objects.all().filter(is_active=True, is_deleted=False),
                                   widget=forms.Select(attrs={
                                       'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                'focus:border-indigo-500 '
                                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    product_picture = forms.ImageField(label=_('Product Picture'), required=False,
                                       validators=[validators.PictureValidator()],
                                       widget=forms.FileInput(attrs={
                                           'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                    'focus:border-indigo-500 '
                                                    'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'size', 'color', 'material', 'weight', 'height', 'width', 'warranty',
            'quantity', 'category', 'brand', 'product_picture'
        ]
        widgets = {
            'category': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'brand': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'product_picture': forms.FileInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'size': forms.Select(attrs={
                'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'color': forms.Select(attrs={
                'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'material': forms.Select(attrs={
                'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'weight': forms.NumberInput(
                attrs={
                    'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                             'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'height': forms.NumberInput(
                attrs={
                    'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                             'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'width': forms.NumberInput(
                attrs={
                    'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                             'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'warranty': forms.Select(
                attrs={
                    'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                             'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                             'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'category': _('Category'),
            'product_picture': _('Product Picture'),
            'brand': _('Brand'),
            'name': _('Name'),
            'description': _('Description'),
            'price': _('Price'),
            'size': _('Size'),
            'color': _('Color'),
            'material': _('Material'),
            'weight': _('Weight'),
            'height': _('Height'),
            'width': _('Width'),
            'warranty': _('Warranty'),
            'quantity': _('Quantity')
        }
        help_texts = {
            'category': _('Select a category for the product'),
            'product_picture': _('Upload a product picture'),
            'brand': _('Select a brand for the product'),
            'name': _('Enter a name for the product'),
            'description': _('Enter a description for the product'),
            'price': _('Enter a price for the product'),
            'size': _('Enter a size for the product'),
            'color': _('Enter a color for the product'),
            'material': _('Enter a material for the product'),
            'weight': _('Enter a weight for the product'),
            'height': _('Enter a height for the product'),
            'width': _('Enter a width for the product'),
            'warranty': _('Enter a warranty for the product'),
            'quantity': _('Enter a quantity for the product')
        }
        error_messages = {
            'category': {
                'required': _('Category is required')
            },
            'product_picture': {
                'required': _('Product picture is required')
            },
            'brand': {
                'required': _('Brand is required')
            },
            'name': {
                'required': _('Name is required'),
                'max_length': _('Name must be at most 100 characters')
            },
            'description': {
                'required': _('Description is required'),
                'max_length': _('Description must be at most 500 characters')
            },
            'price': {
                'required': _('Price is required'),
                'invalid': _('Price must be a positive integer')
            },
            'size': {
                'required': _('Size is required'),
                'invalid': _('Size must be a valid size')
            },
            'color': {
                'required': _('Color is required'),
                'invalid': _('Color must be a valid color')
            },
            'material': {
                'required': _('Material is required'),
                'invalid': _('Material must be a valid material')
            },
            'weight': {
                'required': _('Weight is required'),
                'invalid': _('Weight must be a positive integer')
            },
            'height': {
                'required': _('Height is required'),
                'invalid': _('Height must be a positive integer')
            },
            'width': {
                'required': _('Width is required'),
                'invalid': _('Width must be a positive integer')
            },
            'warranty': {
                'required': _('Warranty is required'),
                'invalid': _('Warranty must be a valid warranty')
            },
            'quantity': {
                'required': _('Quantity is required'),
                'invalid': _('Quantity must be a positive integer')
            }
        }
        required = {
            'category': True,
            'product_picture': True,
            'brand': True,
            'name': True,
            'description': True,
            'price': True,
            'size': False,
            'color': True,
            'material': False,
            'weight': False,
            'height': False,
            'width': False,
            'warranty': False,
            'quantity': True
        }
        validators = {
            'product_picture': [validators.PictureValidator()],
            'name': [validators.NameValidator()],
            'description': [validators.NotesValidator()],
            'price': [validators.PriceValidator()],
            'size': [validators.SizeValidator()],
            'color': [validators.ColorValidator()],
            'material': [validators.MaterialValidator()],
            'warranty': [validators.WarrantyValidator()],
        }

    def save(self, commit=True):
        """
        Method to save the Product object.
        """
        product = super().save(commit=False)  # noqa
        product.category = self.cleaned_data['category']
        product.brand = self.cleaned_data['brand']
        product.name = self.cleaned_data['name']
        product.description = self.cleaned_data['description']
        product.product_picture = self.cleaned_data['product_picture']
        product.price = self.cleaned_data['price']
        product.size = self.cleaned_data['size']
        product.color = self.cleaned_data['color']
        product.material = self.cleaned_data['material']
        product.weight = self.cleaned_data['weight']
        product.height = self.cleaned_data['height']
        product.width = self.cleaned_data['width']
        product.warranty = self.cleaned_data['warranty']
        product.quantity = self.cleaned_data['quantity']
        if commit:
            product.save()
        return product


class ProductUpdateForm(ProductCreateForm):
    """
    Form for updating a product.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the product instance to be updated.
        """
        self.product_instance = kwargs.pop('product_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):  # noqa
        """
        Saves the updated product instance.
        """
        product = super().save(commit=False)  # noqa

        product.category = self.cleaned_data['category']
        product.brand = self.cleaned_data['brand']
        product.name = self.cleaned_data['name']
        product.description = self.cleaned_data['description']
        product.product_picture = self.cleaned_data['product_picture']
        product.price = self.cleaned_data['price']
        product.size = self.cleaned_data['size']
        product.color = self.cleaned_data['color']
        product.material = self.cleaned_data['material']
        product.weight = self.cleaned_data['weight']
        product.height = self.cleaned_data['height']
        product.width = self.cleaned_data['width']
        product.warranty = self.cleaned_data['warranty']
        product.quantity = self.cleaned_data['quantity']

        if self.product_instance:  # noqa
            if product.name == self.product_instance.name:  # noqa
                product.name = self.product_instance.name
            if product.category == self.product_instance.category:
                product.category = self.product_instance.category
            if product.brand == self.product_instance.brand:
                product.brand = self.product_instance.brand
            if product.description == self.product_instance.description:
                product.description = self.product_instance.description
            if product.product_picture == self.product_instance.product_picture:
                product.product_picture = self.product_instance.product_picture
            if product.price == self.product_instance.price:
                product.price = self.product_instance.price
            if product.size == self.product_instance.size:
                product.size = self.product_instance.size
            if product.color == self.product_instance.color:  # noqa
                product.color = self.product_instance.color
            if product.material == self.product_instance.material:
                product.material = self.product_instance.material
            if product.weight == self.product_instance.weight:
                product.weight = self.product_instance.weight
            if product.height == self.product_instance.height:
                product.height = self.product_instance.height
            if product.width == self.product_instance.width:
                product.width = self.product_instance.width
            if product.warranty == self.product_instance.warranty:
                product.warranty = self.product_instance.warranty
            if product.quantity == self.product_instance.quantity:
                product.quantity = self.product_instance.quantity
        if commit:
            product.save()
        return product


class CommentCreateForm(forms.ModelForm):
    """
    Form for creating a comment.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the post ID for which the comment is being created.
        """
        post_id = kwargs.pop('post_id', None)
        super().__init__(*args, **kwargs)
        if post_id:
            self.fields['reply'].queryset = Comment.objects.filter(post_id=post_id, is_reply=True)

    comment = forms.CharField(label=_('Comment'), max_length=500, widget=forms.Textarea(
        attrs={'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                        'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    reply = forms.ModelChoiceField(queryset=Comment.objects.all().filter(is_active=True, is_deleted=False),
                                   required=False,
                                   widget=forms.Select(
                                       attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                       'focus:border-indigo-500 '
                                                       'block w-full shadow-sm sm:text-sm border-gray-300 '
                                                       'rounded-md'}))
    is_reply = forms.BooleanField(label='Is Reply', required=False,
                                  widget=forms.CheckboxInput(
                                      attrs={'class': 'form-checkbox mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                      'focus:border-indigo-500 '
                                                      'block w-full shadow-sm sm:text-sm border-gray-300 '
                                                      'rounded-md'}))

    class Meta:
        model = Comment
        fields = ['comment', 'reply', 'is_reply']
        widgets = {
            'comment': forms.Textarea(
                attrs={'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'reply': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'is_reply': forms.CheckboxInput(
                attrs={'class': 'form-checkbox mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'comment': _('Comment'),
            'reply': _('Reply'),
            'is_reply': _('Is Reply')
        }
        help_texts = {
            'comment': _('Enter a comment for the post'),
            'reply': _('Select a reply for the comment'),
            'is_reply': _('Check if the comment is a reply')
        }
        error_messages = {
            'comment': {
                'required': _('Comment is required'),
                'max_length': _('Comment must be at most 500 characters')
            },
            'reply': {
                'required': _('Reply is required'),
                'invalid': _('Reply must be a valid comment')
            },
            'is_reply': {
                'required': _('Is Reply is required'),
                'invalid': _('Is Reply must be a valid boolean')
            }
        }
        required = {
            'comment': True,
            'reply': False,
            'is_reply': False
        }
        validators = {
            'comment': [validators.NotesValidator()],
        }

    def save(self, commit=True):
        """
        Method to save the Comment object.
        """
        comment = super().save(commit=False)
        comment.comment = self.cleaned_data['comment']
        comment.reply = self.cleaned_data['reply']
        comment.is_reply = self.cleaned_data['is_reply']
        if commit:
            comment.save()
        return comment


class DiscountCreateForm(forms.ModelForm):
    """
    Form for creating a discount.
    """
    product = forms.ModelChoiceField(queryset=Product.objects.all().filter(is_active=True, is_deleted=False),
                                     required=False, widget=forms.Select(
            attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                            'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all().filter(is_active=True, is_deleted=False),
                                      required=False, widget=forms.Select(
            attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                            'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    class Meta:
        model = Discount
        fields = ['product', 'category', 'percentage_discount', 'numerical_discount', 'expiration_date',
                  'is_use']
        widgets = {
            'product': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'category': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'percentage_discount': forms.Select(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'numerical_discount': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'expiration_date': forms.DateInput(
                attrs={'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'is_use': forms.Select(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'product': _('Product'),
            'category': _('Category'),
            'percentage_discount': _('Percentage Discount'),
            'numerical_discount': _('Numerical Discount'),
            'expiration_date': _('Expiration Date'),
            'is_use': _('Is Use')
        }
        help_texts = {
            'product': _('Select a product for the discount'),
            'category': _('Select a category for the discount'),
            'percentage_discount': _('Enter a percentage discount for the product'),
            'numerical_discount': _('Enter a numerical discount for the product'),
            'expiration_date': _('Enter an expiration date for the discount'),
            'is_use': _('Select if the discount is used')
        }
        error_messages = {
            'product': {
                'required': _('Product is required'),
                'invalid': _('Product must be a valid product')
            },
            'category': {
                'required': _('Category is required'),
                'invalid': _('Category must be a valid category')
            },
            'percentage_discount': {
                'required': _('Percentage Discount is required'),
                'invalid': _('Percentage Discount must be a valid integer')
            },
            'numerical_discount': {
                'required': _('Numerical Discount is required'),
                'invalid': _('Numerical Discount must be a valid integer')
            },
            'expiration_date': {
                'required': _('Expiration Date is required'),
                'invalid': _('Expiration Date must be a valid date')
            },
            'is_use': {
                'required': _('Is Use is required'),
                'invalid': _('Is Use must be a valid integer')
            }
        }
        required = {
            'product': False,
            'category': False,
            'percentage_discount': False,
            'numerical_discount': False,
            'expiration_date': True,
            'is_use': True
        }
        validators = {
            'percentage_discount': [validators.PercentageDiscountValidator()],
            'numerical_discount': [validators.NumericalDiscountValidator()],
        }

    def save(self, commit=True):
        """
        Method to save the Discount object.
        """
        discount = super().save(commit=False)  # noqa
        discount.product = self.cleaned_data['product']
        discount.category = self.cleaned_data['category']
        discount.percentage_discount = self.cleaned_data['percentage_discount']
        discount.numerical_discount = self.cleaned_data['numerical_discount']
        discount.expiration_date = self.cleaned_data['expiration_date']
        discount.is_use = self.cleaned_data['is_use']
        if commit:
            discount.save()
        return discount


class DiscountUpdateForm(DiscountCreateForm):
    """
    Form for updating a discount.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the discount instance to be updated.
        """
        self.discount_instance = kwargs.pop('discount_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Saves the discount with the updated fields.
        """
        discount = super().save(commit=False)  # noqa
        discount.product = self.cleaned_data['product']
        discount.category = self.cleaned_data['category']
        discount.percentage_discount = self.cleaned_data['percentage_discount']
        discount.numerical_discount = self.cleaned_data['numerical_discount']
        discount.expiration_date = self.cleaned_data['expiration_date']
        discount.is_use = self.cleaned_data['is_use']

        if self.discount_instance:  # noqa
            if discount.product == self.discount_instance.product:
                discount.product = self.discount_instance.product
            if discount.category == self.discount_instance.category:
                discount.category = self.discount_instance.category
            if discount.percentage_discount == self.discount_instance.percentage_discount:
                discount.percentage_discount = self.discount_instance.percentage_discount
            if discount.numerical_discount == self.discount_instance.numerical_discount:
                discount.numerical_discount = self.discount_instance.numerical_discount
            if discount.expiration_date == self.discount_instance.expiration_date:
                discount.expiration_date = self.discount_instance.expiration_date
            if discount.is_use == self.discount_instance.is_use:
                discount.is_use = self.discount_instance.is_use

        if commit:
            discount.save()

        return discount


class WishlistAddForm(forms.ModelForm):
    """
    Form for adding a product to a wishlist.
    """
    class Meta:
        model = Wishlist
        fields = ['product', 'order', 'quantity', 'total_price']
        widgets = {
            'product': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'order': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
        }
        labels = {
            'product': _(),
            'order': _(),
            'quantity': _(),
            'total_price': _(),
        }
        error_messages = {
            'product': {
                'required': _('Product is required'),
                'invalid': _('Inventory must be a valid Product')
            },
            'order': {
                'required': _('Order is required'),
                'invalid': _('Order must be a valid Order')
            },
            'quantity': {
                'required': _('Quantity is required'),
                'invalid': _('Quantity must be a valid integer')
            },
            'total_price': {
                'required': _('Total Price is required'),
                'invalid': _('Total Price must be a valid integer')
            }
        }
        required = {
            'product': True,
            'order': False,
            'quantity': True,
            'total_price': True
        }

    def save(self, commit=True):
        """
        Method to save the AddToInventory object.
        """
        add_to_wishlist = super().save(commit=False)
        add_to_wishlist.product = self.cleaned_data['product']
        add_to_wishlist.order = self.cleaned_data['order']
        add_to_wishlist.quantity = self.cleaned_data['quantity']
        add_to_wishlist.total_price = self.cleaned_data['total_price']
        if commit:
            add_to_wishlist.save()
        return add_to_wishlist


class WishlistUpdateForm(WishlistAddForm):
    """
    Form for updating a product in a wishlist.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the inventory instance to be updated.
        """
        self.add_to_wishlist_instance = kwargs.pop('add_to_wishlist_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Method to save the AddToInventory object.
        """
        add_to_wishlist = super().save(commit=False)
        add_to_wishlist.product = self.cleaned_data['product']
        add_to_wishlist.order = self.cleaned_data['order']
        add_to_wishlist.quantity = self.cleaned_data['quantity']
        add_to_wishlist.total_price = self.cleaned_data['total_price']
        if self.add_to_inventory_instance:  # noqa
            if add_to_wishlist.product == self.add_to_wishlist_instance.product:
                add_to_wishlist.product = self.add_to_wishlist_instance.product
            if add_to_wishlist.order == self.add_to_wishlist_instance.order:
                add_to_wishlist.order = self.add_to_wishlist_instance.order
            if add_to_wishlist.quantity == self.add_to_wishlist_instance.quantity:
                add_to_wishlist.quantity = self.add_to_wishlist_instance.quantity
            if add_to_wishlist.total_price == self.add_to_wishlist_instance.total_price:
                add_to_wishlist.total_price = self.add_to_wishlist_instance.total_price
        if commit:
            add_to_wishlist.save()
        return add_to_wishlist


class AddToInventoryCreateForm(forms.ModelForm):
    """
    Form for creating a new AddToInventory object.
    """
    inventory = forms.ModelChoiceField(queryset=Inventory.objects.all().filter(is_active=True, is_deleted=False),
                                       widget=forms.Select(
                                           attrs={
                                               'class': 'form-select mt-1 pt-2 py-2 px-4 '
                                                        'focus:ring-indigo-500 focus:border-indigo-500 '
                                                        'block w-full shadow-sm sm:text-sm border-gray-300 '
                                                        'rounded-md'}))
    product = forms.ModelChoiceField(queryset=Product.objects.all().filter(is_active=True, is_deleted=False),
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'form-select mt-1 pt-2 py-2 px-4 '
                                                      'focus:ring-indigo-500 focus:border-indigo-500 '
                                                      'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    quantity = forms.IntegerField(label=_('Quantity'), min_value=0, max_value=10000,
                                  widget=forms.NumberInput(attrs={
                                      'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                               'focus:border-indigo-500 '
                                               'block w-full shadow-sm sm:text-sm border-gray-300 '
                                               'rounded-md'}))

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the inventory instance to be updated.
        """
        super(AddToInventoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['inventory'].label_from_instance = lambda obj: f'{obj.name}'

    class Meta:
        model = AddToInventory
        fields = ['inventory', 'product', 'quantity']
        widgets = {
            'inventory': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'product': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'inventory': _('Inventory'),
            'product': _('Product'),
            'quantity': _('Quantity')
        }
        help_texts = {
            'inventory': _('Select a inventory for the product'),
            'product': _('Select a product for the warehouse keeper'),
            'quantity': _('Enter a quantity for the product')
        }
        error_messages = {
            'brand': {
                'required': _('Inventory is required'),
                'invalid': _('Inventory must be a valid brand')
            },
            'product': {
                'required': _('Product is required'),
                'invalid': _('Product must be a valid product')
            },
            'quantity': {
                'required': _('Quantity is required'),
                'invalid': _('Quantity must be a valid integer')
            }
        }
        required = {
            'inventory': True,
            'product': True,
            'quantity': True
        }

    def save(self, commit=True):
        """
        Method to save the AddToInventory object.
        """
        add_to_inventory = super().save(commit=False)
        add_to_inventory.inventory = self.cleaned_data['inventory']
        add_to_inventory.product = self.cleaned_data['product']
        add_to_inventory.quantity = self.cleaned_data['quantity']
        if commit:
            add_to_inventory.save()
        return add_to_inventory


class AddToInventoryUpdateForm(AddToInventoryCreateForm):
    """
    Form for updating an existing AddToInventory object.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the inventory instance to be updated.
        """
        self.add_to_inventory_instance = kwargs.pop('add_to_inventory_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Saves the updated AddToInventory object.
        """
        add_to_inventory = super().save(commit=False)
        add_to_inventory.inventory = self.cleaned_data['inventory']
        add_to_inventory.product = self.cleaned_data['product']
        add_to_inventory.quantity = self.cleaned_data['quantity']

        if self.add_to_inventory_instance:  # noqa
            if add_to_inventory.inventory == self.add_to_inventory_instance.inventory:
                add_to_inventory.inventory = self.add_to_inventory_instance.inventory
            if add_to_inventory.product == self.add_to_inventory_instance.product:
                add_to_inventory.product = self.add_to_inventory_instance.product
            if add_to_inventory.quantity == self.add_to_inventory_instance.quantity:
                add_to_inventory.quantity = self.add_to_inventory_instance.quantity

        if commit:
            add_to_inventory.save()

        return add_to_inventory


class InventoryCreateForm(forms.ModelForm):
    """
    Form for creating a new Inventory object.
    """
    class Meta:
        model = Inventory
        fields = ['name', 'quantity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'name': _('Name'),
            'quantity': _('Quantity'),
            'description': _('Description')
        }
        help_texts = {
            'name': _('Enter a name for the inventory'),
            'quantity': _('Enter a quantity for the inventory'),
            'description': _('Enter a description for the inventory')
        }
        error_messages = {
            'name': {
                'required': _('Name is required'),
                'invalid': _('Name must be a valid name')
            },
            'quantity': {
                'required': _('Quantity is required'),
                'invalid': _('Quantity must be a valid integer')
            },
            'description': {
                'required': _('Description is required'),
                'invalid': _('Description must be a valid description')
            }
        }
        required = {
            'name': True,
            'quantity': False,
            'description': False
        }
        validators = {
            'name': validators.NameValidator(),
            'description': validators.NameValidator()
        }

    def save(self, commit=True):
        """
        Saves the new Inventory object.
        """
        inventory = super().save(commit=False)
        inventory.name = self.cleaned_data['name']
        inventory.quantity = self.cleaned_data['quantity']
        inventory.description = self.cleaned_data['description']
        if commit:
            inventory.save()
        return inventory


class InventoryUpdateForm(InventoryCreateForm):
    """
    Form for updating an existing Inventory object.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the inventory instance to be updated.
        """
        self.inventory_instance = kwargs.pop('inventory_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Saves the updated Inventory object.
        """
        inventory = super().save(commit=False)
        inventory.name = self.cleaned_data['name']
        inventory.quantity = self.cleaned_data['quantity']
        inventory.description = self.cleaned_data['description']

        if self.inventory_instance:  # noqa
            if inventory.name == self.inventory_instance.name:
                inventory.name = self.inventory_instance.name
            if inventory.quantity == self.inventory_instance.quantity:
                inventory.quantity = self.inventory_instance.quantity
            if inventory.description == self.inventory_instance.description:
                inventory.description = self.inventory_instance.description

        if commit:
            inventory.save()

        return inventory


class SearchForm(forms.Form):
    """
    Form for searching.
    """
    search = forms.CharField(label=_('Search'), max_length=100)
