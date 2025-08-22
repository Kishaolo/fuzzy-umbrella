from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity 
from .forms import EmailPostForms, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

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
    # spisok aktivnix commentov k atomy posty
    comments = post.comments.filter(active=True)
    # forma dla comentirovania userov
    form = CommentForm()

    #post = get_object_or_404(
     #       Post, 
      #      id=id, 
       #     status=Post.Status.PUBLISHED
        #    )
    #try:
     #   post = Post.published.get(id=id)
    #except:
     #   raise Http404("No Post found.")

    #spisok sxoshix postov
    """
    1. Берется список тегов по ид, они идут в кортежах поэтому к ним добовляется флат для того чтоб получить элимент а не одиночный картеж
    2. Выбираются все посты без текущего
    3. футкция Count запимывает в -same_tags число тегов обшиз с запрошеным
    4. результат урорядочивается по убыванию (сначала новые)
    5. Объект similar_posts передается в словарь для функции render
    """
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) #__in poisk po polu
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    
    return render(
            request, 
            'blog/post/detail.html', 
            {'post': post, 
             'comments': comments, 
             'form': form, 
             'similar_posts': similar_posts}
            )


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag=None 
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    #paginatsia po 3
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageAnInteger:
        #esli page_number ne int to vidat first page
        posts = paginator.page(1)
    except EmptyPage:
        #esli page_number naxoditsa vne diapazona ot vidat posledniustranitsu diapazona 
        posts = paginator.page(paginator.num_pages)
    return render(request, 
                  'blog/post/list.html', 
                  {'posts': posts, 
                   'tag': tag})


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


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, 
                            id=post_id, 
                            status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # sozdaet comment i ne soxronaet ego v db 
        comment = form.save(commit=False)
        #naznachit post komentariu
        comment.post = post
        #soxranit comment b db 
        comment.save()
    return render(request, 
                  'blog/post/comment.html', 
                  {'post': post, 
                   'form': form, 
                   'comment': comment})


def post_search(request): 
    form = SearchForm() 
    query = None 
    results = []

    if 'query' in request.GET: 
        form = SearchForm(request.GET)
        if form.is_valid(): 
            query = form.cleaned_data['query']
            #k search_vector применили вес. Это значит, что теперь в приоретете ищутся совпадения в заголовках.
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request, 
                  'blog/post/search.html', 
                  {'form': form, 
                   'query': query, 
                   'results': results})
