import json
import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from django.core.cache import caches
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .forms import ProductForm, ReportForm
from .models import Product, Report
from django_app import models

RamCache = caches["default"]


# def get_cache(
#     key: str, query: callable = lambda: any, timeout: int = 10, cache: any = RamCache
# ) -> any:
#     data = cache.get(key)
#     if data is None:
#         data = query()
#         cache.set(key, data, timeout)
#     return data


def home(request):
    return render(request, "home.html", context={})


def sign_in(request):
    if request.method == "GET":
        return render(request, "sign-in.html")
    elif request.method == "POST":
        email = str(request.POST["email"])
        pwd = str(request.POST["pwd"])
        user = authenticate(username=email, password=pwd)
        if user is None:
            return render(
                request,
                "sign-in.html",
                context={"error": "Invalid email or password"},
            )
        login(request, user)
        return redirect("products")


def sign_up(request):
    if request.method == "GET":
        return render(request, "sign-up.html")
    elif request.method == "POST":
        email = str(request.POST["email"])
        pwd = str(request.POST["pwd"])
        user = authenticate(username=email, password=pwd)
        if user is None:
            user = User.objects.create(username=email, password=make_password(pwd))
        else:
            return render(
                request,
                "sign-up.html",
                context={"error": "Email is already registered"},
            )
        login(request, user)
        return redirect("products")


def log_out(request):
    logout(request)
    return redirect("sign-in")


@cache_page(5)
def products(request):
    # def compute_data() -> int:
    #     time.sleep(1.0)
    #     with open("data.json", "r") as file:
    #         data = json.load(file)
    #     return data["products"]

    # products = get_cache(key="products", query=compute_data, timeout=10, cache=RamCache)
    products = Product.objects.all()
    return render(request, "products.html", context={"products": products})


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product.html", {"product": product})


def add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        # if form.is_valid():
        #     with open("data.json", "r") as file:
        #         data = json.load(file)
        #     title = form.cleaned_data["title"]
        #     price = form.cleaned_data["price"]
        #     image = form.cleaned_data["image"]
        #     image_path = str(random.randint(1, 1000000)) + image.name
        #     product = {"name": title, "image": image_path, "price": float(price)}
        #     data["products"].append(product)
        #     with open("static/src/" + image_path, "wb") as destination:
        #         for chunk in image.chunks():
        #             destination.write(chunk)
        #     with open("data.json", "w") as file:
        #         json.dump(data, file, indent=2)
        #     return redirect("products")
        if form.is_valid():
            product = form.save(commit=False)
            product.image.name = (
                str(random.randint(1, 1000000)) + form.cleaned_data["image"].name
            )
            product.save()
            return redirect("products")
    else:
        form = ProductForm()
    return render(request, "form.html", {"form": form})


def edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product", pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "form.html", {"form": form})


def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("products")
    return render(request, "confirm.html", {"product": product})


@cache_page(5)
def reports(request, report_type=None):
    if report_type is None:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(type=report_type)
    selected_page = request.GET.get(key="page", default=1)
    page_objs = Paginator(object_list=reports, per_page=5)
    page_obj = page_objs.page(number=selected_page)
    return render(
        request,
        "reports.html",
        context={"page_obj": page_obj, "selected_type": report_type},
    )


def report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, "report-card.html", {"report": report})


def report_add(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            try:
                report = form.save()
                report.date = timezone.now().strftime("%d %b %y")
                report.save()
                return render(
                    request,
                    "reports-form.html",
                    {"form": form, "report": report},
                )
            except Exception as e:
                error = f"An error occurred while saving the report: {e}"
                return render(
                    request,
                    "reports-form.html",
                    {"form": form, "error": error},
                )
    else:
        form = ReportForm()
    return render(request, "reports-form.html", {"form": form})


@require_POST
def report_delete(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    return redirect("reports")
