from apps.account.models import User, Address, CodeDiscount, Profile
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput
from django import forms
import re
from apps.core import validators
from django.utils.translation import gettext_lazy as _


class CleanPassword(forms.Form):
    def clean_password(self):
        """
        None
        Clean and validate the confirmation password field.
        Raises:
            forms.ValidationError: If the passwords don't match or if the password fails the specified criteria.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$"
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        elif not re.match(pattern, password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, one digit,"
                " and one special character.")
        elif ' ' in password:
            raise forms.ValidationError("Password cannot contain spaces.")

        return password


class UserPhoneNumberLoginForm(forms.Form):
    """Defines a form for user login using phone number, OTP code, and password.
    This form allows users to log in using their phone number, OTP code, and password.
    """
    phone_number = forms.CharField(label='Phone Number', max_length=11, validators=[validators.PhoneNumberValidator()],
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
        if ' ' in email:
            raise forms.ValidationError("Email address cannot contain spaces.")
        if user:
            return email


class CleanDataUserForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email'), max_length=100, validators=[validators.EmailValidator()],
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                          'focus:border-indigo-500 '
                                          'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    username = forms.CharField(label=_('Username'), max_length=100, validators=[validators.UsernameValidator()],
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                            'focus:border-indigo-500 '
                                            'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    phone_number = forms.CharField(label=_('Phone Number'), max_length=11,
                                   validators=[validators.PhoneNumberValidator()],
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                'focus:border-indigo-500 '
                                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
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
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
            'name': _('Name'),
            'last_name': _('Last Name'),
            'gender': _('Gender'),
            'age': _('Age'),
            # 'profile_picture': _('Profile Picture'),
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

    Attributes:
        name (CharField): The name of the user.
        last_name (CharField): The last name of the user.
        gender (ChoiceField): The gender of the user.
        age (IntegerField): The age of the user.
        profile_picture (ImageField): The profile picture of the user.
    """

    name = forms.CharField(label=_('Name'), max_length=50, validators=[validators.NameValidator()],
                           widget=forms.TextInput(attrs={
                               'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                        'focus:border-indigo-500 '
                                        'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    last_name = forms.CharField(label=_('Last Name'), max_length=50, validators=[validators.LastNameValidator()],
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                             'focus:border-indigo-500 '
                                             'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    gender = forms.ChoiceField(label=_('Gender'), choices=validators.GenderChoices.CHOICES,
                               validators=[validators.GenderValidator()],
                               widget=forms.Select(attrs={
                                   'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                            'focus:border-indigo-500 '
                                            'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    age = forms.IntegerField(label=_('Age'),
                             widget=forms.NumberInput(attrs={
                                 'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                          'focus:border-indigo-500 '
                                          'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    profile_picture = forms.ImageField(label=_('Profile Picture'), required=False,
                                       validators=[validators.PictureValidator()],
                                       widget=forms.FileInput(attrs={
                                           'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                    'focus:border-indigo-500 '
                                                    'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    class Meta:
        model = Profile
        fields = ['name', 'last_name', 'gender', 'age', 'profile_picture']
        labels = {
            'name': _('Name'),
            'last_name': _('Last Name'),
            'gender': _('Gender'),
            'age': _('Age'),
            'profile_picture': _('Profile Picture'),
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
        """
        Save the changes made in the form.

        Args:
            commit (bool, optional): Indicates whether to save the user to the database. Defaults to True.

        Returns:
            User: The user instance with the changes made in the form.
        """
        user = super(ProfileCreateForm, self).save(commit=False)
        if commit:
            user.save()
        return user


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


class UserChangeForm(forms.ModelForm):
    """
    This class defines a form for changing user information.

    Attributes:
        password (ReadOnlyPasswordHashField): Field for displaying password, with a link to change it.
    """

    password = ReadOnlyPasswordHashField(
        help_text="You can change using password <a href=\"../password\">this form</a>")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'username', 'password', 'last_login')
        labels = {
            'email': 'Email',
            'phone_number': 'Phone Number',
            'username': 'Username',
        }
        help_texts = {
            'email': 'Enter your email',
            'phone_number': 'Enter your phone number',
            'username': 'Enter your username',
        }
        error_messages = {
            'email': {
                'required': 'Email is required',
                'invalid': 'Invalid email format',
            },
            'phone_number': {
                'required': 'Phone number is required',
                'invalid': 'Invalid phone number format',
            },
            'username': {
                'required': 'Username is required',
                'invalid': 'Invalid username format'},
        }


class ChangePasswordForm(PasswordChangeForm):
    """
    This class defines a form for changing user password, extending the PasswordChangeForm.

    Methods:
        __init__: Constructor method to customize form field widgets.
        clean_new_password1: Custom validation method to check password similarity and additional rules.
    """

    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                 'focus:border-indigo-500 '
                 'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))  # noqa
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                 'focus:border-indigo-500 '
                 'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))  # noqa
    new_password2 = forms.CharField(label="Confirm New Password",
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


class CustomUserChangeForm(forms.ModelForm):
    """
    This class defines a custom user change form, extending the UserChangeForm.
    """
    email = forms.EmailField(label=_('Email'), max_length=100, validators=[validators.EmailValidator()],
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                          'focus:border-indigo-500 '
                                          'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    username = forms.CharField(label=_('Username'), max_length=100, validators=[validators.UsernameValidator()],
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                            'focus:border-indigo-500 '
                                            'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))
    phone_number = forms.CharField(label=_('Phone Number'), max_length=11,
                                   validators=[validators.PhoneNumberValidator()],
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                                                'focus:border-indigo-500 '
                                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}))

    class Meta:
        """
        Meta class to specify the model and fields for the form.
        """
        model = User
        fields = ['username', 'email', 'phone_number']

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


class CodeDiscountForm(forms.ModelForm):
    """
    Form for creating or updating discount codes.
    """

    class Meta:
        """
        Meta class to specify the model and fields for the form.
        """
        model = CodeDiscount
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 '
                         'focus:border-indigo-500 '
                         'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'percentage_discount': forms.Select(attrs={'class': 'form-select'}),
            'numerical_discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'code': _('Code'),
            'percentage_discount': _('Percentage Discount'),
            'numerical_discount': _('Numerical Discount'),
            'expiration_date': _('Expiration Date'),
        }
        help_texts = {
            'code': _('Enter the discount code.'),
            'percentage_discount': _('Select the percentage discount.'),
            'numerical_discount': _('Enter the numerical discount.'),
            'expiration_date': _('Select the expiration date for the code.'),
        }
        error_messages = {
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
            },
        }


class VerifyCodeForm(forms.Form):
    """
    This class defines a form for verifying a code.

    Methods:
        clean_code: Method to clean and validate the code field.

    """
    code = forms.IntegerField(label='Code', min_value=100000, max_value=999999,
                              widget=forms.NumberInput(attrs={'autocomplete': 'off'}))

    def clean_code(self):
        """
        Clean and validate the code field.

        Returns:
            int: Cleaned and validated code value.

        Raises:
            forms.ValidationError: If the code is not a 6-digit number.
        """
        code = self.cleaned_data['code']
        # if code < 10000 or code > 99999:
        #     raise forms.ValidationError("Code must be a 6-digit number.")
        return code
