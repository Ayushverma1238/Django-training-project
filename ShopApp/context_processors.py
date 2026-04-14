from .models import Wishlist, CartItem

def global_counts(request):
    if request.user.is_authenticated:
        return {
            "wishlist_count": Wishlist.objects.filter(user=request.user).count(),

            # ✅ FIX HERE
            "cart_count": CartItem.objects.filter(cart__user=request.user).count(),
        }

    return {
        "wishlist_count": 0,
        "cart_count": 0,
    }