from django.contrib import admin


from news.models import NewsCategory , NewsPublish


class NewsCategoryAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,               {'fields': ['category_name']}),
    ]
	

# Register your models here.
admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(NewsPublish)