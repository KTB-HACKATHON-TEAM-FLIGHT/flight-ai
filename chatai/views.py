from django.shortcuts import render
from django.http import JsonResponse
import openai
import markdown
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
import requests

def get_image(query):
    api_key = ""
    search_engine_id = ""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={search_engine_id}&key={api_key}"

    response = requests.get(url)
    results = response.json()
    image_list = []
    for item in results['items'][:10]:  # 상위 3개의 검색 결과를 가져옵니다
        pagemap = item.get('pagemap', {})
        cse_images = pagemap.get('cse_image', [])
        if cse_images:  # 이미지가 존재할 경우
            image_list.append(cse_images[0]['src'])
            #return cse_images[0]['src']
    
    return image_list

def google_search(query):
    api_key = ""
    search_engine_id = ""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={search_engine_id}&key={api_key}"
    
    response = requests.get(url)
    results = response.json()
    if 'items' in results:
        # 상위 3개의 검색 결과 링크 반환
        return [item['link'] for item in results['items'][:3]]

    else:
        return None

def generate_rag_response(query):
    search_results = google_search(query)
    
    if search_results:
        search_context = " ".join(search_results)  # 검색 결과를 하나의 컨텍스트로 합침
        gpt_input = f"Given the following search results: {search_context}, please answer the query: {query}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": gpt_input}]
        )
        
        return response['choices'][0]['message']['content'].strip()
    else:
        return "No relevant search results found."


openai_api_key = 'sk-'
openai.api_key = openai_api_key

# 메인 gpt코드
def chat_openai(message):
    topic = get_topic(message)
    information = generate_rag_response(topic)
    image_list = get_image(topic)

    prompt = f"""
            You are an AI assistant responsible for creating professional PowerPoint presentations in Korean. 
            Your task is to generate a structured outline of a PPT containing the following slides:

            1. **Slide 1 (Title Slide)**:
                - Include the main title of the presentation.
                - Add a subtitle that summarizes or provides context for the presentation.
                - Include the presenter's name or title.

            2. **Slide 2 (Contents)**:
                - Title: "Contents".
                - List of key topics or sections to be covered in the presentation.
                
            3. **Second-to-Last Slide (Q&A)**:
                - Title: "Q&A".
                - Add a brief message encouraging questions or feedback.

            4. **Last Slide (Thank You)**:
                - Title: "Thank You".
                - Display a closing message thanking the audience for their attention.

            5. important!! I told you to refer to the title, so make a new one and write it. Don't put slide numbers or slide words.
                For example in slide 2, just put "Contents" in title, not "Slide 2 (Contents)".  
            6. Keep the slide layout clean, organized, and relevant to the user’s input.
            7. You don't have to answer other ment. Just put information about ppt.
            8. Please insert 1-2 appropriate statistical graphs or tables on a random page.
            9. Make the composition more dynamic so that the viewer can have an interesting ppt
            10. I wish I could see sentences that describe each content in more detail often
            11. Cover the divided pages with a <section> tag and show them

            the given topic: '''{message}'''
            Please make the ppt content richer using the given topic and this {information}. I hope 2-3 images are inserted.
            Use the image in the {image_list} as it is and display it on the screen.
            The screen will be composed at a 16:9 ratio, please insert it in half the size
            Insert the image in this format : '![Image](image url here)'
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

    #realContent = makeMarkdown(result)
    html_content = markdown.markdown(result)
    print(html_content)
    return html_content

# 사용자가 입력한 문장에서 주제가 될 단어 추출하는 프롬포트
def get_topic(message):
    prompt = f"""
    Please tell me the one relevant word that can be represented in this message.
    Just say exactly that word.

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

    return result2


def chatai(request):
    chats = Chat.objects.all()

    if request.method == 'POST':
        message = request.POST.get('message')
        response = chat_openai(message)

        chat = Chat(message=message, response=response)
        chat.save()
        
        return JsonResponse({'message': message, 'response':response})        
    return render(request, 'chatbot.html', {'chats': chats})