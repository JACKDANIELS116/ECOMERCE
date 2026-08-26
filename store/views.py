from decimal import Decimal

from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

PRODUCTS = {
    "ember-lime": {
        "name": "Ember Lime", "category": "Energizante", "price": Decimal("8.50"),
        "description": "Cítrico, brillante y con un final ligeramente ahumado.",
        "image": "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?auto=format&fit=crop&w=900&q=85",
        "tone": "lime",
    },
    "midnight-berry": {
        "name": "Midnight Berry", "category": "Energizante", "price": Decimal("9.25"),
        "description": "Frutos oscuros, notas florales y energía limpia.",
        "image": "https://images.unsplash.com/photo-1581636625402-29b2a704ef13?auto=format&fit=crop&w=900&q=85",
        "tone": "berry",
    },
    "saffron-cloud": {
        "name": "Saffron Cloud", "category": "Té exótico", "price": Decimal("12.00"),
        "description": "Azafrán, vainilla y té blanco de hoja completa.",
        "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=900&q=85",
        "tone": "saffron",
    },
    "jasmine-smoke": {
        "name": "Jasmine Smoke", "category": "Té exótico", "price": Decimal("11.50"),
        "description": "Jazmín sedoso con una profundidad tostada y elegante.",
        "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=900&q=85",
        "tone": "smoke",
    },
}


def _cart_items(request):
    cart_data = request.session.get("cart", {})
    items = []
    total = Decimal("0")
    count = 0
    for product_id, quantity in cart_data.items():
        product = PRODUCTS.get(product_id)
        if not product:
            continue
        quantity = int(quantity)
        line_total = product["price"] * quantity
        items.append({"id": product_id, "product": product, "quantity": quantity, "line_total": line_total})
        total += line_total
        count += quantity
    return items, total, count


def _change_quantity(request, product_id, amount):
    cart_data = request.session.get("cart", {})
    current = int(cart_data.get(product_id, 0))
    updated = current + amount
    if updated > 0 and product_id in PRODUCTS:
        cart_data[product_id] = updated
    else:
        cart_data.pop(product_id, None)
    request.session["cart"] = cart_data
    request.session.modified = True


def index(request):
    featured = list(PRODUCTS.values())[:3]
    _, _, count = _cart_items(request)
    return render(request, "store/index.html", {"featured": featured, "cart_count": count})


def catalog(request):
    _, _, count = _cart_items(request)
    return render(request, "store/catalogo2.html", {"products": PRODUCTS.items(), "cart_count": count})


def cart(request):
    items, total, count = _cart_items(request)
    return render(request, "store/cart.html", {"items": items, "total": total, "cart_count": count})


@require_POST
def add_to_cart(request, product_id):
    _change_quantity(request, product_id, 1)
    return redirect("cart")


@require_POST
def increase_quantity(request, product_id):
    _change_quantity(request, product_id, 1)
    return redirect("cart")


@require_POST
def decrease_quantity(request, product_id):
    _change_quantity(request, product_id, -1)
    return redirect("cart")


@require_POST
def remove_from_cart(request, product_id):
    cart_data = request.session.get("cart", {})
    cart_data.pop(product_id, None)
    request.session["cart"] = cart_data
    request.session.modified = True
    return redirect("cart")


def checkout(request):
    items, total, count = _cart_items(request)
    if not items:
        return redirect("catalog")
    return render(request, "store/checkout.html", {"items": items, "total": total, "cart_count": count})


@require_POST
def confirm_order(request):
    items, total, _ = _cart_items(request)
    if not items:
        return redirect("catalog")
    request.session["cart"] = {}
    request.session["last_order_total"] = str(total)
    request.session.modified = True
    return render(request, "store/success.html", {"total": total})
