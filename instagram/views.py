from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from instagram.forms import PostForm, CommentForm
from .models import Post


@login_required
def index(request):
    # 등록 날짜를 조건으로 넣을 수도 있다.
    # timesince = timezone.now() - timedelta(days=3)
    post_list = Post.objects.all()\
                .filter(
                    Q(author=request.user) |
                    Q(author__in=request.user.following_set.all())
                )\
                # .filter(
                #     created_at__gte=timesince
                # )

    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all())[:3]
    # 첫번째 exclude: 현재 user의 데이터는 제외하겠따.
    # 두번째 exclude: 이미 follow한 친구는 suggestions for you에서 제외하겠따.

    comment_form = CommentForm()

    return render(request, "instagram/index.html", {
        "post_list": post_list,
        "suggested_user_list": suggested_user_list,
        "comment_form": comment_form,
    })


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save() # db가 먼저 저장이 되고 pk가 있어야 한다.
            post.tag_set.add(*post.extract_tag_list())
            # for tag_name in post.extract_tag_list():
            #     tag, _ = Tag.objects.get_or_create(name=tag_name)
            messages.success(request, "포스팅을 저장했습니다.")
            return redirect(post) # TODO: get_absolute_url 활용해서 post로 redirect
    # 이 else의 위치가 안으로 들어가면 안되고 여기 있어야 한다.
    else:
        form = PostForm()

    return render(request, "instagram/post_form.html", {
        "form": form,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, "instagram/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
    })


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"{post}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"{post}의 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.is_ajax():
                return render(request, "instagram/_comment.html", {
                    "comment": comment,
                })
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "instagram/comment_form.html", {
        "form": form,
    })


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()
    # 실제 데이터베이스에 count 쿼리를 던지게 된다.
    # len(post_list)로 하면 post_list를 가져와서 메모리에 올린 다음에 세기 떄문에 느릴 수 있다.
    # django debug toolbar에서 sql을 열어보자.

    # request.user = 로그인되어 있으면 User 객체, 아니면 AnonymousUser
    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "is_follow": is_follow,
    })


