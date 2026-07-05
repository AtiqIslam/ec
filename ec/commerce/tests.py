from django.test import TestCase
from django.urls import reverse
from .models import Order


class CartFlowTests(TestCase):
    def setUp(self):
        self.valid_checkout_data = {
            "customer_name": "Rahim Uddin",
            "phone_number": "01712345678",
            "district": "Dhaka",
            "thana": "Mirpur",
            "address": "House 12, Road 5, Mirpur DOHS",
        }

    def test_add_to_cart_updates_session(self):
        response = self.client.post(reverse("add_to_cart", args=["panjabi-1"]))

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.client.session["cart"]["panjabi-1"], 1)

    def test_home_search_filters_products(self):
        response = self.client.get(reverse("home"), {"q": "Black"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Elegant Black Panjabi")
        self.assertNotContains(response, "Classic Eid Panjabi")
        self.assertContains(response, 'Search Results for "Black"')

    def test_checkout_and_confirm_order_flow(self):
        self.client.post(reverse("add_to_cart", args=["panjabi-1"]))
        cart_response = self.client.get(reverse("cart"))
        checkout_response = self.client.get(reverse("checkout"))
        confirm_response = self.client.post(reverse("confirm_order"), self.valid_checkout_data)

        self.assertContains(cart_response, "Checkout")
        self.assertContains(checkout_response, "Confirm Order")
        self.assertContains(confirm_response, "Order Confirmed")
        self.assertEqual(Order.objects.count(), 1)
        self.assertTrue(Order.objects.first().order_number.startswith("ORD-"))
        self.assertEqual(Order.objects.first().customer_name, "Rahim Uddin")
        self.assertEqual(Order.objects.first().phone_number, "01712345678")
        self.assertEqual(Order.objects.first().district, "Dhaka")
        self.assertEqual(Order.objects.first().thana, "Mirpur")
        self.assertEqual(Order.objects.first().address, "House 12, Road 5, Mirpur DOHS")
        self.assertContains(confirm_response, Order.objects.first().order_number)
        self.assertEqual(self.client.session["cart"], {})

    def test_checkout_requires_delivery_fields(self):
        self.client.post(reverse("add_to_cart", args=["panjabi-1"]))
        response = self.client.post(reverse("confirm_order"), {})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertEqual(Order.objects.count(), 0)
