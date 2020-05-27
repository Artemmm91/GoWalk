from django.contrib import admin
from .models import Poll, Option, Vote, Tag, Comment


admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(Comment)
