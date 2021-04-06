from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.utils import timezone
from django.contrib import messages

from .models import Post, Comment

def clone_data(self, request, queryset):
    
    def copy_obj(queryset_obj):

        for obj in queryset_obj:
            # print(Post_book.objects.all())
            id_start_num = Post.objects.all().latest('id').id
            # print('last id is: ', id_start_num)
            id_num = id_start_num+1
            # print('id to set: ', id_num)
            obj.id = id_num
            obj.timestamp = timezone.now()
            obj.save()
         
        return len(queryset_obj)

    updated = copy_obj(queryset)

    self.message_user(request, ngettext(
        " '"+str(updated)+"' object is successfully copied.",
        " '"+str(updated)+"' objects are successfully copied.",
        updated
    ), messages.SUCCESS)
clone_data.allowed_permissions = ('add',)                      # Setting permissions for actions
clone_data.short_description = "copy the objects"


class Post_admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']
    list_display_links = ['id', 'title',]
    list_filter = ['timestamp']
    ordering = ['id']
    search_fields = ['title']
    actions = [clone_data]


admin.site.register(Post, Post_admin)
admin.site.register(Comment)