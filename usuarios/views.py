from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("lista_productos")  # Redirigir a la lista de productos después de login
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "usuarios/login.html")


def user_logout(request):
    logout(request)
    return redirect("user_login")  # Redirigir al login después de cerrar sesión


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/productos/")  # O redirigir a "/productos/"
        return super().get(request, *args, **kwargs)
