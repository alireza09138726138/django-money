from .models import Snippet,Pos
#recent_price

def recent_snippet(request):
    return dict(recent_snippet=Snippet.objects.order_by("-id")[:8])
	
	