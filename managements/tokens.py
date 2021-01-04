from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, rentmanage, timestamp):
        return (six.text_type(rentmanage.pk) + six.text_type(timestamp)) +  six.text_type(rentmanage.active)

account_activation_token = AccountActivationTokenGenerator()