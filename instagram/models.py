# from accounts.models import User 이렇게 해도 동작은 하지만 settings를 import하고 거기서 AUTH_USER_MODEL을 불러올 것
from django.conf import settings
from django.db import models
import re
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("instagram:post_detail)", args=[self.pk])


# Tag는 django taggit을 써도 되지만 공부를 위해 아래와 같이 만들어본다.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name