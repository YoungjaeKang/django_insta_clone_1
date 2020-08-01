from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from instagram.forms import PostForm
from .models import Post


@login_required
def index(request):
    return render(request, "instagram/index.html", {

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
    return render(request, "instagram/post_detail.html", {
        "post": post,
    })


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()
    # 실제 데이터베이스에 count 쿼리를 던지게 된다.
    # len(post_list)로 하면 post_list를 가져와서 메모리에 올린 다음에 세기 떄문에 느릴 수 있다.
    # django debug toolbar에서 sql을 열어보자.
    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
    })