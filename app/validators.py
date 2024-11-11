from django.core.validators import RegexValidator

"""
This regex assumes that you have a clean string,
you should clean the string for spaces and other characters
"""

IsAlphaValidator = RegexValidator(
    "^[A-Za-z]+$", message="Alpha characters only.", code="Invalid value"
)
IsAlphaWithSpaceValidator = RegexValidator(
    "^[A-Za-z ]+$", message="Alphabets and space characters only.", code="Invalid value"
)
IsAlphaWithHyphenValidator = RegexValidator(
    "^[A-Za-z-]+$",
    message="Alphabets and hyphen characters only.",
    code="Invalid value",
)
IsAlphaNumericValidator = RegexValidator(
    "^[A-Za-z0-9]+$", message="Alphanumeric characters only.", code="Invalid value"
)
IsAlphaNumericWithSpaceValidator = RegexValidator(
    "^[A-Za-z0-9 ]+$",
    message="Alphanumeric and space characters only.",
    code="Invalid value",
)
IsAlphaNumericWithHyphenDotValidator = RegexValidator(
    "^[A-Za-z0-9.-]+$",
    message="Alphanumeric, dot and hyphen characters only.",
    code="Invalid value",
)
IsNumericValidator = RegexValidator(
    "^[0-9]+$", message="Numeric characters only.", code="Invalid value"
)
IsWholeNumericValidator = RegexValidator(
    "^[0-9-]+$", message="Numeric characters only.", code="Invalid value"
)
IsDecimalValidator = RegexValidator(
    "^[0-9.]+$", message="Decimal numeric characters only.", code="Invalid value"
)
IsWholeDecimalValidator = RegexValidator(
    "^[0-9.-]+$", message="Decimal numeric characters only.", code="Invalid value"
)
IsDataValidator = RegexValidator(
    "^[A-Za-z0-9-!$%^&*()_+|~={}[:;<>?,.@#\\'\" ]+$",
    message="Alphanumeric characters only.",
    code="Invalid value",
)

# custom validators
IsNameValidator = RegexValidator(
    "^[A-Za-z0-9 ,.'-]+$", message="Alphanumeric characters only.", code="Invalid value"
)
IsPhoneNumberValidator = RegexValidator(
    regex="^\+?1?\d{9,15}$", message="Enter a valid phone number. It should be between 9 and 15 digits and can start with a plus sign (+).", code="Invalid value"
)
IsLatitudeValidator = RegexValidator(
    "^(\+|-)?((\d((\.)|\.\d{1,6})?)|(0*?[0-8]\d((\.)|\.\d{1,6})?)|(0*?90((\.)|\.0{1,6})?))$",
    message="Latitude must be a number between -90 and 90",
    code="Invalid value",
)
IsLongitudeValidator = RegexValidator(
    "^(\+|-)?((\d((\.)|\.\d{1,6})?)|(0*?\d\d((\.)|\.\d{1,6})?)|(0*?1[0-7]\d((\.)|\.\d{1,6})?)|(0*?180((\.)|\.0{1,6})?))$",
    message="Longitude must a number between -180 and 180",
    code="Invalid value",
)
