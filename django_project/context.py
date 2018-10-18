from .models import Price
#recent_price

def recent_price(request):
    return dict(recent_snippets=Price.objects.order_by("-id").all()[:8])