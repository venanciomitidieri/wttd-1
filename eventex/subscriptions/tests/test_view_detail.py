from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Elaine Okada',
            cpf='12345678901',
            email='3l41n3@gmail.com',
            phone='11-12345-1234'
        )
        masked_id = self.obj.pk  ^ 0xABCDEFAB

        self.resp = self.client.get('/inscricao/{}/'.format(masked_id))


    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (self.obj.name,
                    self.obj.cpf,
                    self.obj.email,
                    self.obj.phone)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get('/inscricao/0/')
        self.assertEqual(404, resp.status_code)