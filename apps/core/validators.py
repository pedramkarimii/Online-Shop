from django.core import validators
from django.utils.translation import gettext_lazy as _


class CustomRegexValidator(validators.RegexValidator):
    """
    Custom RegexValidator with enhanced error messages
    """

    def __init__(self, regex, message):
        super().__init__(regex, message=message)


class CustomMinValueValidator(validators.MinValueValidator):
    """
    Custom validator for quantity field
    """

    def __init__(self, limit_value, message):
        super().__init__(
            limit_value=limit_value,
            message=message
        )


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


class StatusValidator(CustomRegexValidator):
    """
    Validator for the status field
    """

    def __init__(self):
        regex = r'^(paid|delivered|cancelled)$'
        message = _('Invalid status')
        super().__init__(regex=regex, message=message)


class CardNumberValidator(CustomRegexValidator):

    def __init__(self):
        regex = r'^\d{12}$'
        message = _('Enter a valid card number.')
        super().__init__(regex=regex, message=message)


class CVVValidator(CustomRegexValidator):
    message = _('Enter a valid 3 or 4-digit CVV.')

    def __init__(self):
        super().__init__(regex=r'^\d{3,4}$', message=self.message)


class QuantityValidators(CustomMinValueValidator):
    """
    Custom validator for quantity field
    """

    def __init__(self):
        super().__init__(
            limit_value=1,
            message=_('Quantity must be at least 1.')
        )


class FinallyPriceValidator(CustomMinValueValidator):
    message = _('Price must be non-negative.')

    def __init__(self):
        super().__init__(0, message=self.message)


class AmountValidator(CustomMinValueValidator):
    message = _('Amount must be non-negative.')

    def __init__(self):
        super().__init__(0, message=self.message)


class CardholderNameValidator(CustomMinValueValidator):
    message = _('Cardholder name must be at least 3 characters.')

    def __init__(self):
        super().__init__(3, message=self.message)


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


class PictureValidator(validators.FileExtensionValidator):
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


class SizeValidator(CustomRegexValidator):
    """
    Validator for size field
    """

    def __init__(self):
        super().__init__(
            regex=r'^(S|M|L|XL|XXL|XXXL|XXXXL)$',
            message='Invalid size. Please select a valid size.'
        )


class MaterialValidator(CustomRegexValidator):
    """
    Validator for material field
    """

    def __init__(self):
        super().__init__(
            regex=r'^(WOOD|METAL|PLASTIC|GLASS|FIBER|LEATHER|TEXTILE|RUBBER|OTHER)$',
            message='Invalid material. Please select a valid material.'
        )


class WarrantyValidator(CustomRegexValidator):
    """
    Validator for warranty field
    """

    def __init__(self):
        super().__init__(
            regex=r'^(1|2|3|4|5)$',
            message='Invalid warranty. Please select a valid warranty.'
        )


class ColorValidator(CustomRegexValidator):
    """
    Validator for color field
    """

    def __init__(self):
        super().__init__(
            regex=r'^(RED|GREEN|BLUE|YELLOW|PURPLE|ORANGE|BLACK|WHITE|GRAY|BROWN|PINK|GOLD|SILVER)$',
            message='Invalid color. Please select a valid color.'
        )


class PercentageDiscountValidator(CustomMinValueValidator):
    """
    Validator for percentage discount field
    """

    def __init__(self):
        super().__init__(
            limit_value=0,
            message='Percentage discount cannot be negative.'
        )


class PriceValidator(CustomMinValueValidator):
    """
    Validator for price field
    """

    def __init__(self):
        super().__init__(
            limit_value=0,
            message='Price must be a non-negative value.'
        )


class PercentageDiscountValidator(CustomMinValueValidator):
    """
    Validator for percentage discount field
    """

    def __init__(self):
        super().__init__(
            limit_value=0,
            message='Percentage discount cannot be negative.'
        )


class NumericalDiscountValidator(CustomMinValueValidator):
    """
    Validator for numerical discount field
    """

    def __init__(self):
        super().__init__(
            limit_value=0,
            message='Numerical discount cannot be negative.'
        )


class NumericalDiscountValidator(CustomMinValueValidator):
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


class OtpCodeValidator(CustomRegexValidator):
    """
    Validator for OTP code field
    """

    def __init__(self):
        super().__init__(
            regex=r'^\d{6}$',  # Regular expression to match exactly 6 digits
            message='OTP code must be exactly 6 digits long.',
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


class StatusChoice:
    PAID = 'paid'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    CHOICES = (
        (PAID, _('Paid')),
        (DELIVERED, _('Delivered')),
        (CANCELLED, _('Cancelled')),
    )


class PaymentMethodChoice:
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    PAYPAL = 'paypal'
    BANK_TRANSFER = 'bank_transfer'
    CASH = 'cash'

    CHOICES = (
        (CREDIT_CARD, _('Credit Card')),
        (DEBIT_CARD, _('Debit Card')),
        (PAYPAL, _('PayPal')),
        (BANK_TRANSFER, _('Bank Transfer')),
        (CASH, _('Cash')),
    )


class SizeChoice:
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    XXL = 'XXL'
    XXXL = 'XXXL'
    XXXXL = 'XXXXL'

    CHOICES = (
        (S, _('Small')),
        (M, _('Medium')),
        (L, _('Large')),
        (XL, _('Extra Large')),
        (XXL, _('Extra Extra Large')),
        (XXXL, _('Extra Extra Extra Large')),
        (XXXXL, _('Extra Extra Extra Extra Large')),
    )


class ColorChoice:
    RED = 'RED'
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    YELLOW = 'YELLOW'
    PURPLE = 'PURPLE'
    ORANGE = 'ORANGE'
    BLACK = 'BLACK'
    WHITE = 'WHITE'
    GRAY = 'GRAY'
    BROWN = 'BROWN'
    PINK = 'PINK'
    GOLD = 'GOLD'
    SILVER = 'SILVER'

    CHOICES = (
        (RED, _('Red')),
        (GREEN, _('Green')),
        (BLUE, _('Blue')),
        (YELLOW, _('Yellow')),
        (PURPLE, _('Purple')),
        (ORANGE, _('Orange')),
        (BLACK, _('Black')),
        (WHITE, _('White')),
        (GRAY, _('Gray')),
        (BROWN, _('Brown')),
        (PINK, _('Pink')),
        (GOLD, _('Gold')),
        (SILVER, _('Silver')),
    )


class MaterialChoice:
    WOOD = 'WOOD'
    METAL = 'METAL'
    PLASTIC = 'PLASTIC'
    GLASS = 'GLASS'
    FIBER = 'FIBER'
    LEATHER = 'LEATHER'
    TEXTILE = 'TEXTILE'
    RUBBER = 'RUBBER'
    OTHER = 'OTHER'

    CHOICES = (
        (WOOD, _('Wood')),
        (METAL, _('Metal')),
        (PLASTIC, _('Plastic')),
        (GLASS, _('Glass')),
        (FIBER, _('Fiber')),
        (LEATHER, _('Leather')),
        (TEXTILE, _('Textile')),
        (RUBBER, _('Rubber')),
        (OTHER, _('Other')),
    )


class WarrantyChoice:
    ONE_YEAR = '1'
    TWO_YEARS = '2'
    THREE_YEARS = '3'
    FOUR_YEARS = '4'
    FIVE_YEARS = '5'

    CHOICES = (
        (ONE_YEAR, _('1 Year')),
        (TWO_YEARS, _('2 Years')),
        (THREE_YEARS, _('3 Years')),
        (FOUR_YEARS, _('4 Years')),
        (FIVE_YEARS, _('5 Years')),
    )
