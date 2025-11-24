from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Note
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from docx import Document

HF_API_TOKEN ="hf_"
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

# Create your views here.
# reader/views.py

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'reader/article_list.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        text = request.POST.get('select_text')
        content = request.POST.get('note_content')
        start = request.POST.get('start_index')
        end = request.POST.get('end_index')
        if content:
            Note.objects.create(
                article=article,
                select_text=text if text else "",
                note_content=content,
                start_index=start if start else 0,
                end_index=end if end else 0
            )
            return redirect('article_detail', article_id=article_id)
    notes = Note.objects.filter(article=article)
    context = {
        'article': article,
        'notes': notes
    }
    return render(request, 'reader/article_detail.html', context)

def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    article_id = note.article.id
    if request.method == 'POST':
        note.delete()
    return redirect('article_detail', article_id=article_id)


def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        new_content = request.POST.get('note_content')
        note.note_content = new_content
        note.save()
    return redirect('article_detail', article_id=note.article.id)

@csrf_exempt
def summarize_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            input_text = data.get('text', '')
            if not input_text:
                return JsonResponse({'error': 'No text provided'}, status=400)
            headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
            payload = {
                "inputs": input_text,
                "parameters": {"max_length": 100, "min_length": 30, "do_sample": False}
            }
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                summary = result[0].get('summary_text', '')
                return JsonResponse({'summary': summary})
            elif isinstance(result, dict) and 'error' in result:
                error_msg = result['error']
                if 'loading' in error_msg.lower():
                    estimated_time = result.get('estimated_time', 20)
                    return JsonResponse({
                        'summary': f"The Model is generating, please wait for {int(estimated_time)} seconds..."
                    })
                return JsonResponse({'summary': f"API Error: {error_msg}"})
            else:
                return JsonResponse({'summary': 'Unrecognized Error'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)


def upload_article(request):
    if request.method == 'POST' and request.FILES.get('article_file'):
        try:
            uploaded_file = request.FILES['article_file']
            file_name = uploaded_file.name
            title = os.path.splitext(file_name)[0]
            content = ""
            if file_name.endswith('.txt'):
                content = uploaded_file.read().decode('utf-8')
            elif file_name.endswith('.docx'):
                doc = Document(uploaded_file)
                content = "\n\n".join([para.text for para in doc.paragraphs])
            else:
                return redirect('article_list')
            if content:
                Article.objects.create(title=title, content=content)
        except Exception as e:
            print(f"Error: {e}")
    return redirect('article_list')
