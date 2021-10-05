from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
# CreateView automaticaaly save data for us.
from django.views.generic.edit import CreateView

from .forms import ReviewForm
from .models import Review


# Create your views here.

class ReviewView(CreateView):
    model = Review
    # labels key is not possible here, so we can point to form_class too.
    form_class = ReviewForm
    # fields = "__all__"
    template_name = "reviews/review.html"
    success_url = "/thank-you"


class TankYouView(TemplateView):
    def get_template_names(self):
        return ["reviews/thank_you.html"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Good Job!"
        return context


class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    # django will fetch all the data realted to the model -
    # - and pass it as context to the template.
    model = Review
    context_object_name = "reviews"

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.filter(rating__gte=1)
        return data
    

class SingleReviewView(DetailView):
    template_name = "reviews/single_review.html"
    # django automatically took the model name basically all lower case - 
    # - and exposes the fetched single peice of data though the model name to our template.
    model = Review

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        # use get method, it will not throw an error if favorite review doesn't exist yet.
        favorite_id = request.session.get("favorite_review")
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context
    
    # django identify a single item with our slug or the primary key defined by us in our urls.py.


class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["reivew_id"]
        # fav_review = Review.objects.get(pk=review_id)
        # django automatically save the data in the database.
        # don't store objects in sessions.
        request.session["favorite_review"] = review_id
        return HttpResponseRedirect("/reviews/" + review_id)