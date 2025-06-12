import sqlite3
import os
import shutil
from datetime import datetime
from werkzeug.security import generate_password_hash


def backup_database():
    """Creează o copie de backup a bazei de date"""
    db_file = 'flower_predictions.db'
    if os.path.exists(db_file):
        backup_file = f'flower_predictions_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        shutil.copy2(db_file, backup_file)
        print(f"✅ Backup creat: {backup_file}")
        return backup_file
    return None


def check_existing_tables():
    """Verifică ce tabele există în baza de date"""
    try:
        conn = sqlite3.connect('flower_predictions.db')
        cursor = conn.cursor()

        print("Verific tabelele existente...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        print(f"Tabele găsite: {tables}")

        conn.close()
        return tables

    except Exception as e:
        print(f"Eroare la verificarea tabelelor: {e}")
        return []


def create_complete_database():
    """Creează schema completă a bazei de date"""

    backup_file = backup_database()

    try:
        conn = sqlite3.connect('flower_predictions.db')
        cursor = conn.cursor()

        print("Creez schema completă a bazei de date...")

        print("Creez tabelul user...")
        cursor.execute('DROP TABLE IF EXISTS user;')
        cursor.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(200) NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                avatar_url VARCHAR(200),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                is_active BOOLEAN DEFAULT 1,
                role VARCHAR(20) DEFAULT 'user'
            )
        ''')
        print("Tabelul user creat")

        print("Creez tabelul prediction...")
        cursor.execute('DROP TABLE IF EXISTS prediction;')
        cursor.execute('''
            CREATE TABLE prediction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_id VARCHAR(36) NOT NULL,
                filename VARCHAR(255) NOT NULL,
                predicted_class VARCHAR(100) NOT NULL,
                confidence FLOAT NOT NULL,
                all_predictions TEXT NOT NULL,
                image_path VARCHAR(255),
                processing_time FLOAT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_feedback VARCHAR(20),
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')
        print("Tabelul prediction creat")

        print("Creez tabelul flower_info...")
        cursor.execute('DROP TABLE IF EXISTS flower_info;')
        cursor.execute('''
            CREATE TABLE flower_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scientific_name VARCHAR(100) UNIQUE NOT NULL,
                common_name VARCHAR(100),
                family VARCHAR(50),
                origin VARCHAR(100),
                flowering_period VARCHAR(50),
                colors VARCHAR(100),
                description TEXT,
                care_instructions TEXT,
                image_url VARCHAR(255)
            )
        ''')
        print("Tabelul flower_info creat")

        print("Creez utilizatorul admin...")
        admin_password_hash = generate_password_hash('Admin123!')
        cursor.execute('''
            INSERT INTO user (username, email, password_hash, first_name, last_name, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
        'admin', 'admin@flowerai.com', admin_password_hash, 'Administrator', 'FlowerAI', 'admin', datetime.utcnow()))
        print("Utilizatorul admin creat")

        print("Adaug informații despre flori...")
        sample_flowers = [
            ('rose', 'Trandafir', 'Rosaceae', 'Asia, Europa', 'Mai - Octombrie', 'Roșu, Roz, Alb',
             'Regina florilor cu parfum intens', 'Necesită sol fertil și expunere la soare'),
            ('sunflower', 'Floarea-soarelui', 'Asteraceae', 'America de Nord', 'Iulie - Septembrie', 'Galben',
             'Floare mare care urmărește soarele', 'Necesită mult soare și sol bine drenat'),
            ('petunia', 'Petunie', 'Solanaceae', 'America de Sud', 'Primăvara - Toamna', 'Variată',
             'Floare populară de grădină cu inflorire abundentă', 'Preferă sol fertil și expunere la soare')
        ]

        for flower in sample_flowers:
            cursor.execute('''
                INSERT OR IGNORE INTO flower_info 
                (scientific_name, common_name, family, origin, flowering_period, colors, description, care_instructions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', flower)

        conn.commit()
        print("\nSchema bazei de date creată cu succes!")
        print("\nRezumat:")
        print("   Tabelul user - creat cu utilizatorul admin")
        print("   Tabelul prediction - creat cu suport pentru autentificare")
        print("   Tabelul flower_info - creat (va fi populat separat)")

        print("\n Informații de autentificare admin:")
        print("   Username: admin")
        print("   Email: admin@flowerscan.com")
        print("   Parolă: Admin123.")

    except Exception as e:
        print(f"Eroare la crearea bazei de date: {e}")
        if backup_file and os.path.exists(backup_file):
            print(f"Restaurez din backup: {backup_file}")
            shutil.copy2(backup_file, 'flower_predictions.db')
        raise


def populate_flower_data():
    """Populează baza de date cu toate informațiile despre flori"""
    try:
        print("Populez baza de date cu informații complete despre flori...")

        import subprocess
        result = subprocess.run(['python', 'populate_db.py'], capture_output=True, text=True)

        if result.returncode == 0:
            print("Informații despre flori adăugate cu succes")
        else:
            print(f"Avertisment la popularea florilor: {result.stderr}")

    except Exception as e:
        print(f"Nu s-au putut adăuga informațiile despre flori: {e}")
        print("Poți rula manual: python populate_db.py")


def show_final_status():
    """Afișează statusul final al bazei de date"""
    try:
        conn = sqlite3.connect('flower_predictions.db')
        cursor = conn.cursor()

        print("\n" + "=" * 50)
        print("STATUS FINAL BAZA DE DATE")
        print("=" * 50)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} înregistrări")

        print("\nBaza de date este gata pentru utilizare!")
        print("Poți rula acum: python app.py")

        conn.close()

    except Exception as e:
        print(f"Eroare la verificarea statusului: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'check':
            check_existing_tables()
        elif command == 'create':
            create_complete_database()
        elif command == 'populate':
            populate_flower_data()
        elif command == 'status':
            show_final_status()
        else:
            print("Comenzi disponibile:")
            print("  python fix_database.py check     - Verifică tabelele existente")
            print("  python fix_database.py create    - Creează schema completă")
            print("  python fix_database.py populate  - Populează cu date despre flori")
            print("  python fix_database.py status    - Afișează statusul final")
    else:
        print("Configurez complet baza de date...")
        check_existing_tables()
        create_complete_database()
        populate_flower_data()
        show_final_status()