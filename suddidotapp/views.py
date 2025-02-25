from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsArticle, Category, Comment
import random
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

'''
------------------------------------------------------------------------------------------------
Home Function
------------------------------------------------------------------------------------------------
'''
def home(request):
    # trending news 
    trending_news = NewsArticle.objects.filter(is_trending=True).order_by('-published_at')[:3]

    # latest news 
    readnext_news = list(NewsArticle.objects.order_by('-published_at')[:20])
    random.shuffle(readnext_news)

    latest_news = list(NewsArticle.objects.order_by('-published_at'))

    # top trending posts 
    trending_posts = list(NewsArticle.objects.order_by('-views', '-published_at')[:5])

    # Get the very latest post (if not already in trending_posts)
    latest_post = NewsArticle.objects.order_by('-published_at').first()

    # Optionally, if the latest_post is already in trending_posts, you can skip it.
    if latest_post in trending_posts:
        new_post = None
    else:
        new_post = latest_post

    # Popular News 
    popular_news = NewsArticle.objects.order_by('-views')[:3]
    
    # Posts with Categories
    categories = list(Category.objects.all())
    random_categories = random.sample(categories, min(4, len(categories)))

    # Footer Categories 
    all_categories_footer = list(Category.objects.all())
    footer_categories = random.sample(all_categories_footer, min(8, len(all_categories_footer)))

    category_posts = {}
    for cat in random_categories:
        posts = NewsArticle.objects.filter(categories=cat).order_by('-published_at')[:4] 
        category_posts[cat] = posts
    
    context = {
        'readnext_news': readnext_news[:8], 
        'latest_news': latest_news[:4], 
        'trending_news': trending_news,
        'trending_posts': trending_posts,
        'new_post': new_post,
        'popular_news': popular_news,
        'categories': random_categories,
        'category_posts': category_posts,
        'new_news': latest_news[:6], 
        'footer_categories': footer_categories,
    }
    return render(request, 'index.html', context)

'''
------------------------------------------------------------------------------------------------
Category Function
------------------------------------------------------------------------------------------------
'''
def category(request,slug):
    readnext_news = list(NewsArticle.objects.order_by('-published_at')[:20])
    random.shuffle(readnext_news)

    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.all().order_by('-published_at')
    
    # Pagination 
    paginator = Paginator(articles,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Popular News 
    popular_news = NewsArticle.objects.order_by('-views')[:3]
    
    # Footer Categories
    categories = list(Category.objects.all())
    random_categories = random.sample(categories, min(8, len(categories)))

    # Latest News 
    latest_news = list(NewsArticle.objects.order_by('-published_at'))

    
    context = {
        'readnext_news': readnext_news[:8], 
        'category': category,
        'articles':articles,
        'page_obj': page_obj,
        'popular_news': popular_news,
        'categories': random_categories,
        'new_news': latest_news[:6], 

    }
    return render(request, 'category.html',context)

'''
------------------------------------------------------------------------------------------------
News Function
------------------------------------------------------------------------------------------------
'''
def news_detail(request, slug):
    news = get_object_or_404(NewsArticle, slug=slug)
    # Comments of the particular blog
    comments = news.comments.all().order_by('-created_at')

    # View count
    news.views += 1
    news.save()
    
    # latest news 
    readnext_news = list(NewsArticle.objects.order_by('-published_at')[:10])
    random.shuffle(readnext_news)

    # Popular News 
    popular_news = NewsArticle.objects.order_by('-views')[:3]
    
    # Footer Categories
    categories = list(Category.objects.all())
    random_categories = random.sample(categories, min(8, len(categories)))

    # Latest news 
    latest_news = list(NewsArticle.objects.order_by('-published_at'))

    # Comments of the blog
    if request.method == "POST":
        # Process new comment submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('msg')
        # Create comment associated with this article
        Comment.objects.create(
            news_article=news,
            name=name,
            email=email,
            message=message
        )
        # Redirect back to the article
        response = redirect('news_detail', slug=slug)
        #Set Cookies
        response.set_cookie('comment_name', name, max_age=2592000)
        response.set_cookie('comment_email', email, max_age=2592000)
        return response

    context = {
        'news': news,
        'readnext_news': readnext_news[:5],
        'popular_news': popular_news,
        'categories': random_categories,
        'new_news': latest_news[:6], 
        'comments': comments,
        'remembered_name': request.COOKIES.get('comment_name', ''),
        'remembered_email': request.COOKIES.get('comment_email', '')

    }
    return render(request, 'blogdisplay.html', context)  

'''
------------------------------------------------------------------------------------------------
Search Function
------------------------------------------------------------------------------------------------
'''
def search(request):
    query = request.GET.get('search', '')
    results = []
    if query:
        results = NewsArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-published_at')
    
    # Pagination 
    paginator = Paginator(results,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Popular News 
    popular_news = NewsArticle.objects.order_by('-views')[:3]
    
    # Footer Categories
    categories = list(Category.objects.all())
    random_categories = random.sample(categories, min(8, len(categories)))
    
    context = {
        'query': query,
        'results': results,
        'page_obj': page_obj,
        'popular_news': popular_news,
        'categories': random_categories,
    }
    return render(request, 'search_results.html', context)

'''
------------------------------------------------------------------------------------------------
Search Function
------------------------------------------------------------------------------------------------
'''