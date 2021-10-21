from django.contrib import admin
from .models import Walk, Option, Vote, Tag, Comment


admin.site.register(Walk)
admin.site.register(Option)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(Comment)
