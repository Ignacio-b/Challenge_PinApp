import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import logging
import shutil
from datetime import datetime

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/logs/test_execution.log'),
        logging.StreamHandler()
    ]
)

@pytest.fixture(scope="function")
def driver(request):
    # Crear un directorio temporal único para los datos de usuario
    temp_dir = f"/tmp/chrome_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(temp_dir, exist_ok=True)
    
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Limpiar el directorio temporal después de cada test
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        logging.error(f"Error al limpiar directorio temporal: {e}")
    
    driver.quit()

@pytest.fixture(scope="function")
def api_client():
    session = requests.Session()
    yield session

def pytest_runtest_setup(item):
    """Hook que se ejecuta antes de cada test"""
    test_name = item.name
    logging.info(f"\n{'='*80}")
    logging.info(f"Iniciando test: {test_name}")
    logging.info(f"{'='*80}\n")

def pytest_runtest_teardown(item):
    """Hook que se ejecuta después de cada test"""
    test_name = item.name
    logging.info(f"\n{'='*80}")
    logging.info(f"Finalizando test: {test_name}")
    logging.info(f"{'='*80}\n")

def pytest_sessionstart(session):
    """Hook que se ejecuta al inicio de la sesión de pruebas"""
    # Crear directorios necesarios si no existen
    os.makedirs('reports/screenshots', exist_ok=True)
    os.makedirs('reports/logs', exist_ok=True)
    
    # Limpiar directorio de screenshots
    screenshots_dir = 'reports/screenshots'
    for file in os.listdir(screenshots_dir):
        file_path = os.path.join(screenshots_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            logging.error(f"Error al eliminar {file_path}: {e}")
    
    logging.info(f"\n{'='*80}")
    logging.info("IMPORTANTE: En la proxima ejecucion de los tests, la carpeta 'reports/screenshots' sera vaciada")
    logging.info(f"{'='*80}\n")

def pytest_runtest_makereport(item, call):
    """Hook que se ejecuta después de cada test para capturar screenshots"""
    if call.when == "call":
        driver = item.funcargs.get("driver")
        if driver:
            try:
                screenshot_name = f"{item.name}_{call.when}.png"
                screenshot_path = os.path.join('reports/screenshots', screenshot_name)
                driver.save_screenshot(screenshot_path)
                logging.info(f"Screenshot guardado: {screenshot_path}")
            except Exception as e:
                logging.error(f"Error al tomar screenshot: {e}")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Hook que se ejecuta al final de la sesión de pruebas"""
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    
    logging.info(f"\n{'='*80}")
    logging.info("RESUMEN DE EJECUCION:")
    logging.info(f"Tests Exitosos: {passed}")
    logging.info(f"Tests Fallidos: {failed}")
    logging.info(f"Tests con Error: {error}")
    logging.info(f"{'='*80}\n") 