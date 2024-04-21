from django.core import validators
from django.utils.translation import gettext_lazy as _


# Define your custom validators
class CustomRegexValidator(validators.RegexValidator):
    """
    Custom RegexValidator with enhanced error messages
    """

    def __init__(self, regex, message):
        super().__init__(regex, message=message)


class UsernameValidator(CustomRegexValidator):
    """
    Validator for username field
    """

    def __init__(self):
        super().__init__(
            r'^[a-zA-Z0-9_.+-]+$',
            _('Username can contain letters, numbers, underscores, dots, '
              'hyphens, and must be at least 4 characters long.')
        )


class EmailValidator(CustomRegexValidator):
    """
    Validator for email field
    """

    def __init__(self):
        super().__init__(
            r'^[a-zA-Z0-9._%+-]+@(?:gmail|yahoo)\.com$',
            _('Please enter a valid Gmail or Yahoo email address.')
        )


class PhoneNumberValidator(CustomRegexValidator):
    """
    Validator for phone number field
    """

    def __init__(self):
        super().__init__(
            r"09(1[0-9]|3[0-9]|2[0-9]|0[1-9]|9[0-9])[0-9]{7}$",
            _('Please enter a valid phone number in the format 09121234567.')
        )


class NameValidator(CustomRegexValidator):
    """
    Validator for name field
    """

    def __init__(self):
        super().__init__(
            r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message=_('Enter a valid name.')
        )


class LastNameValidator(CustomRegexValidator):
    """
    Validator for last name field
    """

    def __init__(self):
        super().__init__(
            r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message=_('Enter a valid last name.')
        )


class GenderValidator(validators.BaseValidator):
    """
    Validator for gender field
    """

    def __init__(self):
        super().__init__(
            limit_value=None,
            message=_('Enter a valid gender (Male, Female, Other).'),
        )

    def __call__(self, value):
        if value not in ['Male', 'Female', 'Other']:
            raise validators.ValidationError(
                self.message,
                code=self.code
            )


class ProfilePictureValidator(validators.FileExtensionValidator):
    """
    Validator for profile picture field
    """

    def __init__(self):
        super().__init__(
            allowed_extensions=['jpg', 'jpeg', 'png'],
            message=_('Only JPG, JPEG, and PNG files are allowed.')
        )


class CountryValidator(CustomRegexValidator):
    """
    Validator for country field
    """

    def __init__(self):
        super().__init__(
            regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message='Enter a valid country name.'
        )


class CityValidator(CustomRegexValidator):
    """
    Validator for city field
    """

    def __init__(self):
        super().__init__(
            regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message='Enter a valid city name.'
        )


class StreetValidator(CustomRegexValidator):
    """
    Validator for street field
    """

    def __init__(self):
        super().__init__(
            regex=r'^[a-zA-Z0-9\s.,#-]+$',
            message='Enter a valid street address.'
        )


class BuildingNumberValidator(CustomRegexValidator):
    """
    Validator for building number field
    """

    def __init__(self):
        super().__init__(
            regex=r'^[a-zA-Z0-9\s-]+$',
            message='Enter a valid building number.'
        )


class FloorNumberValidator(CustomRegexValidator):
    """
    Validator for floor number field
    """

    def __init__(self):
        super().__init__(
            regex=r'^[a-zA-Z0-9\s-]+$',
            message='Enter a valid floor number.'
        )


class PostalCodeValidator(CustomRegexValidator):
    """
    Validator for postal code field
    """

    def __init__(self):
        super().__init__(
            regex=r'^[a-zA-Z0-9\s-]+$',
            message='Enter a valid postal code.'
        )


class NotesValidator(CustomRegexValidator):
    """
    Validator for notes field
    """

    def __init__(self):
        super().__init__(
            regex=r'^[a-zA-Z0-9\s.,#-]+$',
            message='Enter valid notes.'
        )


class CodeValidator(CustomRegexValidator):
    """
    Validator for code field
    """

    def __init__(self):
        super().__init__(
            regex=r'^[a-zA-Z0-9]+$',
            message='Enter a valid code.'
        )


class PercentageDiscountValidator(validators.MinValueValidator):
    """
    Validator for percentage discount field
    """

    def __init__(self):
        super().__init__(
            limit_value=0,
            message='Percentage discount cannot be negative.'
        )


class NumericalDiscountValidator(validators.MinValueValidator):
    """
    Validator for numerical discount field
    """

    def __init__(self):
        super().__init__(
            limit_value=0,
            message='Numerical discount cannot be negative.'
        )


class PasswordValidator(CustomRegexValidator):
    """
    Validator for password field
    """

    def __init__(self):
        super().__init__(
            regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$",
            message='Password must contain at least one lowercase letter, one uppercase letter, one digit, '
                    'one special character, and be at least 8 characters long.'
        )


class OtpCodeValidator(validators.RegexValidator):
    """
    Validator for OTP code field
    """

    def __init__(self):
        super().__init__(
            regex=r'^\d{6}$',  # Regular expression to match exactly 6 digits
            message='OTP code must be exactly 6 digits long.',
            code='invalid_otp_code'
        )


class GenderChoices:
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'

    CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (OTHER, _('Other'))
    )


class CountryChoices:
    IRAN = 'Iran'

    CHOICES = (
        (IRAN, _('Iran')),
    )


class CityChoices:
    TEHRAN = 'Tehran'
    SHIRAZ = 'Shiraz'
    MASHHAD = 'Mashhad'
    TABRIZ = 'Tabriz'
    ISFAHAN = 'Isfahan'
    KISH = 'Kish'
    KERMAN = 'Kerman'
    ZAHEDAN = 'Zahedan'
    FARS = 'Fars'
    SEMNAN = 'Semnan'
    YAZD = 'Yazd'
    QOM = 'Qom'
    AHVAZ = 'Ahvaz'
    GILAN = 'Gilan'
    KHORASAN = 'Khorasan'
    KERMANSHAH = 'Kermanshah'
    KOHGILUYEH_BOYERAHMAD = 'Kohgiluyeh and BoyerAhmad'
    LORESTAN = 'Lorestan'
    MAZANDARAN = 'Mazandaran'
    MARKAZI = 'Markazi'
    HORMOZGAN = 'Hormozgan'
    HAMADAN = 'Hamadan'
    ARDABIL = 'Ardabil'
    ZANJAN = 'Zanjan'
    QAZVIN = 'Qazvin'
    KURDISTAN = 'Kurdistan'

    CHOICES = (
        (TEHRAN, _('Tehran')),
        (SHIRAZ, _('Shiraz')),
        (MASHHAD, _('Mashhad')),
        (TABRIZ, _('Tabriz')),
        (ISFAHAN, _('Isfahan')),
        (KISH, _('Kish')),
        (KERMAN, _('Kerman')),
        (ZAHEDAN, _('Zahedan')),
        (FARS, _('Fars')),
        (SEMNAN, _('Semnan')),
        (YAZD, _('Yazd')),
        (QOM, _('Qom')),
        (AHVAZ, _('Ahvaz')),
        (GILAN, _('Gilan')),
        (KHORASAN, _('Khorasan')),
        (KERMANSHAH, _('Kermanshah')),
        (KOHGILUYEH_BOYERAHMAD, _('Kohgiluyeh and BoyerAhmad')),
        (LORESTAN, _('Lorestan')),
        (MAZANDARAN, _('Mazandaran')),
        (MARKAZI, _('Markazi')),
        (HORMOZGAN, _('Hormozgan')),
        (HAMADAN, _('Hamadan')),
        (ARDABIL, _('Ardabil')),
        (ZANJAN, _('Zanjan')),
        (QAZVIN, _('Qazvin')),
        (KURDISTAN, _('Kurdistan')),
    )


class PercentDiscountChoices:
    FIVE_PERCENT = 5
    TEN_PERCENT = 10
    FIFTEEN_PERCENT = 15
    TWENTY_PERCENT = 20
    TWENTY_FIVE_PERCENT = 25
    THIRTY_PERCENT = 30
    THIRTY_FIVE_PERCENT = 35
    FORTY_PERCENT = 40
    FORTY_FIVE_PERCENT = 45
    FIFTY_PERCENT = 50
    FIFTY_FIVE_PERCENT = 55
    SIXTY_PERCENT = 60

    CHOICES = (
        (FIVE_PERCENT, _('5%')),
        (TEN_PERCENT, _('10%')),
        (FIFTEEN_PERCENT, _('15%')),
        (TWENTY_PERCENT, _('20%')),
        (TWENTY_FIVE_PERCENT, _('25%')),
        (THIRTY_PERCENT, _('30%')),
        (THIRTY_FIVE_PERCENT, _('35%')),
        (FORTY_PERCENT, _('40%')),
        (FORTY_FIVE_PERCENT, _('45%')),
        (FIFTY_PERCENT, _('50%')),
        (FIFTY_FIVE_PERCENT, _('55%')),
        (SIXTY_PERCENT, _('60%'))
    )
