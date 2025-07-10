from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('api/chatbot/', views.chatbot_response, name='chat_ui_response'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.chat_history, name='chat-history'),
    path('clear-history/', views.clear_history, name='clear-history'),
    path('profile/', views.profile_view, name='profile'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('api/pdf-chat/', views.pdf_chatbot_response, name='pdf_chatbot_response'),
    path('pdf-qa-history/', views.pdf_qa_history, name='pdf_qa_history'),
    path('clear-pdf-history/', views.clear_pdf_history, name='clear-pdf-history'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
