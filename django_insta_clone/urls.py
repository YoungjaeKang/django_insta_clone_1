from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
# import django_pydenticon.urls
from django_pydenticon.views import image as pydenticon_image


# @login_required
# def root(request):
#     return render(request, "root.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('identicon/image/<path:data>/', pydenticon_image, name='pydenticon_image'),
    path('', include('instagram.urls')),
    # path('', name='root'),
    path('', login_required(TemplateView.as_view(template_name='root.html')), name='root')
]
# re_path를 쓰면 정규 표현식이기 때문에 '' 같은 빈 주소는 아무 주소나 매칭이 된다.

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)