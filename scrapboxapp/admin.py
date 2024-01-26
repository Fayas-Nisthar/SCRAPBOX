from django.contrib import admin
from scrapboxapp.models import CategoryModel,ScrapModel,WhislistsModel
# Register your models here.

admin.site.register(CategoryModel)
admin.site.register(ScrapModel)
admin.site.register(WhislistsModel)
