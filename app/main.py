from backend import create_app
from backend.views.error.error import not_found

app = create_app()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
    