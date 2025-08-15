from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForms
from django.core.mail import send_mail

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
    context_object_name = "posts"
    paginate_by = 3 
    template_name = "blog/post/list.html"

def post_share(request, post_id):
#izvlech post po indentifukatoru id 
    post = get_object_or_404(Post, 
                             id=post_id, 
                             status=Post.Status.PUBLISHED,) 
    sent = False

    if request.method == 'POST':
        #formy nado otpravit na pererabotky
        form = EmailPostForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomend you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comment: {cd['comment']}"
            send_mail(subject, message, 'vasula.malafeev@gmail.com', 
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForms()
    return render(request, 
                'blog/post/share.html', 
                  {'post': post, 
                   'form': form, 
                   'sent': sent})
