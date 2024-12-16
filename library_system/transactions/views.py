from django.shortcuts import render, redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from transactions.models import Transaction
from django.core.paginator import Paginator


def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    transactions = Transaction.objects.filter(user=request.user).order_by("-id")
    overpaid = request.user.profile.total_bill <= 0
    total_bill = abs(request.user.profile.total_bill)
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "transactions/home.html",
        {
            "user": request.user,
            "transactions": page_obj,
            "overpaid": overpaid,
            "total_bill": total_bill,
        },
    )


def payment(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    if request.method == "POST":
        next_url = request.GET.get("next", resolve_url("books:home"))
        if not url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}
        ):
            next_url = resolve_url("books:home")
        user = request.user
        try:
            amount = float(request.POST.get("amount"))
            if amount < 0:
                raise ValueError
        except:
            messages.error(request, "Invalid amount!")
            return redirect("transactions:home")
        total_bill = float(user.profile.total_bill)
        total_bill -= amount
        user.profile.total_bill = total_bill
        user.save()
        transaction = Transaction.objects.create(user=user, amount=amount)
        total_bill = -total_bill
        overpaid = total_bill >= 0
        s = (
            f"Your balance is: Rs. {abs(total_bill)}"
            if overpaid
            else f"You are yet to pay Rs. {abs(total_bill)}"
        )
        messages.success(request, f"Payment of Rs. {amount} successful! {s}")
        return redirect("transactions:home")
    messages.error(request, "You are not allowed to access the page!")
    return redirect("books:home")
