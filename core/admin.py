from django.contrib import admin
from .models import Category, KnowledgeBase, DocumentFile


admin.site.register(Category)


class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ['description', 'author']


admin.site.register(KnowledgeBase, KnowledgeAdmin)
admin.site.register(DocumentFile)
