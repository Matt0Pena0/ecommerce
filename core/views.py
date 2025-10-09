from django.shortcuts import render


def home_view(request):
    return render(request, "core/Home.html")

def contact_view(request):
    return render(request, "core/Home.html")

