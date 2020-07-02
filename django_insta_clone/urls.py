from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='root.html'), name='root')
]
# re_path를 쓰면 정규 표현식이기 때문에 '' 같은 빈 주소는 아무 주소나 매칭이 된다.

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_ROOT,
                          document_root=settings.MEDIA_ROOT)