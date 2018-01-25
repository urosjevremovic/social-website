import redis

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from common import ajax_required
from actions.utils import create_action

from .forms import ImageCreateForm
from .models import Image


r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIST_PORT, db =settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            create_action(request.user, 'bookmarked image', instance)
            messages.success(request, "Image added successfully")
            return redirect(instance.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    Image.objects.filter(id=id, slug=slug).update(num_views=F('num_views')+1)
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/detail.html', {'section': 'image', 'image': image, 'total_views': image.num_views})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'liked image', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
def image_list(request):
    images = Image.objects.all().exclude(user=request.user)
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/list_ajax.html', {'section': 'images', 'images': images})
    return render(request, 'images/list.html', {'sector': 'images', 'images': images})


@login_required
def users_image_list(request):
    user = request.user
    images = Image.objects.filter(user=user)
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/list_ajax.html', {'section': 'my images', 'images': images})
    return render(request, 'images/list.html', {'sector': 'my images', 'images': images})


@login_required
def image_ranking(request):
    most_viewed = Image.objects.all().order_by('-num_views')
    most_viewed = most_viewed[:10]
    return render(request, 'images/ranking.html', {"section": "ranking", "most_viewed": most_viewed})
