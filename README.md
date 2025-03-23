# Proyecto de Testing Automatizado

Este proyecto contiene pruebas automatizadas para una aplicación web y una API pública.

## Estructura del Proyecto

```
├── tests/
│   ├── web_tests/
│   │   ├── test_base.py
│   │   └── test_login.py
│   └── api_tests/
│       ├── test_api_base.py
│       └── test_posts.py
├── pages/
│   ├── login_page.py
│   └── products_page.py
├── utils/
│   └── driver_factory.py
├── reports/
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de Pruebas

Para ejecutar todas las pruebas:
```bash
pytest --html=reports/report.html
```

## Casos de Prueba

### Pruebas Web (Sauce Demo)
1. Login exitoso y verificación de productos
   - Verificar que se puede iniciar sesión con credenciales válidas
   - Verificar que se muestra la página de productos
2. Login fallido
   - Verificar que se muestra mensaje de error con credenciales inválidas

### Pruebas API (JSONPlaceholder)
1. Obtener posts
   - Verificar que se pueden obtener todos los posts
   - Verificar la estructura de la respuesta
2. Crear post
   - Verificar que se puede crear un nuevo post
   - Verificar que la respuesta contiene los datos correctos 