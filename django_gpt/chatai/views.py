from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
import markdown
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

openai_api_key = 'mykey'
openai.api_key = openai_api_key

def chat_openai(message):
    response = openai.ChatCompletion.create(
        #model = "gpt-3.5-turbo",
        model = "gpt-4o",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},  # 시스템 메시지
            {"role": "user", "content": message},  # 사용자 메시지
        ]
    )
    #print(response)
    #return response['choices'][0]['message']['content'].strip()
    # 응답 내용 추출 및 Markdown에서 HTML로 변환
    content = response['choices'][0]['message']['content'].strip()
    html_content = markdown.markdown(content)
    return html_content

def chatai(request):
    # if not request.user.is_authenticated:
    #    return redirect('login')  # 로그인되지 않은 경우 로그인 페이지로 이동
    
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = chat_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response':response})        
    return render(request, 'chatbot.html', {'chats': chats})