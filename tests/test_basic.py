import pytest
from app import create_app, db
from app.models import User, Project

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup(client, app):
    response = client.post('/auth/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'role': 'Admin'
    })
    assert response.status_code == 302 # redirect to login
    
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.email == 'test@example.com'
        assert user.is_admin()

def test_login(client, app):
    # Create user first
    with app.app_context():
        u = User(username='testuser', email='test@example.com', role='Admin')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()
        
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 302 # redirect to dashboard
    
    # Try accessing protected route
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_unauthorized_access(client):
    response = client.get('/dashboard')
    assert response.status_code == 302 # redirects to login
    assert b'/auth/login' in response.data
