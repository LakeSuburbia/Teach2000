from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "application/index.html")


def admin_panel(request):
    if not request.user.is_authenticated:
        return login(request)
    return render(request, "application/admin.html")


def login(request):
    if request.method == "POST":
        # Create login function
        index(request)

    return render(request, "application/logins.html")
