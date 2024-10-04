import asyncio
from asyncio.log import logger
from django.http import HttpResponse
from django.shortcuts import render
import logging
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import time

# Configurar el logger
logger = logging.getLogger('myapp')  # Reemplaza 'myapp' con el nombre de tu aplicación


def get_qr_code(request):
    phone_number = "+528130733175"
    message = "Hola, este es un mensaje de prueba."
    with sync_playwright() as p:
        try:
            browser = p.firefox.launch_persistent_context(user_data_dir='ws_data', headless=True)
            page = browser.new_page()
            whatsapp_url = "https://web.whatsapp.com/"
            logger.info(f"Navegando a la URL de WhatsApp: {whatsapp_url}")
            
            # Navegar a WhatsApp Web
            page.goto(whatsapp_url, timeout=60000)
            page.wait_for_load_state("networkidle")
            logger.info("Página cargada, verificando autenticación")
            
            # Esperar un momento para que la página cargue completamente
            time.sleep(10)
            
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
        page.wait_for_selector("div._aj-e", timeout=60000)
        time.sleep(2)
        # Buscar el span con role="button" y clase x1n68mz9 dentro del div con clase _aj-e
        span_selector = "span.x1n68mz9"
        span_element = page.query_selector(span_selector)
        span_element.click()
        if span_element:
            print("Span encontrado")
            # Realizar una acción sobre el span, por ejemplo, hacer clic
            
            time.sleep(3)
             
            page.wait_for_selector("span.x19co3pv", timeout=50000)
            span_element_number = page.query_selector("span.x19co3pv")
            pan_text = span_element_number.text_content()
            time.sleep(4)
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
    

"""
def get_qr_code(request):
    phone_number = "+528130733175"
    message = "esto es vuicbdsua hcñ dshoia hcdios chids ahidco sñahicdo aijcod ñajic dosñaj idsa ñcdisac dsapjc disjc disaj c{d sapi}."
    with sync_playwright() as p:
    
        try:
            browser = p.firefox.launch_persistent_context(user_data_dir='ws_data', headless=True)
            page = browser.new_page()
            whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
            logger.info(f"Navegando a la URL de WhatsApp: {whatsapp_url}")
            
            # Aumentar el tiempo de espera para la navegación
            page.goto(whatsapp_url, timeout=20000)
            page.wait_for_load_state("networkidle")
            logger.info("Página cargada, enviando mensaje")
            
            time.sleep(10)
            screenshot_path = "before_enter_screenshot.png"
            page.screenshot(path=screenshot_path)

            div_selector_load = "div._ak9t"
            charge_page_login = page.wait_for_selector(div_selector_load, timeout=20000)
            selected_div_login = page.query_selector(div_selector_load)

            if selected_div_login==False:
                print("Please scan the QR code to log in.")
                logger.info("Por favor, escanea el código QR para iniciar sesión.")

            logger.info(f"Captura de pantalla tomada antes de presionar Enter: {screenshot_path}")
            # Hacer clic en el botón de enviar
            time.sleep(10)
            
            page.keyboard.press("Enter")

            page.screenshot(path="screenshot_path_despuesdelenter.png")
            logger.info(f"Captura de pantalla tomada antes de presionar Enter: {screenshot_path}")
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"Error al navegar a la URL de WhatsApp: {e}")
            
        finally:
            browser.close()
            logger.info("Cerrando el navegador")

    return render(request, 'qr_code.html')
"""


"""

def get_qr_code(request):
    phone_number = "+528130733175"
    message = "Hola, este es un mensaje de prueba."
    with sync_playwright() as p:

                
        browser = p.chromium.launch_persistent_context(user_data_dir='ws_data', headless=True)

        page = browser.new_page()
        whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
        page.goto(whatsapp_url)
        page.wait_for_load_state("networkidle")
        logger.info("Navegando a la URL de WhatsApp y enviando mensaje", whatsapp_url)

        try:
            page.wait_for_selector("div[data-tab='1']", timeout=20000)
            
            page.keyboard.press("Enter")
                
            page.wait_for_selector("div._aigv._aigw", timeout=20000)
            print("Etiqueta <html> con id 'whatsapp-web' detectada.")
        except Exception as e:
            logging.error(f"Error sending message: {e}")
        finally:
            browser.close()
    
    logger.info("Cerrando el navegador")

    return render(request, 'qr_code.html')



"""



async def send_whatsapp_message_asc(phone_number, message):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Navegar a WhatsApp Web
        await page.goto("https://web.whatsapp.com")

        # Esperar a que el usuario se autentique
        try:
            await page.wait_for_selector("div._ak96", timeout=15000)
            print("Please scan the QR code to log in.")
            await page.wait_for_selector("span._aka-", timeout=60000)
            
            #await page.wait_for_selector("div[data-tab='3']", timeout=60000)
            await page.screenshot(path="qr_code_screenshot3.png")
        except:
            print("Already authenticated or timeout reached.")

        # Navegar a la URL de WhatsApp con el número y el mensaje
        whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
        await page.goto(whatsapp_url)

        # Esperar a que el botón de enviar esté disponible y hacer clic
        await page.wait_for_selector("a[href*='send']", timeout=10000)
        await page.click("a[href*='send']")

        # Esperar a que el mensaje sea enviado
        await page.wait_for_selector("span[data-icon='msg-dblcheck']", timeout=10000)
        print("Message sent successfully.")

        await browser.close()


def send_whatsapp_message(phone_number, message):
    try:
        with sync_playwright() as p:
            try:
                

                browser = p.firefox.launch_persistent_context(user_data_dir='ws_data', headless=False)
            except Exception as e:
                logging.error(f"Error launching browser: {e}")
                logging.info("Attempting to install Playwright browsers...")
                
                browser = p.chromium.launch_persistent_context(user_data_dir='ws_data', headless=False)

            page = browser.new_page()
            
            whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
            page.goto(whatsapp_url)
            print("here 1")
            page.screenshot(path="screenshot_initial_click.png")
            page.wait_for_load_state("networkidle")
            
            print("here 2")
            # Capturar una captura de pantalla para depuración
            statu_code = page.query_selector("div._aigv")
            
            if statu_code:
                print("Escanea el código QR" )
                logging.info("Escanea el código QR de WhatsApp Web")
                time.sleep(15)
            try:
                page.wait_for_selector("div[data-tab='1']", timeout=60000)
                page.screenshot(path="screenshot_before_click_0.png")
                time.sleep(30)
                page.screenshot(path="screenshot_before_click_40.png")
                page.keyboard.press("Enter")
                time.sleep(15)
                page.wait_for_selector("div._aigv._aigw", timeout=60000)
                print("Etiqueta <html> con id 'whatsapp-web' detectada.")
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
        #send_whatsapp_message("+528130733175", "Hola, soy un mensaje de prueba")
        asyncio.run(send_whatsapp_message_asc("+528130733175", "Hola, soy un mensaje de prueba"))
        return HttpResponse("Mensaje de WhatsApp enviado con éxito")
    return HttpResponse("Método no permitido", status=405)

"""


def get_qr_code(request):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto("https://web.whatsapp.com/")  # Reemplaza con la URL correcta

        # Esperar a que el div con la clase _aj-e esté presente
        page.wait_for_selector("div._aj-e", timeout=60000)
        time.sleep(2)
        # Buscar el span con role="button" y clase x1n68mz9 dentro del div con clase _aj-e
        span_selector = "span.x1n68mz9"
        span_element = page.query_selector(span_selector)
        span_element.click()
        if span_element:
            print("Span encontrado")
            # Realizar una acción sobre el span, por ejemplo, hacer clic
            
            time.sleep(3)
             
            page.wait_for_selector("span.x19co3pv", timeout=50000)
            span_element_number = page.query_selector("span.x19co3pv")
            pan_text = span_element_number.text_content()
            time.sleep(4)
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

        whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
        page.goto(whatsapp_url)
    return render(request, 'qr_code.html')
"""