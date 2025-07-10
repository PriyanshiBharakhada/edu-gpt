from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from .chatbot import get_chat_response


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()

            if not message:
                return JsonResponse({'error': 'Empty message'}, status=400)

            # ✅ Just use get_chat_response() without extra arguments
            from .chatbot import get_chat_response
            response = get_chat_response(message)

            # ✅ Save to history
            ChatMessage.objects.create(
                user=request.user,
                message=message,
                response=response
            )

            return JsonResponse({'response': response})
        except Exception as e:
            print("🔥 Chatbot error:", e)
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)



@login_required
def chatbot(request):
    return render(request, 'chatbot.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('chatbot')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('chatbot')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def chat_history(request):
    history = ChatMessage.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, 'chat_history.html', {"history": history})

@login_required
def clear_history(request):
    ChatMessage.objects.filter(user=request.user).delete()
    return redirect("chat-history")

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


import os

import threading, time, hashlib, json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from .models import PdfQuestionAnswer
from edu import PDFQAHandler
from django.core.paginator import Paginator

handler_lock = threading.Lock()
pdf_handler = None

def get_pdf_handler():
    global pdf_handler
    with handler_lock:
        if pdf_handler is None:
            pdf_handler = PDFQAHandler()
    return pdf_handler

def get_hash(content):
    return hashlib.md5(content).hexdigest()

@login_required
@csrf_exempt
@never_cache
def upload_pdf(request):
    ctx = {}
    if request.method == "POST" and 'pdf' in request.FILES:
        f = request.FILES['pdf']
        if not f.name.lower().endswith('.pdf'):
            ctx['error'] = "Please upload a PDF file."
        else:
            # Save to a temporary path
            tmp_path = f"media/tmp_{request.user.id}_{int(time.time())}.pdf"
            with open(tmp_path, 'wb') as out:
                out.write(f.read())

            # Load PDF
            handler = get_pdf_handler()
            handler.load_pdf(tmp_path)

            # Save session + remove temp file
            request.session['pdf_loaded'] = True
            request.session['pdf_name'] = f.name
            request.session['pdf_hash'] = hashlib.md5(open(tmp_path, 'rb').read()).hexdigest()

            os.remove(tmp_path)  # clean up

            ctx['uploaded'] = True
            ctx['pdf_name'] = f.name

    return render(request, "upload_pdf.html", ctx)

@login_required
@csrf_exempt
def pdf_chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
        q = data.get("question", "").strip()
        if not q:
            return JsonResponse({"error": "Please enter a question"}, status=400)
        if not request.session.get("pdf_loaded"):
            return JsonResponse({"error": "Please upload a PDF first"}, status=400)

        handler = get_pdf_handler()
        ans = handler.answer_question(q)
        PdfQuestionAnswer.objects.create(
            user=request.user, pdf_name=request.session.get("pdf_name", ""),
            question=q, answer=ans
        )
        return JsonResponse({"answer": ans})
    except Exception as e:
        print("❌ PDF Chatbot error:", e)
        return JsonResponse({"error": "Internal server error"}, status=500)

@login_required
def pdf_qa_history(request):
    history = PdfQuestionAnswer.objects.filter(user=request.user).order_by("-timestamp")
    paginator = Paginator(history, 10)
    page = request.GET.get("page")
    return render(request, "pdf_qa_history.html", {
        "history": paginator.get_page(page),
        "is_paginated": paginator.num_pages > 1
    })



from django.views.decorators.http import require_POST

@require_POST
@login_required
def clear_pdf_history(request):
    PdfQuestionAnswer.objects.filter(user=request.user).delete()
    return redirect("pdf_qa_history")