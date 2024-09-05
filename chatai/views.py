from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
import markdown
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

openai_api_key = 'sk-M85V7vWe5hRq9n6GLy4FBbom3wcmj2FdiTahjArgZJT3BlbkFJculDs_vkml3LYWRQVmqhoWXpXGZWMVTZDXEAaRY_MA'
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

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('chatbot')
#         else:
#             error_message = '아이디나 비밀번호가 틀렸습니다'
#             return render(request, 'login.html', {'error_message': error_message})
#     else:
#         return render(request, 'login.html')

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 == password2:
#             try:
#                 user = User.objects.create_user(username, email, password1)
#                 user.save()
#                 auth.login(request, user)
#                 return redirect('chatbot')
#             except:
#                 error_message = '계정 생성 실패'
#                 return render(request, 'register.html', {'error_message': error_message})
            
#         else:
#             error_message = '비밀번호 일치 않음'
#             return render(request, 'register.html', {'error_message': error_message})
#     return render(request, 'register.html')

# def logout(request):
#     auth.logout(request)
#     return redirect('login')