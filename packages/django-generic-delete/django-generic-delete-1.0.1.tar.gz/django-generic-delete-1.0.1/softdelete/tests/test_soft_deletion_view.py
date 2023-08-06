from django.test import TestCase, Client
from django.urls import reverse
from .models import TestModel


class AdminSingleDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.model = TestModel.objects.create(title='test')
        self.model2 = TestModel.objects.create(title='test2')
        pks = str(self.model.id) + ',' + str(self.model2.id)
        self.url = reverse('softdelete:single-delete', args=['tests', 'TestModel', pks]) + '?next=/test/'

    def test_it_returns_200_status_code(self):
        """Test the request returns with status code 200 OK"""
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_it_uses_translate_template_in_GET_request(self):
        """ test template used is component/delete_view/delete_confirmation.html """
        self.response = self.client.get(self.url)
        self.assertTemplateUsed(self.response, "softdelete/delete_confirmation.html")

    def test_context_has_next_in_GET_request(self):
        """Test that context has next url"""
        self.response = self.client.get(self.url)
        self.assertIn('next', self.response.context)

    def test_it_throws_exception_if_next_is_not_in_url(self):
        """Test that it throws exception when next route dont exist in url"""
        with self.assertRaises(KeyError) as context:
            self.response = self.client.get(reverse('softdelete:single-delete', args=['tests', 'TestModel', 1]))
        self.assertTrue("key next must be included in request" in str(context.exception))

    def test_post_request_returns_302_status_code(self):
        """Test that it return status code 302 when delete object"""
        self.response = self.client.post(self.url)
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_to_next_after_delete(self):
        """Test that it redirect to next url after delete"""
        self.response = self.client.post(self.url)
        self.assertEqual(self.response.url, '/test/')

    def test_delete_object(self):
        """Test that object deleted successfully from database"""
        self.response = self.client.post(self.url)
        self.assertNotIn(self.model, TestModel.objects.all())

    def test_it_delete_all_values_in_the_database(self):
        self.assertNotEqual(0, TestModel.objects.all().count())
        self.response = self.client.post(self.url)
        self.assertEqual(0, TestModel.objects.all().count())
