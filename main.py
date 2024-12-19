
from flask import Flask
from routes.books import books_bp
from routes.members import members_bp
from routes.search import search_bp
from auth import auth_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(books_bp)
app.register_blueprint(members_bp)
app.register_blueprint(search_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
