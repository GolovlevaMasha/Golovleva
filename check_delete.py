import sys
sys.path.append('.')
from src.main import app

print("Все маршруты приложения:")
for route in app.routes:
    if hasattr(route, 'path'):
        methods = getattr(route, 'methods', set())
        if 'DELETE' in methods:
            print(f"  DELETE {route.path}")
