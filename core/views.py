from django.http import HttpResponse
from events.models import Show

def home(request):
    shows = Show.objects.filter(is_active=True).order_by("start_at")
    if not shows.exists():
        return HttpResponse("No hay funciones activas todavía.")

    lines = ["🎪 Funciones activas:\n"]
    for s in shows:
        lines.append(f"- {s.event.title} @ {s.venue_name} | {s.start_at:%Y-%m-%d %H:%M}")
    return HttpResponse("\n".join(lines))


# Create your views here.
