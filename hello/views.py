
from asyncio.log import logger
from django.http import HttpResponse
from django.shortcuts import redirect, render
import logging
from django.urls import reverse
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import time

#Configurar el logger
logger = logging.getLogger('hola')  # Reemplaza 'myapp' con el nombre de tu aplicación


def get_qr_code(request):
    phone_number = "+528130733175"
    message = "Hola, este es un mensaje de prueba."
    screenshot_path = "static/qr_code_screenshot.png"
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
                authenticate_and_send_message(page, phone_number, message)
            
        except Exception as e:
            logger.error(f"Error al navegar a la URL de WhatsApp: {e}")
        finally:
            if browser:
                browser.close()
                logger.info("Cerrando el navegador")

    return render(request, 'qr_code.html')


def send_message(page, phone_number, message):
    try:
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        page.goto(whatsapp_url, timeout=40000)
        page.wait_for_load_state("networkidle")
        logger.info("Página de mensaje cargada, enviando mensaje")
        
        time.sleep(10)
        
        # Tomar una captura de pantalla antes de presionar "Enter"
        screenshot_path = "before_enter_screenshot.png"
        page.screenshot(path=screenshot_path)
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
        logger.error(f"Error al enviar el mensaje: {e}")


def authenticate_and_send_message(page, phone_number, message):
    try:
        logger.info("Esperando autenticación del usuario")
        # Esperar a que el usuario se autentique manualmente
        
        page.goto("https://web.whatsapp.com/")  # Reemplaza con la URL correcta

        # Esperar a que el div con la clase _aj-e esté presente
        page.wait_for_selector("div._aj-e", timeout=10000)
        time.sleep(8)
        # Buscar el span con role="button" y clase x1n68mz9 dentro del div con clase _aj-e
        span_selector = "span.x1n68mz9"
        span_element = page.query_selector(span_selector)
        span_element.click()
        if span_element:
            print("Span encontrado")
            # Realizar una acción sobre el span, por ejemplo, hacer clic
            
            time.sleep(10)
             
            #
            # Tomar una captura de pantalla después de la autenticación

            span_element_number = page.query_selector("span.x19co3pv")
            page.wait_for_selector("span.x19co3pv")
            pan_text = span_element_number.text_content()
            time.sleep(10)
            print(pan_text)

            input_selector = 'input[dir="ltr"]'
            page.wait_for_selector(input_selector, timeout=50000)

            input_element_number = page.query_selector(input_selector)

            if input_element_number:
                print("Input con dir='ltr' encontrado")
                time.sleep(5)
                # Puedes realizar más acciones con el input aquí, por ejemplo, llenarlo con texto
                input_element_number.fill("+52 81 3073 3175")

                button_selector = "button.x889kno.x1a8lsjc.xbbxn1n.xxbr6pl.x1n2onr6.x1rg5ohu.xk50ysn.x1f6kntn.xyesn5m.x1z11no5.xjy5m1g.x1mnwbp6.x4pb5v6.x178xt8z.xm81vs4.xso031l.xy80clv.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x1v8p93f.xogb00i.x16stqrj.x1ftr3km.x1hl8ikr.xfagghw.x9dyr19.x9lcvmn.xbtce8p.x14v0smp.xo8ufso.xcjl5na.x1k3x3db.xuxw1ft.xv52azi"

                button_element = page.query_selector(button_selector)
                if button_element:
                    button_element.click()
                    print("Botón con clase x889kno clicado")
                    div_selector = 'div[data-link-code]'
                    time.sleep(5)
                    page.wait_for_selector(div_selector, timeout=60000)
                    div_element = page.query_selector(div_selector)

                    if div_element:
                        data_link_code_value = div_element.get_attribute('data-link-code')
                        
                        print(f"Valor del atributo data-link-code: {data_link_code_value}")
                        time.sleep(30)
                        html_element_wp = page.query_selector("div._aigv._aigw")
                        if html_element_wp:
                            page.wait_for_selector("div._aigv._aigw", timeout=60000)
                            print("Etiqueta <html> con id 'whatsapp-web' detectada.")
                        else:
                            print("Etiqueta <html> con id 'whatsapp-web' no encontrada.")
                    else:
                        print("Div con atributo data-link-code no encontrado")                          
                else:
                    print("Botón con clase x889kno no encontrado")
            else:
                print("Input con dir='ltr' no encontrado")      
            time.sleep(3)
            print(pan_text)
            print("terminando el span")
        else:
            print("Span no encontrado")

        logger.info("Autenticación completada, enviando mensaje")
        send_message(page, phone_number, message)
    except Exception as e:
        logger.error(f"Error durante la autenticación: {e}")
    
# Create your views here.
def hola_mundo(request):
    context = {
        'mensaje': 'Hola Mundo!'
    }
    return render(request, 'main.html', context)