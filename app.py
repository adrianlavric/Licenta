from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import io
import base64
import json
import logging
from datetime import datetime
import sqlite3
from werkzeug.utils import secure_filename
import uuid
from functools import wraps
import time
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flower_predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Te rog să te autentifici pentru a accesa această pagină.'
login_manager.login_message_category = 'info'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MODEL_PATH = 'models/model_flori_avansat.keras'
model = tf.keras.models.load_model(MODEL_PATH)
IMG_SIZE = (224, 224)

flower_classes = [
    "pink primrose", "hard-leaved pocket orchid", "canterbury bells", "sweet pea",
    "english marigold", "tiger lily", "moon orchid", "bird of paradise", "monkshood",
    "globe thistle", "snapdragon", "colt's foot", "king protea", "spear thistle",
    "yellow iris", "globe-flower", "purple coneflower", "peruvian lily", "balloon flower",
    "giant white arum lily", "fire lily", "pincushion flower", "fritillary",
    "red ginger", "grape hyacinth", "corn poppy", "prince of wales feathers",
    "stemless gentian", "artichoke", "sweet william", "carnation", "garden phlox",
    "love in the mist", "mexican aster", "alpine sea holly", "ruby-lipped cattleya",
    "cape flower", "great masterwort", "siam tulip", "lenten rose", "barbeton daisy",
    "daffodil", "sword lily", "poinsettia", "bolero deep blue", "wallflower",
    "marigold", "buttercup", "oxeye daisy", "common dandelion", "petunia",
    "wild pansy", "primula", "sunflower", "pelargonium", "bishop of llandaff",
    "gaura", "geranium", "orange dahlia", "pink-yellow dahlia", "cautleya spicata",
    "japanese anemone", "black-eyed susan", "silverbush", "californian poppy",
    "osteospermum", "spring crocus", "bearded iris", "windflower", "tree poppy",
    "gazania", "azalea", "water lily", "rose", "thorn apple", "morning glory",
    "passion flower", "lotus", "toad lily", "anthurium", "frangipani", "clematis",
    "hibiscus", "columbine", "desert-rose", "tree mallow", "magnolia", "cyclamen",
    "watercress", "canna lily", "hippeastrum", "bee balm", "ball moss",
    "foxglove", "bougainvillea", "camellia", "mallow", "mexican petunia",
    "bromelia", "blanket flower", "trumpet creeper", "blackberry lily"
]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    avatar_url = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')  # 'user', 'admin'

    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Setează parola criptată"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifică parola"""
        return check_password_hash(self.password_hash, password)

    def get_stats(self):
        """Obține statistici pentru utilizator"""
        total_predictions = len(self.predictions)
        correct_feedback = len([p for p in self.predictions if p.user_feedback == 'correct'])
        incorrect_feedback = len([p for p in self.predictions if p.user_feedback == 'incorrect'])

        return {
            'total_predictions': total_predictions,
            'correct_predictions': correct_feedback,
            'incorrect_predictions': incorrect_feedback,
            'accuracy': (correct_feedback / (correct_feedback + incorrect_feedback) * 100) if (
                                                                                                          correct_feedback + incorrect_feedback) > 0 else 0
        }

    def to_dict(self):
        """Convertește obiectul User la dicționar"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'role': self.role
        }


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # NULL pentru utilizatori neautentificați
    session_id = db.Column(db.String(36), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    predicted_class = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    all_predictions = db.Column(db.Text, nullable=False)  # JSON string
    image_path = db.Column(db.String(255), nullable=True)
    processing_time = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_feedback = db.Column(db.String(20), nullable=True)  # 'correct', 'incorrect', None


class FlowerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(100), unique=True, nullable=False)
    common_name = db.Column(db.String(100), nullable=True)
    family = db.Column(db.String(50), nullable=True)
    origin = db.Column(db.String(100), nullable=True)
    flowering_period = db.Column(db.String(50), nullable=True)
    colors = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    care_instructions = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validate_email(email):
    """Validează formatul email-ului"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validează puterea parolei"""
    if len(password) < 8:
        return False, "Parola trebuie să aibă cel puțin 8 caractere"
    if not re.search(r'[A-Z]', password):
        return False, "Parola trebuie să conțină cel puțin o literă mare"
    if not re.search(r'[a-z]', password):
        return False, "Parola trebuie să conțină cel puțin o literă mică"
    if not re.search(r'\d', password):
        return False, "Parola trebuie să conțină cel puțin o cifră"
    return True, "Parolă validă"


def timing_decorator(f):
    """Decorator pentru măsurarea timpului de execuție"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{f.__name__} executat în {end_time - start_time:.2f} secunde")
        return result

    return wrapper


def preprocess_image(img_data):
    """Preprocesează imaginea pentru predicție"""
    try:
        if ',' in img_data:
            img_data = img_data.split(',')[1]

        img_bytes = base64.b64decode(img_data)
        img = Image.open(io.BytesIO(img_bytes))

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img = img.resize(IMG_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalizare

        return img_array
    except Exception as e:
        logger.error(f"Eroare la preprocesarea imaginii: {e}")
        raise


def save_image(img_data, filename):
    """Salvează imaginea pe disk"""
    try:
        if ',' in img_data:
            img_data = img_data.split(',')[1]

        img_bytes = base64.b64decode(img_data)
        file_extension = os.path.splitext(filename)[1] or '.jpg'
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        with open(file_path, 'wb') as f:
            f.write(img_bytes)

        return file_path
    except Exception as e:
        logger.error(f"Eroare la salvarea imaginii: {e}")
        return None


def get_flower_info(scientific_name):
    """Obține informații despre o floare din baza de date"""
    flower = FlowerInfo.query.filter_by(scientific_name=scientific_name).first()
    if flower:
        return {
            'scientific_name': flower.scientific_name,
            'common_name': flower.common_name,
            'family': flower.family,
            'origin': flower.origin,
            'flowering_period': flower.flowering_period,
            'colors': flower.colors,
            'description': flower.description,
            'care_instructions': flower.care_instructions,
            'image_url': flower.image_url
        }
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Înregistrare utilizator nou"""
    if request.method == 'GET':
        return render_template('auth/register.html')

    try:
        data = request.json
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()

        if not username or len(username) < 3:
            return jsonify({'success': False, 'error': 'Username-ul trebuie să aibă cel puțin 3 caractere'}), 400

        if not validate_email(email):
            return jsonify({'success': False, 'error': 'Adresa de email nu este validă'}), 400

        password_valid, password_message = validate_password(password)
        if not password_valid:
            return jsonify({'success': False, 'error': password_message}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': 'Username-ul este deja folosit'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email-ul este deja folosit'}), 400

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        logger.info(f"Utilizator nou înregistrat: {username}")

        return jsonify({
            'success': True,
            'message': 'Contul a fost creat cu succes! Te poți autentifica acum.',
            'user': user.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la înregistrare: {e}")
        return jsonify({'success': False, 'error': 'Eroare la crearea contului'}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Autentificare utilizator"""
    if request.method == 'GET':
        return render_template('auth/login.html')

    try:
        data = request.json
        username_or_email = data.get('username', '').strip()
        password = data.get('password', '')
        remember_me = data.get('remember_me', False)

        if not username_or_email or not password:
            return jsonify({'success': False, 'error': 'Username/email și parola sunt obligatorii'}), 400

        user = User.query.filter(
            (User.username == username_or_email) |
            (User.email == username_or_email.lower())
        ).first()

        if not user or not user.check_password(password):
            return jsonify({'success': False, 'error': 'Username/email sau parolă incorectă'}), 401

        if not user.is_active:
            return jsonify({'success': False, 'error': 'Contul este dezactivat'}), 401

        login_user(user, remember=remember_me)
        user.last_login = datetime.utcnow()
        db.session.commit()

        logger.info(f"Utilizator autentificat: {user.username}")

        return jsonify({
            'success': True,
            'message': 'Autentificare reușită!',
            'user': user.to_dict()
        })

    except Exception as e:
        logger.error(f"Eroare la autentificare: {e}")
        return jsonify({'success': False, 'error': 'Eroare la autentificare'}), 500


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Deautentificare utilizator"""
    username = current_user.username
    logout_user()
    logger.info(f"Utilizator deautentificat: {username}")
    return jsonify({'success': True, 'message': 'Deautentificare reușită!'})


@app.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    """Profil utilizator"""
    if request.method == 'GET':
        stats = current_user.get_stats()
        return jsonify({
            'success': True,
            'user': current_user.to_dict(),
            'stats': stats
        })

    # Actualizare profil
    try:
        data = request.json

        if 'first_name' in data:
            current_user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            current_user.last_name = data['last_name'].strip()
        if 'avatar_url' in data:
            current_user.avatar_url = data['avatar_url'].strip()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Profilul a fost actualizat cu succes!',
            'user': current_user.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la actualizarea profilului: {e}")
        return jsonify({'success': False, 'error': 'Eroare la actualizarea profilului'}), 500


@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Schimbă parola utilizatorului"""
    try:
        data = request.json
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')

        if not current_user.check_password(current_password):
            return jsonify({'success': False, 'error': 'Parola curentă este incorectă'}), 400

        password_valid, password_message = validate_password(new_password)
        if not password_valid:
            return jsonify({'success': False, 'error': password_message}), 400

        current_user.set_password(new_password)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Parola a fost schimbată cu succes!'})

    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la schimbarea parolei: {e}")
        return jsonify({'success': False, 'error': 'Eroare la schimbarea parolei'}), 500


@app.route('/')
def index():
    """Pagina principală"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
@timing_decorator
def predict():
    """Rută pentru procesarea predicțiilor - cu suport pentru utilizatori autentificați"""
    start_time = time.time()

    try:
        data = request.json
        img_data = data['image']
        filename = data.get('filename', 'unknown.jpg')
        session_id = data.get('session_id', str(uuid.uuid4()))

        processed_image = preprocess_image(img_data)
        predictions = model.predict(processed_image)

        top_indices = predictions[0].argsort()[-5:][::-1]
        top_predictions = []

        for i in top_indices:
            class_name = flower_classes[i]
            confidence = float(predictions[0][i]) * 100
            top_predictions.append({
                'class': class_name,
                'confidence': confidence
            })

        image_path = save_image(img_data, filename) if data.get('save_image', False) else None
        processing_time = time.time() - start_time

        prediction = Prediction(
            user_id=current_user.id if current_user.is_authenticated else None,
            session_id=session_id,
            filename=secure_filename(filename),
            predicted_class=top_predictions[0]['class'],
            confidence=top_predictions[0]['confidence'],
            all_predictions=json.dumps(top_predictions),
            image_path=image_path,
            processing_time=processing_time
        )

        db.session.add(prediction)
        db.session.commit()

        logger.info(
            f"Predicție salvată: {top_predictions[0]['class']} ({top_predictions[0]['confidence']:.2f}%) - User: {current_user.username if current_user.is_authenticated else 'Anonim'}")

        result = {
            'success': True,
            'predictions': top_predictions,
            'flower_classes': flower_classes,
            'processing_time': round(processing_time, 3),
            'prediction_id': prediction.id
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Eroare la predicție: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/flower-info/<scientific_name>')
def flower_info(scientific_name):
    """Obține informații despre o floare"""
    try:
        info = get_flower_info(scientific_name)
        if info:
            return jsonify({'success': True, 'data': info})
        else:
            return jsonify({
                'success': False,
                'error': 'Informații indisponibile pentru această floare'
            }), 404
    except Exception as e:
        logger.error(f"Eroare la obținerea informațiilor florii: {e}")
        return jsonify({
            'success': False,
            'error': 'Eroare la obținerea informațiilor'
        }), 500


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Primește feedback de la utilizatori"""
    try:
        data = request.json
        prediction_id = data.get('prediction_id')
        feedback = data.get('feedback')  # 'correct' sau 'incorrect'

        if not prediction_id or feedback not in ['correct', 'incorrect']:
            return jsonify({
                'success': False,
                'error': 'Date de feedback invalide'
            }), 400

        prediction = Prediction.query.get(prediction_id)
        if not prediction:
            return jsonify({
                'success': False,
                'error': 'Predicția nu a fost găsită'
            }), 404

        prediction.user_feedback = feedback
        db.session.commit()

        logger.info(f"Feedback primit pentru predicția {prediction_id}: {feedback}")

        return jsonify({'success': True, 'message': 'Feedback salvat cu succes'})

    except Exception as e:
        logger.error(f"Eroare la salvarea feedback-ului: {e}")
        return jsonify({
            'success': False,
            'error': 'Eroare la salvarea feedback-ului'
        }), 500


@app.route('/statistics')
def get_statistics():
    """Obține statistici despre utilizare"""
    try:
        total_predictions = Prediction.query.count()
        correct_feedback = Prediction.query.filter_by(user_feedback='correct').count()
        incorrect_feedback = Prediction.query.filter_by(user_feedback='incorrect').count()

        total_feedback = correct_feedback + incorrect_feedback
        user_accuracy = (correct_feedback / total_feedback * 100) if total_feedback > 0 else 0

        predictions = Prediction.query.all()
        class_counts = {}
        for pred in predictions:
            class_name = pred.predicted_class
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        top_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        avg_processing_time = db.session.query(db.func.avg(Prediction.processing_time)).scalar() or 0

        stats = {
            'total_predictions': total_predictions,
            'user_accuracy': round(user_accuracy, 2),
            'feedback_count': {
                'correct': correct_feedback,
                'incorrect': incorrect_feedback,
                'total': total_feedback
            },
            'top_classes': top_classes,
            'avg_processing_time': round(avg_processing_time, 3),
            'total_classes': len(flower_classes)
        }

        return jsonify({'success': True, 'data': stats})

    except Exception as e:
        logger.error(f"Eroare la obținerea statisticilor: {e}")
        return jsonify({
            'success': False,
            'error': 'Eroare la obținerea statisticilor'
        }), 500


@app.route('/history/<session_id>')
def get_history(session_id):
    """Obține istoricul predicțiilor pentru o sesiune"""
    try:
        predictions = Prediction.query.filter_by(session_id=session_id) \
            .order_by(Prediction.timestamp.desc()) \
            .limit(50).all()

        history = []
        for pred in predictions:
            history.append({
                'id': pred.id,
                'filename': pred.filename,
                'predicted_class': pred.predicted_class,
                'confidence': pred.confidence,
                'all_predictions': json.loads(pred.all_predictions),
                'timestamp': pred.timestamp.isoformat(),
                'processing_time': pred.processing_time,
                'user_feedback': pred.user_feedback
            })

        return jsonify({'success': True, 'data': history})

    except Exception as e:
        logger.error(f"Eroare la obținerea istoricului: {e}")
        return jsonify({
            'success': False,
            'error': 'Eroare la obținerea istoricului'
        }), 500


@app.route('/health')
def health_check():
    """Health check pentru aplicație"""
    try:
        model_status = model is not None

        db_status = True
        try:
            db.session.execute('SELECT 1')
        except:
            db_status = False

        status = {
            'status': 'healthy' if (model_status and db_status) else 'unhealthy',
            'model_loaded': model_status,
            'database_connected': db_status,
            'total_classes': len(flower_classes),
            'timestamp': datetime.utcnow().isoformat()
        }

        return jsonify(status), 200 if status['status'] == 'healthy' else 503

    except Exception as e:
        logger.error(f"Eroare la health check: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@app.route('/my-history')
@login_required
def my_history():
    """Istoricul personal al utilizatorului autentificat"""
    try:
        predictions = Prediction.query.filter_by(user_id=current_user.id) \
            .order_by(Prediction.timestamp.desc()) \
            .limit(50).all()

        history = []
        for pred in predictions:
            history.append({
                'id': pred.id,
                'filename': pred.filename,
                'predicted_class': pred.predicted_class,
                'confidence': pred.confidence,
                'all_predictions': json.loads(pred.all_predictions),
                'timestamp': pred.timestamp.isoformat(),
                'processing_time': pred.processing_time,
                'user_feedback': pred.user_feedback
            })

        return jsonify({'success': True, 'data': history})

    except Exception as e:
        logger.error(f"Eroare la obținerea istoricului personal: {e}")
        return jsonify({
            'success': False,
            'error': 'Eroare la obținerea istoricului'
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Resursa nu a fost găsită'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'error': 'Eroare internă a serverului'}), 500


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({'success': False, 'error': 'Fișierul este prea mare'}), 413


def init_db():
    """Inițializează baza de date"""
    with app.app_context():
        db.create_all()
        logger.info("Baza de date inițializată")


def init_db():
    """Inițializează baza de date"""
    with app.app_context():
        db.create_all()
        logger.info("Baza de date inițializată")

        # Creează un admin implicit dacă nu există
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@flowerscan.com',
                first_name='Administrator',
                last_name='FlowerScan',
                role='admin'
            )
            admin.set_password('Admin123.')
            db.session.add(admin)
            db.session.commit()
            logger.info("Cont admin creat cu succes")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)