#encoding:utf-8
from django.shortcuts import render, redirect, render_to_response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from forms import ArticleForm
import models

# Create your views here.

def index(request):
  articles = models.Article.objects.all()
  return render(request, 'web/index.html', {'articles': articles})

def category(request, category_id):
  articles = models.Article.objects.filter(category_id = category_id)
  return render(request, 'web/index.html', {'articles': articles})

def article_detail(request, article_id):
  try:
    article_detail = models.Article.objects.get(id = article_id)
  except ObjectDoesNotExist, e:
    return render(request, 'base/404.html', {'err_msg': 'Artcile not found'})
  return render(request, 'web/article.html', {'article_detail': article_detail})



def dj_login(request):
  err_msg = ''
  if request.method == 'POST':
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    #django admin 的后台认证功能
    user = authenticate(username = username, password = password)
    if user:
      #验证成功需要登录 把session生成
      login(request, user)
      return HttpResponseRedirect('/web/')
    else:
      err_msg = "Some error about username or password"
  return render(request, 'web/login.html', {'title': 'Login', 'err_msg': err_msg})

def dj_logout(request):
  logout(request)
  return HttpResponseRedirect('/web')

def dj_reg(request):
  return render(request, 'web/reg.html', {'title': 'Register'})

def new_article(request):
  if request.method == 'POST':
    print request.POST
    form = ArticleForm(request.POST)
    if form.is_valid():
      print "form data: ", form.cleaned_data
      form_data = form.cleaned_data
      form_data['author_id'] = request.user.userprofile.id
      new_article_obj = models.Article(**form_data)
      new_article_obj.save()

      return render(request, 'web/new_article.html', {'title': 'New Article Published', 'new_article_obj': new_article_obj })
    else:
      print "Error: ", form.errors

  category_list = models.Category.objects.all()
  return render(request, 'web/new_article.html', {'title': 'New Article', 'category_list':category_list})

def list(request):
  return HttpResponse('web list')

