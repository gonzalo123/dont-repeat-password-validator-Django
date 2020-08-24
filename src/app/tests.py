from django.core.exceptions import ValidationError
from django.test import TestCase
from app.models import CustomUser as User
from app.models import CustomUserPasswordHistory
from app.validators import DontRepeatValidator


class UserCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='gonzalo')

    def test_persist_password_to_history(self):
        self.user.set_password('pass1')
        self.user.save()

        all_history_user_passwords = CustomUserPasswordHistory.objects.filter(username_id=self.user)
        self.assertEqual(1, all_history_user_passwords.count())


class DontRepeatValidatorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='gonzalo')
        self.validator = DontRepeatValidator()

    def test_validator_with_new_pass(self):
        self.validator.validate('pass33', self.user)
        self.assertTrue(True)

    def test_validator_with_repeated_pass(self):
        for i in range(0, 11):
            self.user.set_password(f'pass{i}')
            self.user.save()

        with self.assertRaises(ValidationError):
            self.validator.validate('pass3', self.user)

    def test_keep_only_10_passwords(self):
        for i in range(0, 11):

            self.user.set_password(f'pass{i}')
            self.user.save()

        self.validator.validate('xxxx', self.user)

        all_history_user_passwords = CustomUserPasswordHistory.objects.filter(username_id=self.user)
        self.assertEqual(10, all_history_user_passwords.count())
