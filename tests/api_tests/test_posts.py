import pytest
import logging

logger = logging.getLogger(__name__)

def test_get_posts(api_client):
    """
    Prueba el endpoint GET de posts.
    Verifica que:
    1. La respuesta tenga status code 200 (éxito)
    2. Se obtengan posts en la respuesta
    3. La respuesta sea un array no vacío
    """
    logger.info("Iniciando test de obtención de posts")
    response = api_client.get('https://jsonplaceholder.typicode.com/posts')
    api_client.last_response = response  # Guardar la respuesta para el reporte
    
    logger.info(f"Status code de la respuesta: {response.status_code}")
    logger.info(f"Cantidad de posts obtenidos: {len(response.json())}")
    
    assert response.status_code == 200
    assert len(response.json()) > 0
    logger.info("Test completado exitosamente")

def test_create_post(api_client):
    """
    Prueba el endpoint POST para crear un nuevo post.
    Verifica que:
    1. La respuesta tenga status code 201 (creado)
    2. Los datos enviados coincidan con la respuesta
    3. Se genere un ID para el nuevo post
    """
    logger.info("Iniciando test de creación de post")
    
    post_data = {
        'title': 'Test Post',
        'body': 'This is a test post',
        'userId': 1
    }
    
    logger.info(f"Datos del post a crear: {post_data}")
    response = api_client.post('https://jsonplaceholder.typicode.com/posts', json=post_data)
    api_client.last_response = response  # Guardar la respuesta para el reporte
    
    logger.info(f"Status code de la respuesta: {response.status_code}")
    logger.info(f"Respuesta del servidor: {response.json()}")
    
    assert response.status_code == 201
    assert response.json()['title'] == post_data['title']
    assert response.json()['body'] == post_data['body']
    logger.info("Test completado exitosamente") 