from . import db
from datetime import datetime

class User(db.Model):
    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones (opcional)
    # posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        """Representación en string del objeto"""
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convierte el modelo a diccionario para JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def save(self):
        """Guarda el objeto en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Elimina el objeto de la base de datos"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        """Método de clase para buscar por username"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        """Método de clase para buscar por email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_all_active(cls):
        """Método de clase para obtener todos los usuarios activos"""
        return cls.query.filter_by(is_active=True).all()


# Ejemplo de modelo con relaciones
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación: Muchos posts pertenecen a un usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='posts', lazy=True)
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'published': self.published,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'author_id': self.user_id,
            'author_username': self.author.username if self.author else None
        }


# Ejemplo de tabla de asociación (Many-to-Many)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relación many-to-many con Post
    posts = db.relationship('Post', secondary='post_categories', backref='categories')
    
    def __repr__(self):
        return f'<Category {self.name}>'


# Tabla de asociación para many-to-many
post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)
