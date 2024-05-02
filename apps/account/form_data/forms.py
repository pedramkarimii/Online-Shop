from apps.account.models import User, Address, CodeDiscount, Profile, Role
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput
from django import forms
import re
from apps.core import validators
from django.utils.translation import gettext_lazy as _


class UserPhoneNumberLoginForm(forms.Form):
    """Defines a form for user login using phone number, OTP code, and password.
    This form allows users to log in using their phone number, OTP code, and password.
    """
    phone_number = forms.CharField(label='Phone Number', max_length=11,
                                   validators=[validators.PhoneNumberMobileValidator()],
                                   widget=TextInput(attrs={
                                       'class': 'mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                                'block w-full shadow-sm sm:text-sm'
                                                ' border-gray-300 rounded-md'}))

    def clean_phone_number(self):
        """
        Clean and validate the phone number field.

        Raises:
            forms.ValidationError: If the phone number is invalid or not registered.
        """

        phone_number = self.cleaned_data['phone_number']
        try:
            user = User.objects.get(phone_number=phone_number)  # noqa
        except User.DoesNotExist:
            raise forms.ValidationError("User with this phone number does not exist.")
        return phone_number


class UserLoginUsernameOrEmailForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=100,
                                        widget=TextInput(attrs={'class': 'form-control mt-1 pt-2 py-2 px-4 '
                                                                         'text-xl focus:ring-indigo-500 '
                                                                         'focus:border-indigo-500 mb-2 '
                                                                         'block w-full shadow-sm '
                                                                         'sm:text-sm border-gray-300 rounded-md'}))
    password = forms.CharField(label='Password', validators=[validators.PasswordValidator()],
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control mt-4 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                            'text-xl focus:border-indigo-500 '
                                            'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))


class UserLoginEmailForm(forms.Form):
    """Defines a form for user login using email and password.
    This form allows users to log in using their email address and password.
    """

    email = forms.EmailField(label='Email', max_length=100, validators=[validators.EmailValidator()],
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                          'focus:border-indigo-500 '
                                          'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    def clean_email(self):
        """
        Clean and validate the email field.

        Raises:
            forms.ValidationError: If the email address is already registered,
                doesn't end with '@gmail.com' or '@yahoo.com',
                doesn't contain '@', contains spaces, is empty, longer than 254 characters, or doesn't end with '.com'.
        """
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)
        if not user:
            raise forms.ValidationError("Email address is not registered.")
        else:
            return email


class CleanDataUserForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'),
                                validators=[validators.PasswordValidator()],
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                             'focus:border-indigo-500 '
                                             'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))  # noqa
    password2 = forms.CharField(label=_('Confirm Password'),
                                validators=[validators.PasswordValidator()],
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                             'focus:border-indigo-500 '
                                             'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))  # noqa

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
        }
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'phone_number': _('Phone Number'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
        }

        help_texts = {
            'username': _('Enter a username that is between 3 and 20 characters long.'),
            'email': _('Enter a valid email address.'),
            'phone_number': _('Enter a valid phone number.'),
            'password1': _('Enter a password that is between 8 and 20 characters long.'),
            'password2': _('Confirm your password.'),
        }

        error_messages = {
            'username': {
                'required': _('This field is required.'),
                'min_length': _('This field must be at least 3 characters long.'),
                'max_length': _('This field must be at most 20 characters long.'),
            },
            'email': {
                'required': _('This field is required.'),
                'invalid': _('Enter a valid email address.'),
            },
            'phone_number': {
                'required': _('This field is required.'),
                'invalid': _('Enter a valid phone number.'),
            },
            'password1': {
                'required': _('This field is required.'),
                'min_length': _('This field must be at least 8 characters long.'),
                'max_length': _('This field must be at most 20 characters long.'),
            },
            'password2': {
                'required': _('This field is required.'),
                'min_length': _('This field must be at least 8 characters long.'),
                'max_length': _('This field must be at most 20 characters long.'),
            },
        }
        required = {
            'username': True,
            'email': True,
            'phone_number': True,
            'password1': True,
            'password2': True,
        }
        validators = {
            'username': [validators.UsernameValidator()],
            'email': [validators.EmailValidator()],
            'phone_number': [validators.PhoneNumberMobileValidator()],
            'password1': [validators.PasswordValidator()],
            'password2': [validators.PasswordValidator()],
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            user = User.objects.get(phone_number=phone_number)  # noqa
            raise ValidationError(_("User with this phone number already exists."))
        except User.DoesNotExist:
            pass
        return phone_number

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileCreateForm(forms.ModelForm):
    """
    This class defines a form for creating a user profile.
    """

    class Meta:
        model = Profile
        fields = ['name', 'last_name', 'gender', 'age', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'gender': forms.Select(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'age': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
        }
        labels = {
            'name': _('Name'),
            'last_name': _('Last Name'),
            'gender': _('Gender'),
            'age': _('Age'),
            'profile_picture': _('Profile Picture'),
        }
        help_texts = {
            'name': _('Enter your name.'),
            'last_name': _('Enter your last name.'),
            'gender': _('Select your gender.'),
            'age': _('Enter your age.'),
            'profile_picture': _('Upload a profile picture in .jpg or .png format.'),
        }
        required = {
            'name': True,
            'last_name': True,
            'gender': True,
            'age': True,
            'profile_picture': False,
        }
        validators = {
            'name': [validators.NameValidator()],
            'last_name': [validators.LastNameValidator()],
            'gender': [validators.GenderValidator()],
            'profile_picture': [validators.PictureValidator()],
        }

    def __init__(self, *args, **kwargs):
        """
        Constructor method to initialize form fields.
        """
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs['accept'] = 'image/*'

    def profile_pictures(self, user_id, commit=True):
        """
        Method to handle profile picture upload.

        Args:
            user_id (int): The ID of the user for whom the profile picture is uploaded.
            commit (bool, optional): Indicates whether to save the profile to the database. Defaults to True.

        Returns:
            Profile: The profile instance with the updated profile picture.
        """
        profile = Profile.objects.get(user_id=user_id)
        if 'profile_picture' in self.files:
            profile.profile_picture = self.files['profile_picture']
            if commit:
                profile.save()

        return profile

    def save(self, commit=True):
        profile = super().save(commit=False)  # noqa
        profile.name = self.cleaned_data['name']
        profile.last_name = self.cleaned_data['last_name']
        profile.gender = self.cleaned_data['gender']
        profile.age = self.cleaned_data['age']
        profile.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            profile.save()
        return profile


class RoleCreateForm(forms.ModelForm):
    """
    This class defines a form for creating a role.
    """
    code_discount = forms.ModelChoiceField(
        queryset=CodeDiscount.objects.all(), required=False,
        widget=forms.Select(attrs={
            'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                     'focus:border-indigo-500 '
                     'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    golden = forms.ModelChoiceField(queryset=Role.objects.filter(golden__isnull=False),
                                    required=False,
                                    widget=forms.SelectMultiple(attrs={
                                        'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                 'focus:border-indigo-500 '
                                                 'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    silver = forms.ModelChoiceField(queryset=Role.objects.filter(silver__isnull=False),
                                    required=False,
                                    widget=forms.SelectMultiple(attrs={
                                        'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                 'focus:border-indigo-500 '
                                                 'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    bronze = forms.ModelChoiceField(queryset=Role.objects.filter(bronze__isnull=False),
                                    required=False,
                                    widget=forms.SelectMultiple(attrs={
                                        'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                 'focus:border-indigo-500 '
                                                 'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    seller = forms.ModelChoiceField(queryset=Role.objects.filter(seller__isnull=False),
                                    required=False,
                                    widget=forms.SelectMultiple(attrs={
                                        'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                 'focus:border-indigo-500 '
                                                 'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    class Meta:
        model = Role
        fields = ['code_discount', 'golden', 'silver', 'bronze', 'seller']  # Added commas here
        labels = {
            'code_discount': _('Code Discount'),
            'golden': _('Golden'),
            'silver': _('Silver'),
            'bronze': _('Bronze'),
            'seller': _('Seller'),

        }
        help_texts = {
            'code_discount': _('Enter the code discount percentage for the role.'),
            'golden': _('Select the golden role.'),
            'silver': _('Select the silver role.'),
            'bronze': _('Select the bronze role.'),
            'seller': _('Select the seller role.'),
        }

    def save(self, commit=True):
        role = super().save(commit=False)  # noqa
        role.golden = self.cleaned_data['golden']
        role.silver = self.cleaned_data['silver']
        role.bronze = self.cleaned_data['bronze']
        role.seller = self.cleaned_data['seller']
        if commit:
            role.save()
        return role


class RoleUpdateForm(RoleCreateForm):
    def __init__(self, *args, **kwargs):
        self.role_instance = kwargs.pop('role_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        role = super().save(commit=False)  # noqa
        role = super().save(commit=False)  # noqa
        role.golden = self.cleaned_data['golden']
        role.silver = self.cleaned_data['silver']
        role.bronze = self.cleaned_data['bronze']
        role.seller = self.cleaned_data['seller']
        if self.role_instance:  # noqa
            if role.golden == self.role_instance.golden:  # noqa
                role.golden = self.role_instance.golden
            if role.silver == self.role_instance.silver:
                role.silver = self.role_instance.silver
            if role.bronze == self.role_instance.bronze:
                role.bronze = self.role_instance.bronze
            if role.seller == self.role_instance.seller:
                role.seller = self.role_instance.seller
        if commit:
            role.save()
        return role


class ProfileUpdateForm(ProfileCreateForm):
    def __init__(self, *args, **kwargs):
        self.profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=False)  # noqa
        profile.name = self.cleaned_data['name']
        profile.last_name = self.cleaned_data['last_name']
        profile.gender = self.cleaned_data['gender']
        profile.age = self.cleaned_data['age']
        profile.profile_picture = self.cleaned_data['profile_picture']
        if self.profile_instance:  # noqa
            if profile.name == self.profile_instance.name:  # noqa
                profile.name = self.profile_instance.name
            if profile.last_name == self.profile_instance.last_name:
                profile.last_name = self.profile_instance.last_name
            if profile.gender == self.profile_instance.gender:
                profile.gender = self.profile_instance.gender
            if profile.age == self.profile_instance.age:
                profile.age = self.profile_instance.age
            if profile.gender == self.profile_instance.gender:
                profile.gender = self.profile_instance.gender
        if commit:
            profile.save()
        return profile


class UserRegistrationForm(CleanDataUserForm):
    """
    This class defines a form for user registration, extending the CleanDataUserForm.

    Attributes:
        inheritance CleanDataUserForm

    Methods:
        __init__: Constructor method to initialize form fields.
        save: Method to save the created user as a regular user.
    """

    def save(self, commit=True):
        """
        Save the created user as a regular user.

        Args:
            commit (bool, optional): Indicates whether to save the user to the database. Defaults to True.

        Returns:
            User: The created user instance.
        """
        user = super().save(commit=False)
        user.is_staff = False
        user.is_admin = False
        if commit:
            user.save()
        return user


class ChangePasswordForm(PasswordChangeForm):
    """
    This class defines a form for changing user password, extending the PasswordChangeForm.

    Methods:
        __init__: Constructor method to customize form field widgets.
        clean_new_password1: Custom validation method to check password similarity and additional rules.
    """

    old_password = forms.CharField(label="Old Password", validators=[validators.PasswordValidator()],
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                'focus:border-indigo-500 '
                                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))  # noqa
    new_password1 = forms.CharField(label="New Password", validators=[validators.PasswordValidator()],
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                 'focus:border-indigo-500 '
                                                 'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))  # noqa
    new_password2 = forms.CharField(label="Confirm New Password", validators=[validators.PasswordValidator()],
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                 'focus:border-indigo-500 '
                                                 'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))  # noqa

    def __init__(self, *args, **kwargs):
        """
        Constructor method to customize form field widgets.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for password in ['old_password', 'new_password1', 'new_password2']:
            self.fields[password].widget.attrs.update({'class': 'form-control'})

    def clean_new_password1(self):
        """
        Clean the new password and ensure it meets complexity requirements.
        """
        new_password1 = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')
        username = self.user.username if self.user else None

        if new_password1 and old_password and new_password1 == old_password:
            raise ValidationError("The new password must be different from the old password.")

        if username and new_password1 and username in new_password1:
            raise ValidationError("The password cannot be too similar to the username.")

        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$"

        if len(new_password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        elif not re.match(pattern, new_password1):
            raise ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, one digit,"
                " and one special character.")
        elif ' ' in new_password1:
            raise ValidationError("Password cannot contain spaces.")
        if username and new_password1 and new_password1.lower().startswith(username.lower()):
            return new_password1
        return new_password1


class UserPasswordResetForm(PasswordResetForm):
    """
    This class defines a form for resetting user password, extending the PasswordResetForm.

    Methods:
        __init__: Constructor method to customize form field widgets.

    """

    def __init__(self, *args, **kwargs):
        """
        Constructor method to customize form field widgets.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for password in ['email']:
            self.fields[password].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('email',)


class UserUpdateForm(forms.ModelForm):
    """
    This class defines a custom user change form, extending the UserChangeForm.
    """

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    class Meta:
        """
        Meta class to specify the model and fields for the form.
        """
        model = User
        fields = ['username', 'email', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
        }

        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'phone_number': _('Phone Number'),
        }
        help_texts = {
            'username': _(
                'Username can contain letters, numbers, underscores, dots,'
                ' hyphens, and must be at least 4 characters long.'
            ),
            'email': _(
                'Please enter a valid Gmail or Yahoo email address.'
            ),
            'phone_number': _(
                'Please enter a valid phone number in the format 09121234567.'
            ),
        }
        error_messages = {
            'username': {
                'required': _('Username is required.'),
            }, 'email': {
                'required': _('Email is required.'),
            }, 'phone_number': {
                'required': _('Phone Number is required.'),
            }}
        required = {
            'username': True,
            'email': True,
            'phone_number': True,
        }
        validators = {
            'username': [validators.UsernameValidator()],
            'email': [validators.EmailValidator()],
            'phone_number': [validators.PhoneNumberMobileValidator()],
        }

    def save(self, commit=True):
        """
        Method to save the user object.
        """
        user = super().save(commit=False)  # noqa
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        if self.discount_code_instance:  # noqa
            if user.username == self.user_instance.username:  # noqa
                user.username = self.user_instance.username
            if user.email == self.user_instance.email:  # noqa
                user.email = self.user_instance.email
            if user.phone_number == self.user_instance.phone_number:  # noqa
                user.phone_number = self.user_instance.phone_number
        if commit:
            user.save()
        return user


class CreateAddressForm(forms.ModelForm):
    """
    This class defines a form for user Address information.
    """

    class Meta:
        """
        Meta class to specify the model and fields for the form, along with widget attributes,
        labels, help texts, and error messages.
        """
        model = Address
        fields = ['address_name', 'country', 'city', 'street', 'building_number', 'floor_number', 'postal_code',
                  'notes']
        widgets = {
            'address_name': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'country': forms.Select(attrs={
                'class': 'form-control text-2xl mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'city': forms.Select(attrs={
                'class': 'form-control text-2xl mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'street': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'building_number': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'floor_number': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'postal_code': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
        }
        labels = {
            'address_name': _('Address Name'),
            'country': _('Country'),
            'city': _('City'),
            'street': _('Street'),
            'building_number': _('Building Number'),
            'floor_number': _('Floor Number'),
            'postal_code': _('Postal Code'),
            'notes': _('Notes'),
        }
        help_texts = {
            'address_name': _('Enter a name for this address.'),
            'country': _('Select the country where this address is located.'),
            'city': _('Select the city where this address is located.'),
            'street': _('Enter the street address.'),
            'building_number': _('Enter the building number.'),
            'floor_number': _('Enter the floor number.'),
            'postal_code': _('Enter the postal code.'),
            'notes': _('Enter any additional notes or information about this address (optional).'),
        }
        error_messages = {
            'address_name': {
                'required': _('The address name field is required.'),
                'max_length': _('Ensure this field has no more than 50 characters.'),
            },
            'country': {
                'required': _('The country field is required.'),
            },
            'city': {
                'required': _('The city field is required.'),
            },
            'street': {
                'required': _('The street field is required.'),
                'max_length': _('Ensure this field has no more than 200 characters.'),
            },
            'building_number': {
                'required': _('The building number field is required.'),
                'max_length': _('Ensure this field has no more than 20 characters.'),
            },
            'floor_number': {
                'required': _('The floor number field is required.'),
                'max_length': _('Ensure this field has no more than 20 characters.'),
            },
            'postal_code': {
                'required': _('The postal code field is required.'),
                'max_length': _('Ensure this field has no more than 20 characters.'),
            },
            'notes': {
                'max_length': _('Ensure this field has no more than 500 characters.'),
            },
        }
        required = {
            'address_name': True,
            'country': True,
            'city': True,
            'street': True,
            'building_number': True,
            'floor_number': True,
            'postal_code': True,
            'notes': False,
        }
        validators = {
            'address_name': [validators.NameValidator()],
            'country': [validators.CountryValidator()],
            'city': [validators.CityValidator()],
            'street': [validators.StreetValidator()],
            'building_number': [validators.BuildingNumberValidator()],
            'notes': [validators.NotesValidator()],
        }

    def save(self, commit=True):
        """
        Method to save the address object.
        """
        address = super().save(commit=False)  # noqa
        address.address_name = self.cleaned_data['address_name']
        address.street = self.cleaned_data['street']
        address.building_number = self.cleaned_data['building_number']
        address.floor_number = self.cleaned_data['floor_number']
        address.postal_code = self.cleaned_data['postal_code']
        address.notes = self.cleaned_data['notes']
        if commit:
            address.save()
        return address


class UpdateAddressForm(CreateAddressForm):
    def __init__(self, *args, **kwargs):
        self.address_instance = kwargs.pop('address_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        address = super().save(commit=False)  # noqa
        address.address_name = self.cleaned_data['address_name']
        address.street = self.cleaned_data['street']
        address.building_number = self.cleaned_data['building_number']
        address.floor_number = self.cleaned_data['floor_number']
        address.postal_code = self.cleaned_data['postal_code']
        address.notes = self.cleaned_data['notes']
        if self.address_instance:  # noqa
            if address.address_name == self.address_instance.address_name:  # noqa
                address.address_name = self.address_instance.address_name
            if address.street == self.address_instance.street:
                address.street = self.address_instance.street
            if address.building_number == self.address_instance.building_number:
                address.building_number = self.address_instance.building_number
            if address.floor_number == self.address_instance.floor_number:
                address.floor_number = self.address_instance.floor_number
            if address.postal_code == self.address_instance.postal_code:
                address.postal_code = self.address_instance.postal_code
            if address.notes == self.address_instance.notes:
                address.notes = self.address_instance.notes
        if commit:
            address.save()
        return address


class DiscountCodeCreateForm(forms.ModelForm):
    """
    Form for creating or updating discount codes.
    """

    class Meta:
        """
        Meta class to specify the model and fields for the form.
        """

        model = CodeDiscount
        fields = ['role_name', 'code', 'percentage_discount', 'numerical_discount', 'expiration_date', 'is_use']
        widgets = {
            'role_name': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'code': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'percentage_discount': forms.Select(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'numerical_discount': forms.NumberInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'expiration_date': forms.DateInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'is_use': forms.Select(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'role_name': _('Role Name'),
            'code': _('Code'),
            'percentage_discount': _('Percentage Discount'),
            'numerical_discount': _('Numerical Discount'),
            'expiration_date': _('Expiration Date'),
            'is_use': _('Is Use')
        }
        help_texts = {
            'role_name': _('Select the role for the discount code.'),
            'code': _('Enter the discount code.'),
            'percentage_discount': _('Select the percentage discount.'),
            'numerical_discount': _('Enter the numerical discount.'),
            'expiration_date': _('Select the expiration date for the code.'),
            'is_use': _('Select if the discount cod is used')
        }
        error_messages = {
            'role_name': {
                'required': _('The role name field is required.'),
            },
            'code': {
                'required': _('The code field is required.'),
                'max_length': _('Ensure this field has no more than 100 characters.'),
            },
            'percentage_discount': {
                'min_value': _('Percentage discount cannot be less than 0.'),
            },
            'numerical_discount': {
                'min_value': _('Numerical discount cannot be less than 0.'),
            },
            'expiration_date': {
                'invalid': _('Enter a valid date.'),
                'required': _('The role name field is required.'),
            },
            'is_use': {
                'required': _('Is Use is required'),
                'invalid': _('Is Use must be a valid integer'),
            }
        }
        required = {
            'role_name': True,
            'code': True,
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
        discount_code = super().save(commit=False)  # noqa
        discount_code.role_name = self.cleaned_data['role_name']
        discount_code.code = self.cleaned_data['code']
        discount_code.percentage_discount = self.cleaned_data['percentage_discount']
        discount_code.numerical_discount = self.cleaned_data['numerical_discount']
        discount_code.expiration_date = self.cleaned_data['expiration_date']
        discount_code.is_use = self.cleaned_data['is_use']
        if commit:
            discount_code.save()
        return discount_code


class DiscountCodeUpdateForm(DiscountCodeCreateForm):
    """
    Form for updating discount codes.
    """

    def __init__(self, *args, **kwargs):
        self.discount_code_instance = kwargs.pop('discount_code_instance', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        discount_code = super().save(commit=False)  # noqa
        discount_code.role_name = self.cleaned_data['role_name']
        discount_code.code = self.cleaned_data['code']
        discount_code.percentage_discount = self.cleaned_data['percentage_discount']
        discount_code.numerical_discount = self.cleaned_data['numerical_discount']
        discount_code.expiration_date = self.cleaned_data['expiration_date']
        discount_code.is_use = self.cleaned_data['is_use']
        if self.discount_code_instance:  # noqa
            if discount_code.role_name == self.discount_code_instance.role_name:  # noqa
                discount_code.role_name = self.discount_code_instance.role_name
            if discount_code.code == self.discount_code_instance.code:
                discount_code.code = self.discount_code_instance.code
            if discount_code.percentage_discount == self.discount_code_instance.percentage_discount:
                discount_code.percentage_discount = self.discount_code_instance.percentage_discount
            if discount_code.numerical_discount == self.discount_code_instance.numerical_discount:
                discount_code.numerical_discount = self.discount_code_instance.numerical_discount
            if discount_code.expiration_date == self.discount_code_instance.expiration_date:
                discount_code.expiration_date = self.discount_code_instance.expiration_date
            if discount_code.is_use == self.discount_code_instance.is_use:
                discount_code.is_use = self.discount_code_instance.is_use

        if commit:
            discount_code.save()
        return discount_code


class VerifyCodeForm(forms.Form):
    """
    This class defines a form for verifying a code.

    Methods:
        clean_code: Method to clean and validate the code field.

    """
    code = forms.IntegerField(label='Code', max_value=999999,
                              widget=forms.NumberInput(attrs={
                                  'class': 'form-control mt-1  pt-1 py-1 px-1'
                                           ' focus:ring-indigo-500 focus:border-indigo-500'
                                           ' shadow-sm sm:text-sm border-gray-300 rounded-md', 'autocomplete': 'off'}))

    def clean_code(self):
        """
        Clean and validate the code field.

        Returns:
            int: Cleaned and validated code value.

        Raises:
            forms.ValidationError: If the code is not a 6-digit number.
        """
        code = self.cleaned_data['code']
        return code
