import os
import sys
import pytest
import requests
import logging
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def pytest_configure(config):
    # Crear directorio para las capturas de pantalla si no existe
    screenshots_dir = 'reports/screenshots'
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    else:
        # Limpiar directorio de screenshots
        for file in os.listdir(screenshots_dir):
            file_path = os.path.join(screenshots_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.error(f"Error al eliminar {file_path}: {e}")
        logger.info("Directorio de screenshots limpiado exitosamente")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    logger.info("\n" + "="*80)
    logger.info("IMPORTANTE: En la proxima ejecucion de los tests, la carpeta 'reports/screenshots' sera vaciada")
    logger.info("="*80 + "\n")

@pytest.fixture(scope="function")
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    return session

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # Agregar información del entorno
        report.sections.append(("Environment", f"""
            Python: {sys.version}
            Platform: {sys.platform}
            Pytest: {pytest.__version__}
            Selenium: {webdriver.__version__}
            Requests: {requests.__version__}
        """))
        
        # Agregar logs
        report.sections.append(("Test Logs", f"""
            Test Name: {item.name}
            Status: {'Passed' if report.passed else 'Failed'}
            Duration: {report.duration:.2f} seconds
        """))

def pytest_runtest_setup(item):
    logger.info(f"\n{'='*80}\nIniciando test: {item.name}\n{'='*80}")

def pytest_runtest_call(item):
    logger.info(f"Ejecutando test: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    logger.info(f"Finalizando test: {item.name}\n{'='*80}")

def allure_attach_file(file_path, name, attachment_type):
    """Helper function para adjuntar archivos al reporte."""
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            logger.info(f"Archivo adjuntado: {name}")
    except Exception as e:
        logger.error(f"Error al adjuntar archivo {name}: {e}") 