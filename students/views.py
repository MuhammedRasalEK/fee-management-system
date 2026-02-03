from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



from .models import StudentProfile, Fee, Payment


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')


# ---------------- SIGNUP ----------------
def signup_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        profile = StudentProfile.objects.create(
            user=user,
            admission_no=request.POST.get('admission_no'),
            department=request.POST.get('department'),
            semester=request.POST.get('semester'),
            dob=request.POST.get('dob')
        )

        Fee.objects.create(
            student=profile,
            total_amount=Decimal('50000'),
            paid_amount=Decimal('0'),
            balance_amount=Decimal('50000')
        )

        return redirect('login')

    return render(request, 'signup.html')


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    student = StudentProfile.objects.get(user=request.user)
    fee = Fee.objects.filter(student=student).first()

    return render(request, 'dashboard.html', {
        'student': student,
        'fee': fee
    })


# ---------------- PAY FEE ----------------
@login_required
def pay_fee(request):
    profile = StudentProfile.objects.get(user=request.user)
    fee = Fee.objects.get(student=profile)

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))

        Payment.objects.create(
            student=profile,
            bank_name=request.POST.get('bank'),
            transaction_id=request.POST.get('transaction'),
            amount=amount
        )

        fee.paid_amount += amount
        fee.balance_amount -= amount
        fee.save()

        return redirect('dashboard')

    # 👇 changed template name
    return render(request, 'pay_fee.html')


# ---------------- REPORT ----------------
@login_required
def fee_report(request):
    profile = StudentProfile.objects.get(user=request.user)
    payments = Payment.objects.filter(student=profile)

    # 👇 changed template name
    return render(request, 'fee_report.html', {
        'payments': payments
    })


# ---------------- PROFILE ----------------
@login_required
def profile_view(request):
    profile = StudentProfile.objects.get(user=request.user)

    return render(request, 'profile.html', {
        'profile': profile
    })


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('login')
