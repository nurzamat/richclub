from django.shortcuts import render,get_object_or_404
from .models import News,Sliders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def MainPage(request):
    main_news=News.objects.order_by('created')[0:3]
    slides=Sliders.objects.order_by('created')

    return render(request, 'main/main.html', {
        'news':main_news,'slides':slides
    })


def NewsList(request):
    news_list=News.objects.order_by('updated')
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    return render(request, 'main/news.html',{'news':news})


def NewsDetail(request,id):
    item = get_object_or_404(News, id=id)
    return render(request, 'main/newsdetail.html',{'item':item})


def SlideDetail(request,id):
    item = get_object_or_404(Sliders, id=id)
    return render(request, 'main/newsdetail.html',{'item':item})