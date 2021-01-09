from django.contrib import admin
from  .models import *
# Register your models here.



class BookAdmin(admin.ModelAdmin):
    exclude = ('slug','user', )
    list_filter = ('category', 'created', 'year', )
    ordering = ('-created', )

    def save_model(self,request,obj,form,change):
        if getattr(obj,'user',None) is None:
            obj.user =request.user
        obj.save()

class DownloadAdmin(admin.ModelAdmin):
    exclude = ('pk', )

    

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book,BookAdmin)
admin.site.register(Download,DownloadAdmin)
