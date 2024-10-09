
#from asyncio.log import logger

#from django.http import HttpResponse
from django.shortcuts import redirect, render
#import logging
from django.urls import reverse
#from playwright.sync_api import sync_playwright
#from playwright.async_api import async_playwright
import time
from django.http import StreamingHttpResponse
from django.http import HttpResponseBadRequest
import pywhatkit

from datetime import datetime

#Configurar el logger
#logger = logging.getLogger('hello')  # Reemplaza 'myapp' con el nombre de tu aplicación


"""
def get_qr_code(request):
    phone_number = "+528130733175"
    message = "Hola, este es un mensaje de prueba."
    
    browser = None

    with sync_playwright() as p:
        try:
            browser = p.firefox.launch_persistent_context(
                user_data_dir='ws_data',
                headless=True,
                #user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            )
            page = browser.new_page()
            whatsapp_url = "https://web.whatsapp.com/"
            logger.info(f"Navegando a la URL de WhatsApp: {whatsapp_url}")
      
            
            # Navegar a WhatsApp Web
            page.goto(whatsapp_url, timeout=10000)
            page.wait_for_load_state("networkidle")
            logger.info("Página cargada, verificando autenticación")
                        
            # Verificar si ya estamos autenticados
            try:
                page.wait_for_selector("div[data-tab='3']", timeout=10000)
                logger.info("Ya autenticado en WhatsApp")
                # Función A: Ya autenticado
                send_message(page, phone_number, message)
            except:
                logger.info("No autenticado en WhatsApp")
                # Función B: No autenticado
                authenticate_whatsapp(page)
                
                logger.info("--------Terminando ----------")
            
        except Exception as e:
            logger.error(f"Error al navegar a la URL de WhatsApp: {e}")
        finally:
            if browser:
                browser.close()
                logger.info("Cerrando el navegador")

    return render(request, 'qr_code.html')


def send_message(page, phone_number, message):
    logger.info(f"Inicia Función Send Message; Enviando mensaje a {phone_number}: {message}")
    try:
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        page.goto(whatsapp_url, timeout=30000)
        page.wait_for_load_state("networkidle")
        logger.info("Página de mensaje cargada, enviando mensaje")
        
        
        time.sleep(10)
        
        # Tomar una captura de pantalla antes de presionar "Enter"
        logger.info(f"Captura de pantalla tomada antes de presionar Enter: {screenshot_path}")
                
        # Simular la acción de presionar "Enter"
        page.keyboard.press("Enter")
        logger.info("Presionando Enter para enviar el mensaje")
        time.sleep(5)
        # Esperar a que el mensaje sea enviado
        page.wait_for_selector("div._aigv._aigw", timeout=20000)
        screenshot_path = "after_enter_screenshot.png"
        page.screenshot(path=screenshot_path)

        logger.info("Mensaje enviado y etiqueta detectada.")
    except Exception as e:
        logger.error(f"Error al enviar el mensaje: {e}")c


def authenticate_whatsapp(page):
    try:
        logger.info(" -------- 1/9 Inicio Esperando autenticación ----------- ")
        
        # Navegar a WhatsApp Web
        page.goto("https://web.whatsapp.com/")
        
        # Esperar a que el div con la clase _aj-e esté presente
        page.wait_for_selector("div._aj-e", timeout=10000)
        time.sleep(8)
        # Buscar el span con role="button" y clase x1n68mz9 dentro del div con clase _aj-e
        span_selector = "span.x1n68mz9"
        span_element = page.query_selector(span_selector)
        span_element.click()
        #page.wait_for_selector(span_selector, timeout=30000)
        page.screenshot(path="static/span2.png")
        #page.wait_for_selector(span_element, timeout=10000)
        try:
            time.sleep(5)
            
            logger.info(" -------- 2/9 Inicio Clic en el span ----------- ")
            
            #span que contiene lac clave del país de número de teléfono
            span_value_number = "span.x19co3pv"
            page.wait_for_selector(span_value_number, timeout=10000)
            span_element_number = page.query_selector(span_value_number)
            pan_text = span_element_number.text_content()
            
            logger.info(f" -------- 2/9 Terminar Span encontrado {pan_text} ----------- ")

            #agregar número de teléfono al input, primero identificar el input
            input_selector = 'input[dir="ltr"]'
            page.wait_for_selector(input_selector, timeout=10000)
            input_element_number = page.query_selector(input_selector)
            input_element_number.fill("+52 81 8075 1211")

            logger.info(f" <-------- 2/9 Terminar Input con dir='ltr' encontrado {input_element_number} -----------> ")

            try:
                logger.info(" -------- 3/9 Inicio Llenar input con número de teléfono ----------- ")

                #hacer clic en el botón para continuar
                button_selector = "button.x889kno.x1a8lsjc.xbbxn1n.xxbr6pl.x1n2onr6.x1rg5ohu.xk50ysn.x1f6kntn.xyesn5m.x1z11no5.xjy5m1g.x1mnwbp6.x4pb5v6.x178xt8z.xm81vs4.xso031l.xy80clv.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x1v8p93f.xogb00i.x16stqrj.x1ftr3km.x1hl8ikr.xfagghw.x9dyr19.x9lcvmn.xbtce8p.x14v0smp.xo8ufso.xcjl5na.x1k3x3db.xuxw1ft.xv52azi"
                page.wait_for_selector(button_selector, timeout=10000)
                button_element = page.query_selector(button_selector)
                button_element.click()

                logger.info(" -------- 3/9 Terminar Llenar input con número de teléfono ----------- ")

                try:
                    logger.info(" -------- 4/9 Inicio Clic en el botón ----------- ")
                    
                    #seleccionar el div que contiene el atributo data-link-code
                    div_selector = 'div[data-link-code]'
                    page.wait_for_selector(div_selector, timeout=20000)
                    div_element = page.query_selector(div_selector)
                    get_code_ws = div_element.get_attribute('data-link-code')
                    
                    logger.info(f"Codigo: {get_code_ws}")
                    
                    time.sleep(60)
                    #html_element_wp = page.query_selector("div._aigv._aigw")
                    #page.wait_for_selector("div._aigv._aigw", timeout=10000)
                    logger.info(" -------- 4/9 Terminar Clic en el botón ----------- ")
                except Exception as e:
                    logger.error(f" ------- 4/9 Error al obtener el valor del atributo data-link-code: {e}")

            except Exception as e:
                logger.error(f" ------- 3/9 Error al llenar el input con el número de teléfono: {e}")

        except Exception as e:
            logger.error(f" ------- 2/9 Error al hacer clic en el span: {e}")
    except Exception as e:
        logger.error(f"------ 1/9 --- Error durante la autenticación en la función inside_whatsapp: {e}")
        return None


"""


def hola_mundo(request):
    context = {
        'mensaje': 'Hola Mundo!'
    }
    return render(request, 'main.html', context)


def send_whatsapp_message(request):
    #phone_number = request.GET.get('phone_number')
    #message = request.GET.get('message')


    phone_number = "+528130733175"
    message = "Hola, este es un mecdfsac nsaje de prueba."

    # Obtener la hora y minuto actuales
    now = datetime.now()
    hour = now.hour
    minute = now.minute + 2

    print(f"Enviando mensaje a {phone_number} a las {hour}:{minute}")

    try:
        # Enviar el mensaje instantáneamente
        pywhatkit.sendwhatmsg(phone_number, message, hour, minute, wait_time=20, tab_close=False, close_time=10)
        print("Mensaje enviado exitoscdfsacdsac fvfdsa dsamente.")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
    
    return render(request, 'main.html')