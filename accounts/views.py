from django.shortcuts import render, redirect
from .forms import CustomCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomCreationForm()

    return render(request, "accounts/signup.html", {"form": form})
