from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

CustomUser = get_user_model()


class CustomUserTestCase(TestCase):
    def test_create_user(self):
        email = "test@example.com"
        password = "testpassword"
        new_user = CustomUser.objects.create_user(
                    email=email, password=password)
        self.assertEqual(new_user.email, email)
        self.assertTrue(new_user.check_password(password))
        self.assertFalse(new_user.is_staff)
        self.assertTrue(new_user.is_active)
        self.assertTrue(new_user.date_joined <= timezone.now())

    def test_create_superuser(self):
        email = "admin@example.com"
        password = "adminpassword"
        new_user = CustomUser.objects.create_superuser(
                                    email=email,
                                    password=password)

        self.assertEqual(new_user.email, email)
        self.assertTrue(new_user.check_password(password))
        self.assertTrue(new_user.is_staff)
        self.assertTrue(new_user.is_active)
        self.assertTrue(new_user.date_joined <= timezone.now())
