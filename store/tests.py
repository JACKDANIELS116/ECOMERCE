from django.test import TestCase
from django.urls import reverse


class ShoppingFlowTests(TestCase):
    def test_cart_starts_empty(self):
        response = self.client.get(reverse("cart"))
        self.assertContains(response, "Aquí todavía")
        self.assertEqual(response.context["cart_count"], 0)

    def test_add_update_checkout_and_confirm_order(self):
        self.client.post(reverse("add_to_cart", args=["ember-lime"]))
        self.client.post(reverse("increase_quantity", args=["ember-lime"]))
        response = self.client.get(reverse("cart"))
        self.assertContains(response, "$17,00")
        self.assertContains(response, "2")

        checkout = self.client.get(reverse("checkout"))
        self.assertContains(checkout, "Ember Lime")
        self.client.post(reverse("confirm_order"), {"payment": "card"})
        self.assertEqual(self.client.session.get("cart"), {})
        self.assertRedirects(self.client.get(reverse("checkout")), reverse("catalog"))

    def test_remove_product(self):
        self.client.post(reverse("add_to_cart", args=["midnight-berry"]))
        self.client.post(reverse("remove_from_cart", args=["midnight-berry"]))
        self.assertEqual(self.client.session.get("cart"), {})
