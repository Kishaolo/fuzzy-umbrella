from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404

# Create your views here.
def post_detail(request, id):
    """funktion vozvrashaet oshibky 404 vmesto doesNotExitst"""
    #libo post libo 404
    post = get_object_or_404(
            Post, 
            id=id, 
            status=Post.Status.PUBLISHED
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
    posts = Post.published.all()
    return render(
            request, 
            'blog/post/list.html', 
            {'posts': posts}
            )
