from models import User
from views import db

def login(self, name, password):
    return self.app.post('/', data=dict(
        name=name, password=password), follow_redirects=True)

def register(self, name, email, password, confirm):
    return self.app.post(
        'register/',
        data=dict(name=name, email=email, password=password, confirm=confirm),
        follow_redirects=True
    )

def logout(self):
    return self.app.get('logout/', follow_redirects=True)

def create_user(self, name, email, password):
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

def create_task(self):
    return self.app.post('add/', data=dict(
        name='Go to the bank',
        due_date='02/05/2015',
        priority='1',
        posted_date='02/04/2015',
        status='1'
    ), follow_redirects=True)

def create_admin_user(self):
    new_user = User(
        name='Superman',
        email='admin@realpython.com',
        password='allpowerful',
        role='admin'
    )
    db.session.add(new_user)
    db.session.commit()
