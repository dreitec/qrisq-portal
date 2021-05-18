from django.core.validators import RegexValidator


CARD_VALIDATOR = RegexValidator(r'(\d{14,16})', 'Only numeric characters or Invalid Card Number')

CVC_VALIDATOR = RegexValidator(r'(\d{3,4})', 'Only numeric characters')

DATE_VALIDATOR = RegexValidator(r'^((0?[1-9]|[1][0-2])\/\d{2})', 'Invalid Expiration date format')

NUMERIC_VALIDATOR = RegexValidator(r'^[0-9]*$', 'Only numeric characters')
