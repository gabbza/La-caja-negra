from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from venues.models import Venue, Seat
from .models import Show, ShowSeat

HOLD_MINUTES = 10
PRICE_PER_SEAT = 80.00


def show_detail(request, show_id):
    show = get_object_or_404(Show, pk=show_id, is_active=True)
    venue = Venue.objects.filter(name=show.venue_name).first() or Venue.objects.first()
    if not venue:
        return render(request, "events/show_detail.html", {"show": show, "error": "No hay foros configurados."})

    seats = Seat.objects.filter(venue=venue)
    if not seats.exists():
        return render(request, "events/show_detail.html", {"show": show, "error": "No hay asientos configurados."})

    existing_ids = set(
        ShowSeat.objects.filter(show=show, seat__venue=venue).values_list("seat_id", flat=True)
    )
    missing_seats = [s for s in seats if s.id not in existing_ids]
    if missing_seats:
        ShowSeat.objects.bulk_create([ShowSeat(show=show, seat=s) for s in missing_seats], ignore_conflicts=True)

    now = timezone.now()
    ShowSeat.objects.filter(show=show, status=ShowSeat.Status.HELD, held_until__lte=now).update(
        status=ShowSeat.Status.AVAILABLE,
        held_by=None,
        held_until=None,
    )

    show_seats = ShowSeat.objects.filter(show=show, seat__venue=venue).select_related("seat")

    error = None
    if request.method == "POST":
        seat_ids = request.POST.getlist("seat_ids")
        if not seat_ids:
            error = "Selecciona al menos un asiento."
        else:
            available = show_seats.filter(seat_id__in=seat_ids, status=ShowSeat.Status.AVAILABLE)
            if available.count() != len(seat_ids):
                error = "Uno o más asientos ya no están disponibles."
            else:
                hold_until = now + timedelta(minutes=HOLD_MINUTES)
                available.update(
                    status=ShowSeat.Status.HELD,
                    held_by=request.user if request.user.is_authenticated else None,
                    held_until=hold_until,
                )
                request.session[f"held_seats_{show.id}"] = [int(sid) for sid in seat_ids]
                return redirect("checkout", show_id=show.id)

    context = {
        "show": show,
        "venue": venue,
        "show_seats": show_seats,
        "hold_minutes": HOLD_MINUTES,
        "error": error,
    }
    return render(request, "events/show_detail.html", context)


def checkout(request, show_id):
    show = get_object_or_404(Show, pk=show_id, is_active=True)
    key = f"held_seats_{show.id}"
    seat_ids = request.session.get(key, [])

    now = timezone.now()
    ShowSeat.objects.filter(show=show, status=ShowSeat.Status.HELD, held_until__lte=now).update(
        status=ShowSeat.Status.AVAILABLE,
        held_by=None,
        held_until=None,
    )

    held_qs = ShowSeat.objects.filter(show=show, seat_id__in=seat_ids, status=ShowSeat.Status.HELD).select_related("seat")
    if not held_qs.exists():
        return render(request, "events/checkout.html", {"show": show, "error": "No tienes asientos apartados."})

    if request.method == "POST":
        if held_qs.filter(held_until__lte=now).exists():
            return render(request, "events/checkout.html", {"show": show, "error": "Tus asientos expiraron."})
        held_qs.update(
            status=ShowSeat.Status.SOLD,
            held_by=request.user if request.user.is_authenticated else None,
            held_until=None,
        )
        if key in request.session:
            del request.session[key]
        return redirect("checkout_success", show_id=show.id)

    total = float(len(seat_ids)) * PRICE_PER_SEAT
    context = {
        "show": show,
        "held_seats": held_qs,
        "total": total,
        "price_per_seat": PRICE_PER_SEAT,
    }
    return render(request, "events/checkout.html", context)


def checkout_success(request, show_id):
    show = get_object_or_404(Show, pk=show_id, is_active=True)
    return render(request, "events/checkout_success.html", {"show": show})
