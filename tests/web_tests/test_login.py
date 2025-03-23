import pytest
import logging
from datetime import datetime
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

logger = logging.getLogger(__name__)

def get_screenshot_name(test_name, step):
    """
    Genera un nombre único para las capturas de pantalla.
    Args:
        test_name: Nombre del test que está ejecutándose
        step: Paso del test (before_login/after_login)
    Returns:
        str: Ruta completa del archivo de captura
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"reports/screenshots/{test_name}_{step}_{timestamp}.png"

def test_login_successful(driver):
    """
    Prueba el flujo de login exitoso.
    Verifica que:
    1. Se pueda acceder a la página de login
    2. Se pueda hacer login con credenciales válidas
    3. Se redirija a la página de productos
    4. La página de productos sea visible
    """
    logger.info("Iniciando test de login exitoso")
    
    # Inicializa los objetos de página necesarios
    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)
    
    # Navega a la página de login
    logger.info("Navegando a la página de login")
    driver.get("https://www.saucedemo.com/")
    
    # Toma captura del estado inicial
    logger.info("Tomando captura de pantalla antes del login")
    driver.save_screenshot(get_screenshot_name("test_login_successful", "before_login"))
    
    # Realiza el login con credenciales válidas
    logger.info("Intentando login con credenciales válidas")
    login_page.login("standard_user", "secret_sauce")
    
    # Toma captura del estado después del login
    logger.info("Tomando captura de pantalla después del login")
    driver.save_screenshot(get_screenshot_name("test_login_successful", "after_login"))
    
    # Verifica que se haya redirigido a la página de productos
    logger.info("Verificando que estamos en la página de productos")
    assert products_page.is_products_page_visible()
    logger.info("Test completado exitosamente")

def test_login_failed(driver):
    """
    Prueba el flujo de login fallido.
    Verifica que:
    1. Se pueda acceder a la página de login
    2. Al usar credenciales inválidas se muestre el mensaje de error
    3. El mensaje de error sea el correcto
    """
    logger.info("Iniciando test de login fallido")
    
    # Inicializa el objeto de página de login
    login_page = LoginPage(driver)
    
    # Navega a la página de login
    logger.info("Navegando a la página de login")
    driver.get("https://www.saucedemo.com/")
    
    # Toma captura del estado inicial
    logger.info("Tomando captura de pantalla antes del login fallido")
    driver.save_screenshot(get_screenshot_name("test_login_failed", "before_login"))
    
    # Intenta hacer login con credenciales inválidas
    logger.info("Intentando login con credenciales inválidas")
    login_page.login("invalid_user", "invalid_password")
    
    # Toma captura del mensaje de error
    logger.info("Tomando captura de pantalla del mensaje de error")
    driver.save_screenshot(get_screenshot_name("test_login_failed", "after_login"))
    
    # Verifica que se muestre el mensaje de error correcto
    logger.info("Verificando mensaje de error")
    assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
    logger.info("Test completado exitosamente") 