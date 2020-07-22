from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from instagram.forms import PostForm


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
            return redirect("/") # TODO: get_absolute_url 활용해서 post로 redirect
    # 이 else의 위치가 안으로 들어가면 안되고 여기 있어야 한다.
    else:
        form = PostForm()

    return render(request, "instagram/post_form.html", {
        "form": form,
    })
