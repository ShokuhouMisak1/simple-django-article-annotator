from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Note(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    select_text = models.TextField(blank=True, null=True)
    note_content = models.TextField()
    start_index = models.IntegerField(default=0)
    end_index = models.IntegerField(default=0)
    def __str__(self):
        return f"Note for {self.article.title}"
