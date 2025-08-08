from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.gereric import List_View

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

class PostListView(ListView):
    """
    Alternativa funktsiam
    """
    queryset = Post.published.all()
    context_object_name = "post"
    paginate_by = 3 
    template_name = "blog/post/list.html"
