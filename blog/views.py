from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 поста на каждой странице.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если номер страницы не целочисленного формата, представить первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы вне диапозона, представить страницу с последнего запроса.
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Список активных комментариев для поста.
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # Комментарий был отправлен.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создать объект Comment, но в базу не сохранять.
            new_comment = comment_form.save(commit=False)
            # Назначить пост комментарию.
            new_comment.post = post
            # Сохранить комментарий в базу данных.
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Выбор поста по ID.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Форма будет отправлена.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Прохождение валидации полей формы.
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
