from django.shortcuts import render, redirect
from django.urls import reverse
from models import Movie, Director, Review
from ..login_app.models import User
from ..login_app.views import print_messages

from django.template import Library
register = Library()


def check_logged_in(request):
    return 'user' in request.session


@register.filter
def index(request):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    context = {
        'movies': Movie.objects.all(),
        'reviews': Review.objects.fetch_recent()
    }

    return render(request, 'movie_review_app/index.html', context)


def new(request):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    context = {
        'movies': Movie.objects.all(),
        'directors': Director.objects.all()
    }

    return render(request, 'movie_review_app/new.html', context)


def create(request):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    result = Review.objects.create_review(
        request.POST, request.session['user']['id'])

    if result[0] == True:
        return redirect(reverse('reviews:show', kwargs={'id': result[1].movie.id}))
    else:
        print_messages(request, result[1])
        return redirect(reverse('reviews:new'))


@register.filter
def show(request, id):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    context = {
        'movie': Movie.objects.get(id=id)
    }
    return render(request, 'movie_review_app/show.html', context)


@register.filter
def show_user(request, id):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    context = {
        'user': User.objects.fetch_user_info(id)
    }

    return render(request, 'movie_review_app/show_user.html', context)
