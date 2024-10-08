"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from hello.views import  hola_mundo, get_qr_code

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hola_mundo, name='hola_mundo'),
    #path('send-whatsapp/', trigger_send_whatsapp_message, name='send_whatsapp'),
    path('get-qr-code/', get_qr_code, name='get_qr_code'),
    #path('show_input_value/<str:input_value>/', show_input_value, name='show_input_value'),
    #path('logs/', logsView, name='logs'),
    #path('send_whatsapp/', send_whatsapp_message, name='send_whatsapp_message'),

    
]
