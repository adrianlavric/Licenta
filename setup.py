import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Verifică versiunea Python"""
    if sys.version_info < (3, 8):
        print("Eroare: Este necesară Python 3.8 sau mai nou!")
        print(f"Versiunea curentă: {sys.version}")
        sys.exit(1)
    else:
        print(f"Python {sys.version_info.major}.{sys.version_info.minor} detectat")


# def install_requirements():
#     """Instalează dependințele"""
#     print("📦 Instalez dependințele...")
#
#     try:
#         subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
#         print("✅ Dependințele au fost instalate cu succes")
#     except subprocess.CalledProcessError:
#         print("❌ Eroare la instalarea dependințelor")
#         print("💡 Încearcă să rulezi manual: pip install -r requirements.txt")
#         sys.exit(1)


def create_directories():
    """Creează directoarele necesare"""
    directories = [
        "uploads",
        "logs"
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Director creat/verificat: {directory}")


def check_model_files():
    """Verifică existența fișierelor modelului"""
    model_path = "models/model_flori_avansat.keras"

    if Path(model_path).exists():
        print(f"Model găsit: {model_path}")
        return True
    else:
        print(f"Model lipsă: {model_path}")
        print("⚠Asigură-te că ai modelul în directorul models/")
        return False


def setup_database():
    """Configurează baza de date"""
    print("🗄️  Configurez baza de date...")

    try:
        # Importă și rulează scriptul de populare
        subprocess.run([sys.executable, "populate_db.py", "all"], check=True)
        print("Baza de date configurată cu succes")
    except subprocess.CalledProcessError:
        print("Eroare la configurarea bazei de date")
        print("Încearcă să rulezi manual: python populate_db.py")


def create_run_script():
    """Creează script pentru rularea aplicației"""
    if os.name == 'nt':  # Windows
        run_script = """@echo off
echo Pornesc aplicația FlowerAI...
python app.py
pause"""
        with open("run.bat", "w") as f:
            f.write(run_script)
        print("✅ Script de rulare creat: run.bat")
    else:  # Linux/Mac
        run_script = """#!/bin/bash
echo "Pornesc aplicația FlowerAI..."
python app.py"""
        with open("run.sh", "w") as f:
            f.write(run_script)
        os.chmod("run.sh", 0o755)
        print("✅ Script de rulare creat: run.sh")


def main():
    """Funcția principală de setup"""
    print("🌸 === Setup FlowerScan - Aplicație de Recunoaștere a Florilor ===\n")

    check_python_version()

    create_directories()

    model_exists = check_model_files()

    if model_exists:
        setup_database()
    else:
        print("⚠️  Setup-ul bazei de date a fost omis din cauza modelului lipsă")

    create_run_script()

    print("\n === Setup complet! ===")
    print("\n Pași următori:")

    if not model_exists:
        print("1. ❗ Copiază modelul în models/model_flori_avansat.keras")
        print("2. 🗄️  Rulează: python populate_db.py all")

    print("3. 🚀 Pornește aplicația:")
    if os.name == 'nt':
        print("   Windows: run.bat sau python app.py")
    else:
        print("   Linux/Mac: ./run.sh sau python app.py")

    print("4. 🌐 Deschide browser la: http://localhost:5000")

    print("\n Fișiere importante:")
    print("   app.py - Aplicația principală")
    print("   populate_db.py - Popularea bazei de date")
    print("   requirements.txt - Dependințe Python")
    print("   templates/ - Template-uri HTML")
    print("   models/ - Modele de machine learning")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
Comenzi disponibile:

python setup.py              - Setup complet
python setup.py --help       - Acest mesaj
python app.py                - Rulează aplicația
python populate_db.py all    - Populează baza de date
        """)
    else:
        main()