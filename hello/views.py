from django.http import HttpResponse
from django.shortcuts import render
import logging
from playwright.sync_api import sync_playwright

def send_whatsapp_message(phone_number, message):
    from playwright.sync_api import sync_playwright
    import time
    import os

    try:
        with sync_playwright() as p:
            try:
                
                browser = p.chromium.launch_persistent_context(user_data_dir='ws_data', headless=False)
            except Exception as e:
                logging.error(f"Error launching browser: {e}")
                logging.info("Attempting to install Playwright browsers...")
                
                browser = p.chromium.launch_persistent_context(user_data_dir='ws_data', headless=False)

            page = browser.new_page()
            whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
            page.goto(whatsapp_url)
            page.wait_for_load_state("networkidle")
            if "Escanea el código QR" in page.content():
                logging.info("Escanea el código QR de WhatsApp Web")
                time.sleep(15)
            try:
                # page.wait_for_selector("div[data-tab='1']", timeout=60000)
                time.sleep(30)
                page.keyboard.press("Enter")
                time.sleep(15)
            except Exception as e:
                logging.error(f"Error sending message: {e}")
            finally:
                browser.close()
    except Exception as e:
        logging.error(f"Error in send_whatsapp_message: {e}")

# Create your views here.
def hola_mundo(request):
    context = {
        'mensaje': 'Hola Mundo!'

    }
    return render(request, 'main.html', context)

def trigger_send_whatsapp_message(request):
    if request.method == 'POST':
        send_whatsapp_message("+528130733175", "Hola, soy un mensaje de prueba")
        return HttpResponse("Mensaje de WhatsApp enviado con éxito")
    return HttpResponse("Método no permitido", status=405)