from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
import markdown
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser

openai_api_key = 'openai_key'
openai.api_key = openai_api_key

def chat_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-4o",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},  
            {"role": "user", "content": message},  
        ]
    )
    #print(response)
    #return response['choices'][0]['message']['content'].strip()
    # 응답 내용 추출 및 Markdown에서 HTML로 변환
    content = response['choices'][0]['message']['content'].strip()
    html_content = markdown.markdown(content)
    return html_content

def chatai(request):
    if isinstance(request.user, AnonymousUser):
        user = None 
    else:
        user = request.user

    chats = Chat.objects.filter(user=user) if user else []

    if request.method == 'POST':
        message = request.POST.get('message')
        response = chat_openai(message)

        if user:
            chat = Chat(user=user, message=message, response=response, created_at=timezone.now())
            chat.save()

        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'chats': chats})