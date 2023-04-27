from django.test import TestCase

# Create your tests here.


from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        """
        Test creating a new user with the default User model.

        It creates a user with email and password, and checks that the email is
        correctly set, and the user is active, not staff nor superuser.
        Then it asserts that the username is None (for AbstractUser) or not
        present (for AbstractBaseUser).
        Finally, it tests that TypeError and ValueError are raised when calling
        create_user with invalid arguments.
        """
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        """
        Test creating a superuser.

        Creates a superuser with the given email and password using the Django
        authentication framework's create_superuser method. Asserts that the email
        and boolean flags for active, staff, and superuser status are all set
        correctly, and that the username (which may not exist depending on the user
        model) is None. Also asserts that creating a superuser with the same email
        and password but is_superuser=False raises a ValueError.
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)
            