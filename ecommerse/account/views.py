from django.shortcuts import redirect, render
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.contrib.auth.models import User
# from django.contrib.sites.shortcuts import get_current_site
# from .token import user_tokenizer_generate
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import auth
# from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Welcome to gregyjudah store! You are registered"
            )
            # # email verification setup
            # current_site = get_current_site(request)
            # subject = 'Account verification email'
            # message = render_to_string('account/registration/email-verification.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': user_tokenizer_generate.make_token(user),
            # })
            # EmailMessage(subject=subject, body=message, from_email=settings.EMAIL_FROM_USER, to=[user.email])
            return redirect('dashboard')
        else:
            messages.success(
                request, "Something went wrong with your registration. Please try again"
            )
            return redirect('store')

    context = {'form': form}

    return render(request, 'account/registration/register.html', context=context)


# def email_verification(request, uidb64, token):

#     # uniqueid
#     unique_id = force_text(urlsaft_base64_decode(uidb64))
#     user = User.objects.get(pk=unique_id)

#     # success
#     if user and user_tokenizer_generate.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return redirect('email-verification-success')

#     # failed
#     else:
#         return redirect('email-verification-failed')


# def email_verification_sent(request):
#     return render(request, 'account/registration/email-verification-sent.html')


# def email_verification_success(request):
#     return render(request, 'account/registration/email-verification-success.html')


# def email_verification_failed(request):
#     return render(request, 'account/registration/email-verification-failed.html')


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'form': form}
    return render(request, 'account/my-login.html', context=context)


# Logout
@login_required(login_url='my-login')
def user_logout(request):
    auth.logout(request)
    return redirect("store")


@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required(login_url='my-login')
def profile_management(request):
    # Updating our user's username and email
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('dashboard')
    context = {'user_form': user_form}
    return render(request, 'account/profile-management.html', context=context)


@login_required(login_url='my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('store')
    return render(request, 'account/delete-account.html')
