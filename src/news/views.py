# -*- encoding: utf-8 -*-
from django.shortcuts import get_object_or_404,render, redirect
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission, User
from django.contrib.auth import login,logout
from news.models import NewsCategory,NewsPublish
from django.utils import timezone
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


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



def LoginView(request):
	if request.method == 'POST':
		form = UserloginForm(request.POST)
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				 login(request, user)
				 if request.GET.get('next'): 
				 	return redirect( request.GET['next'] )
				 else : 
				 	return redirect( 'news:index' )
			else:
				return render(request, 'login.html', {
					'form' : form,
			    	'error_message': "The password is valid, but the account has been disabled!",
				})
		else:
			return render(request, 'login.html', {
				'form' : form,
			    'error_message': "The username and password were incorrect.",
			})
	form = UserloginForm()
	return render(request, 'login.html', RequestContext(request, {'form' : form}))


def logoutView(request):
	logout(request)
	return redirect(('news:index'))


@login_required
def reportnewsView(request):
	if request.method == 'POST':
	    form = AddNewsForm(request.POST, request.FILES)
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
		form = AddNewsForm()
		
	return render(request, 'reportnews.html', {'form': form})


class AddNewsForm(forms.Form):
    title = forms.CharField(label=u'หัวข้อ', max_length=75 , widget=forms.TextInput(attrs={'class': 'form-control'}))
    stitle = forms.CharField(label=u'คำโปรย', max_length=150 , widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label=u'เนื้อหาข่าว', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label=u'รูปภาพประกอบข่าว',required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(label=u'ประเภทข่าว',queryset=NewsCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))


class UserloginForm(forms.Form):
    username = forms.CharField(label=u'ผู้ใช้', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=u'รหัสผ่าน', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


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
		form = AddNewsForm(request.POST, request.FILES)
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
		form = AddNewsForm(initial={
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

