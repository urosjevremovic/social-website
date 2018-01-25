from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save

from common import ajax_required
from actions.utils import create_action
from actions.models import Action

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Contact, Profile
from .utils import code_generator


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd.get('username'), password=cd.get('password'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("This account has been suspended.")
            else:
                return HttpResponse("Invalid credentials, please try again.")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    paginator = Paginator(actions, 10)
    page = request.GET.get('page')
    if following_ids:
        actions = \
            actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        actions = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'actions/detail.html', {'section': 'dashboard', 'actions': actions})

    return render(request, "account/dashboard.html", {"section": "dashboard", "actions": actions})


class LoginAfterPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('account:login')


login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view())


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data.get('password'))
            new_user.is_active = False
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            create_action(new_user, 'created an account')
            return render(request, 'account/register_done.html', {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {"form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('account:dashboard')
        else:
            messages.error(request, "Error occurred while updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {"user_form": user_form, "profile_form": profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    paginator = Paginator(users, 25)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        users = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'account/list_ajax.html', {'section': 'people', 'users': users})

    return render(request, 'account/list.html', {"section": "people", "users": users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/detail.html', {"section": "people", "user": user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'has started following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "ok"})


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = User.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            user = qs.first()
            if not user.is_active:
                user.is_active = True
                user.save()
                return render(request, 'account/account_activated.html', {"user": user})
    # invalid code
    return redirect(reverse('account:login'))