from django.contrib import admin
from .models import Article, Note
# Register your models here.

admin.site.register(Article)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('article','note_content','select_text')

admin.site.register(Note, NoteAdmin)