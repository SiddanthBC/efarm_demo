from django.contrib import admin
from .models import PageView,creds

# Register your models here.


class PageViewAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'timestamp']

class CredsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','password']

admin.site.register(PageView, PageViewAdmin)
admin.site.register(creds,CredsAdmin)
