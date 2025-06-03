from django.contrib import admin
from post.models import Action, Post, PostAction

admin.site.register(Action)
admin.site.register(Post)
admin.site.register(PostAction)