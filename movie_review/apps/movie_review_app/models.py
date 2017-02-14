from __future__ import unicode_literals
from ..login_app.models import User
from django.db import models


# Create your models here.


class Director(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    title = models.CharField(max_length=45)
    director = models.ForeignKey('Director')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReviewManager(models.Manager):

    def create_review(self, form_data, user_id):
        try:
            movie = self.fetch_movie(form_data)
            user = User.objects.get(id=user_id)
            new_review = Review.objects.create(review=form_data['review'], rating=form_data[
                                               'rating'], user=user, movie=movie)
            return (True, new_review)
        except:
            return (False, ["There was a problem creating the review..."])

    def fetch_movie(self, form_data):
        try:
            movie = Movie.objects.get(id=form_data['movie_id'])
        except:
            director = self.fetch_director(form_data)
            movie = Movie.objects.create(
                title=form_data['new_movie'], director=director)
        return movie

    def fetch_director(self, form_data):
        try:
            director = Director.objects.get(id=form_data['director_id'])
        except:
            director = Director.objects.create(name=form_data['new_director'])
        return director

    def fetch_recent(self):
        return Review.objects.all().order_by('-created_at')[:3]


class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey('login_app.User')
    movie = models.ForeignKey('Movie')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()
