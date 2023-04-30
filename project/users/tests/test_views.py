from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

CustomUser = get_user_model()


class SignupViewTest(TestCase):
    def test_signup_view_uses_correct_template(self):
        """
        Checks if the signup view uses the correct template (signup.html)
        """
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_signup_form_valid(self):
        """
        Checks if the signup form works correctly when provided
        with valid data. It posts the form data with a valid
        email and matching passwords, and checks if the user
        is redirected (status code 302) and if the user is
        created in the database.
        """
        response = self.client.post(reverse('users:signup'), {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(
            email='test@example.com').exists()
            )

    def test_signup_form_invalid(self):
        """
        Checks if the signup form displays an error message when provided with
        invalid data, such as non-matching passwords. It posts the form data
        with a valid email and non-matching passwords, and checks if the user
        is not created in the database and if the error message is displayed
        in the response.
        """
        response = self.client.post(reverse('users:signup'), {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(
            email='test@example.com').exists()
            )
        self.assertContains(response, 'The two password fields didn’t match.')

    def test_signup_form_email_already_exists(self):
        """
        Checks if the signup form displays an error message when
        the provided email already exists in the database.
        It creates a user with a specific email address,
        then posts the form data with the same email address
        and valid passwords, and checks if the error message
        is displayed in the response.
        """
        CustomUser.objects.create(
            email='test@example.com',
            password='testpassword123'
            )
        response = self.client.post(reverse('users:signup'), {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Custom user with this Email address already exists.'
            )
