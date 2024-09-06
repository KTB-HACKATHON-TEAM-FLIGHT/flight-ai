from django.shortcuts import render
from django.http import JsonResponse
import openai
import markdown
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def chat_openai(message):
    prompt = f"""
    You are a kind planner who composes the given content into 8 pages of ppt. 
    Show me the ppt you have composed

    the given content: '''{message}'''
    """

    response = openai.ChatCompletion.create(
        #model = "gpt-3.5-turbo",
        model = "gpt-4o",
        messages=[
            {"role": "system", "content": prompt},  # 시스템 메시지
            {"role": "user", "content": message},  # 사용자 메시지
        ]
    )
    result = response['choices'][0]['message']['content'].strip()
    realContent = makeMarkdown(result)
    return realContent

def makeMarkdown(message):
    prompt = f"""
    Show this in a markdown code. Make sure the page is '---' and make sure you distinguish between spaces, indentations, line breaks, and paragraphs.
    Please print it out according to the 'Marpit' format.
    Don't say anything but markdown code.

    the given content: '''{message}'''
    """

    response = openai.ChatCompletion.create(
        #model = "gpt-3.5-turbo",
        model = "gpt-4o",
        messages=[
            {"role": "system", "content": prompt},  # 시스템 메시지
            {"role": "user", "content": message},  # 사용자 메시지
        ]
    )

    result2 = response['choices'][0]['message']['content'].strip()
    # html_content = markdown.markdown(result2)

    return result2


def chatai(request):
    # if not request.user.is_authenticated:
    #    return redirect('login')  # 로그인되지 않은 경우 로그인 페이지로 이동
    
    chats = Chat.objects.all()

    if request.method == 'POST':
        message = request.POST.get('message')
        response = chat_openai(message)

        chat = Chat(message=message, response=response)
        chat.save()
        
        return JsonResponse({'message': message, 'response':response})        
    return render(request, 'chatbot.html', {'chats': chats})