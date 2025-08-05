from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_detail(request, year, month, day, post):
    """funktion vozvrashaet oshibky 404 vmesto doesNotExitst"""
    #libo post libo 404
    post = get_object_or_404(
            Post, 
            status=Post.Status.PUBLISHED, 
            slug=post, 
            publish__year=year, 
            publish__month=month, 
            publish__day=day
            )

    #post = get_object_or_404(
     #       Post, 
      #      id=id, 
       #     status=Post.Status.PUBLISHED
        #    )
    #try:
     #   post = Post.published.get(id=id)
    #except:
     #   raise Http404("No Post found.")

    return render(
            request, 
            'blog/post/detail.html', 
            {'post': post}
            )

def post_list(request):
    post_list = Post.published.all()
    # разбивка  3 поста на странице
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #информирует если переменная page не равна int
        posts = paginator.page(1)
    except EmptyPage:
        #sdelat posledniu str 
        posts = paginator.page(paginator.num_pages)
    return render(
            request, 
            'blog/post/list.html', 
            {'posts': posts}
            )
