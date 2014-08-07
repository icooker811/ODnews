# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404,render, redirect, render_to_response
from django.utils import timezone
from django.views import generic

from news.models import NewsCategory,NewsPublish
from news.forms import NewsForm 


def IndexView(request):
	news_list = NewsPublish.objects.order_by('-pub_date')
	paginator = Paginator(news_list, 5) 
	page = request.GET.get('page')
	try:
	    news = paginator.page(page)
	except PageNotAnInteger:
	    news = paginator.page(1)
	except EmptyPage:
	    news = paginator.page(paginator.num_pages)

	return render(request, 'index.html', {"news": news})



def categoryView(request, category):
	news_category = NewsCategory.objects.get(category_name=category)
	news_list = NewsPublish.objects.filter(category=news_category).order_by('-pub_date')
	paginator = Paginator(news_list, 20) 
	page = request.GET.get('page')
	try:
	    news = paginator.page(page)
	except PageNotAnInteger:
	    news = paginator.page(1)
	except EmptyPage:
	    news = paginator.page(paginator.num_pages)
	return render(request, 'category.html', {"news": news , "category" : news_category, })




@login_required
def reportnewsView(request):
	if request.method == 'POST':
	    form = NewsForm(request.POST, request.FILES)
	    if form.is_valid():
	        news_publish = NewsPublish()
	        news_publish.title = form.cleaned_data['title']
	        news_publish.stitle = form.cleaned_data['stitle']
	        news_publish.description = form.cleaned_data['description']
	        if form.cleaned_data['image'] != None:
				news_publish.newsimage = form.cleaned_data['image']
	        news_publish.category = form.cleaned_data['category']
	        news_publish.pub_date = timezone.now();
	        news_publish.reporter = request.user
	        news_publish.save()
		return redirect('news:index')
	else :
		form = NewsForm()
		
	return render(request, 'reportnews.html', {'form': form})





def detailView(request, category, news_id, news_title):
	try:
	    news = NewsPublish.objects.get(pk=news_id)
	except NewsPublish.DoesNotExist:
	    raise Http404
	return render(request, 'detail.html', {'news': news})


@login_required
def editView(request, category, news_id, news_title):
	news_publish = NewsPublish.objects.get(pk=news_id)
	if request.method == 'POST':
		form = NewsForm(request.POST, request.FILES)
		if form.is_valid():
		    news_publish.title = form.cleaned_data['title']
		    news_publish.stitle = form.cleaned_data['stitle']
		    news_publish.description = form.cleaned_data['description']
		    if form.cleaned_data['image'] != None:
		    	news_publish.newsimage = form.cleaned_data['image']
		    news_publish.category = form.cleaned_data['category']
		    news_publish.save()
		    return redirect('news:detailnews', category,  news_id, news_publish.title)
	else :
		form = NewsForm(initial={
			'title': news_publish.title,
			'stitle' : news_publish.stitle,
			'description' : news_publish.description,
			'category' : news_publish.category,
			})
	return render(request, 'editnews.html', {'form': form, 'news' : news_publish })

@login_required
def deleteView(request, category, news_id, news_title):
	if request.method == 'POST':
		news = NewsPublish.objects.get(pk=news_id).delete()
		return redirect('news:index')

