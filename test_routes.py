import sys
sys.path.append('.')
from src.main import app

# Выводим все пути
print("Все маршруты приложения:")
for route in app.routes:
    if hasattr(route, 'path'):
        methods = getattr(route, 'methods', ['ANY'])
        endpoint = getattr(route, 'endpoint', 'Unknown')
        print(f"  {route.path} - {methods}")
        print(f"    Endpoint: {endpoint}")
        print()
