from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from events.models import Show
from .models import UserProfile


# HOME (requiere login)
@login_required(login_url="login")
def home(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.role:
        return redirect("choose_role")
    shows = Show.objects.filter(is_active=True).order_by("start_at")
    return render(request, "core/home.html", {"shows": shows})


# SIGNUP (registro público)
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # login automático
            return redirect("choose_role")
    else:
        form = UserCreationForm()

    return render(request, "core/signup.html", {"form": form})


# ELEGIR ROL
@login_required(login_url="login")
def choose_role(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # si ya eligió rol, no volver a mostrar
    if profile.role:
        return redirect("home")

    if request.method == "POST":
        role = request.POST.get("role")
        if role in ("PARTICIPANT", "BUYER"):
            profile.role = role
            profile.save()
            return redirect("home")

        return render(
            request,
            "core/choose_role.html",
            {"error": "Elige una opción válida."},
        )

    return render(request, "core/choose_role.html")
