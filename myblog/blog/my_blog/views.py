from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Article, Carousel, AboutAuthor, Category,Tag

from django.core.paginator import Paginator


# Create your views here.
# 视图函数
def article_list(request):
    articles = Article.objects.all()

    # paginator = Paginator(articles, 4)
    # # 获取 url 中的页码
    # page = request.GET.get('page')
    # # 将导航对象相应的页码内容返回给 articles
    #
    # articles = paginator.page(page)

    carousels = Carousel.objects.all()
    articles_top = Article.objects.all().filter(is_top=True)
    author = AboutAuthor.objects.get(name='Chenglulu')
    context = {'articles': articles, 'carousels': carousels, 'articles_top': articles_top, 'author': author}
    return render(request, 'my_blog2/index.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = Article.objects.get(id=id)
    article.update_views()
    article.body = article.body_to_markdown()
    # 需要传递给模板的对象
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'my_blog2/table.html', context)


def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Article.objects.filter(category=cate).order_by('-create_date')
    return render(request, 'my_blog2/list.html', context={'post_list': post_list})


def archive(request, year, month):
    post_list = Article.objects.filter(create_date__year=year,
                                       create_date__month=month,
                                       ).order_by('-create_date')
    return render(request, 'my_blog2/list.html', context={'post_list': post_list})


def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Article.objects.filter(tags=t).order_by('-create_date')
    return render(request, 'my_blog2/list.html', context={'post_list': post_list})


def search(request):
    keyboard = request.GET.get('keyboard')
    print(keyboard)

    if keyboard:
        post_list = Article.objects.filter(
            Q(title__icontains=keyboard) |
            Q(body__icontains=keyboard)
        )
    else:
        post_list = Article.objects.all()

    context = {'post_list': post_list}
    return render(request, 'my_blog2/list.html', context)
