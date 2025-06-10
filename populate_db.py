from app import app, db, FlowerInfo

FLOWER_DATA = {
    "pink primrose": {
        "common_name": "Ciuboțica cucului roz",
        "family": "Primulaceae",
        "origin": "Europa",
        "flowering_period": "Aprilie - Iunie",
        "colors": "Roz, Alb",
        "description": "Floare de primăvară cu petale delicate roz sau albe.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "hard-leaved pocket orchid": {
        "common_name": "Orhidee cu frunze tari",
        "family": "Orchidaceae",
        "origin": "Europa",
        "flowering_period": "Mai - Iulie",
        "colors": "Violet, Roz",
        "description": "Orhidee terestră cu flori mici și parfumate.",
        "care_instructions": "Necesită sol calcaros și expunere la soare."
    },
    "canterbury bells": {
        "common_name": "Clopotei de Canterbury",
        "family": "Campanulaceae",
        "origin": "Europa de Sud",
        "flowering_period": "Mai - Iulie",
        "colors": "Albastru, Alb, Roz",
        "description": "Plantă bienală cu flori în formă de clopot.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "sweet pea": {
        "common_name": "Mazăre dulce",
        "family": "Fabaceae",
        "origin": "Regiunea Mediteraneană",
        "flowering_period": "Iunie - Septembrie",
        "colors": "Roz, Alb, Violet",
        "description": "Plantă cățărătoare cu flori parfumate.",
        "care_instructions": "Necesită suport pentru cățărare și sol fertil."
    },
    "english marigold": {
        "common_name": "Gălbenele englezești",
        "family": "Asteraceae",
        "origin": "Europa de Sud",
        "flowering_period": "Aprilie - Octombrie",
        "colors": "Galben, Portocaliu",
        "description": "Floare anuală cu proprietăți medicinale.",
        "care_instructions": "Foarte rezistentă, preferă sol bine drenat."
    },
    "tiger lily": {
        "common_name": "Crinul tigru",
        "family": "Liliaceae",
        "origin": "Asia de Est",
        "flowering_period": "Iulie - August",
        "colors": "Portocaliu cu pete negre",
        "description": "Crin spectaculos cu petale întoarse și pete negre.",
        "care_instructions": "Preferă sol umed și expunere la soare."
    },
    "moon orchid": {
        "common_name": "Orhideea lunii",
        "family": "Orchidaceae",
        "origin": "Asia de Sud-Est",
        "flowering_period": "Tot anul",
        "colors": "Alb cu centru galben",
        "description": "Orhidee epifită cu flori albe elegante.",
        "care_instructions": "Necesită umiditate ridicată și lumină indirectă."
    },
    "bird of paradise": {
        "common_name": "Pasărea paradisului",
        "family": "Strelitziaceae",
        "origin": "Africa de Sud",
        "flowering_period": "Tot anul (clima tropicală)",
        "colors": "Portocaliu, Albastru",
        "description": "Floare exotică cu forma unei păsări în zbor.",
        "care_instructions": "Necesită temperaturi calde și umiditate ridicată."
    },
    "monkshood": {
        "common_name": "Aconit",
        "family": "Ranunculaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Iunie - Septembrie",
        "colors": "Albastru, Violet",
        "description": "Plantă perenă toxică cu flori în formă de cască.",
        "care_instructions": "Preferă sol umed și umbră parțială. ATENȚIE: Toxică!"
    },
    "globe thistle": {
        "common_name": "Scai globular",
        "family": "Asteraceae",
        "origin": "Europa și Asia",
        "flowering_period": "Iulie - Septembrie",
        "colors": "Albastru",
        "description": "Plantă perenă cu capitule sferice albastre.",
        "care_instructions": "Foarte rezistentă la secetă, preferă sol uscat."
    },
    "snapdragon": {
        "common_name": "Gura leului",
        "family": "Plantaginaceae",
        "origin": "Regiunea Mediteraneană",
        "flowering_period": "Mai - Octombrie",
        "colors": "Variată",
        "description": "Flori în formă de gură care se deschid la apăsare.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "sunflower": {
        "common_name": "Floarea-soarelui",
        "family": "Asteraceae",
        "origin": "America de Nord",
        "flowering_period": "Iulie - Septembrie",
        "colors": "Galben",
        "description": "Floare mare care urmărește soarele pe parcursul zilei.",
        "care_instructions": "Necesită mult soare și sol bine drenat."
    },
    "rose": {
        "common_name": "Trandafir",
        "family": "Rosaceae",
        "origin": "Asia, Europa, America de Nord",
        "flowering_period": "Mai - Octombrie",
        "colors": "Roșu, Roz, Alb, Galben",
        "description": "Regina florilor, cu parfum intens și frumusețe clasică.",
        "care_instructions": "Necesită sol fertil, expunere la soare și udare regulată."
    }
}


def populate_flower_database():
    """Populează baza de date cu informații despre flori"""

    with app.app_context():
        print("Începe popularea bazei de date cu informații despre flori...")

        # Creează tabelele dacă nu există
        db.create_all()

        added_count = 0
        for scientific_name, info in FLOWER_DATA.items():
            # Verifică dacă floarea există deja
            existing_flower = FlowerInfo.query.filter_by(scientific_name=scientific_name).first()

            if not existing_flower:
                flower = FlowerInfo(
                    scientific_name=scientific_name,
                    common_name=info.get('common_name'),
                    family=info.get('family'),
                    origin=info.get('origin'),
                    flowering_period=info.get('flowering_period'),
                    colors=info.get('colors'),
                    description=info.get('description'),
                    care_instructions=info.get('care_instructions'),
                    image_url=None  # Poate fi completat ulterior
                )

                db.session.add(flower)
                added_count += 1
                print(f"Adăugat: {scientific_name}")
            else:
                print(f"Există deja: {scientific_name}")

        # Salvează modificările
        try:
            db.session.commit()
            print(f"Popularea completă! Au fost adăugate {added_count} flori în baza de date.")
        except Exception as e:
            print(f"Eroare la salvarea în baza de date: {e}")
            db.session.rollback()


def add_romanian_flowers():
    """Adaugă flori specifice României"""

    romanian_flowers = {
        "centaurea cyanus": {
            "common_name": "Albăstrea",
            "family": "Asteraceae",
            "origin": "Europa",
            "flowering_period": "Mai - Septembrie",
            "colors": "Albastru",
            "description": "Floarea națională a României, cu petale albastre caracteristice.",
            "care_instructions": "Preferă sol bine drenat și expunere la soare."
        },
        "galanthus nivalis": {
            "common_name": "Ghiocel",
            "family": "Amaryllidaceae",
            "origin": "Europa",
            "flowering_period": "Februarie - Martie",
            "colors": "Alb",
            "description": "Prima floare a primăverii în România, cu petale albe delicate.",
            "care_instructions": "Preferă sol umed și umbră parțială."
        },
        "leucojum vernum": {
            "common_name": "Clopoței",
            "family": "Amaryllidaceae",
            "origin": "Europa",
            "flowering_period": "Februarie - Aprilie",
            "colors": "Alb cu puncte verzi",
            "description": "Floare de primăvară specifică pădurilor românești.",
            "care_instructions": "Preferă sol umed și umbră."
        },
        "crocus heuffelianus": {
            "common_name": "Brândușă",
            "family": "Iridaceae",
            "origin": "România (endemic)",
            "flowering_period": "Septembrie - Octombrie",
            "colors": "Violet",
            "description": "Specie endemică României, înflorește toamna.",
            "care_instructions": "Preferă sol calcaros și expunere la soare."
        }
    }

    with app.app_context():
        print("Adăugarea florilor românești...")

        added_count = 0
        for scientific_name, info in romanian_flowers.items():
            existing_flower = FlowerInfo.query.filter_by(scientific_name=scientific_name).first()

            if not existing_flower:
                flower = FlowerInfo(
                    scientific_name=scientific_name,
                    common_name=info.get('common_name'),
                    family=info.get('family'),
                    origin=info.get('origin'),
                    flowering_period=info.get('flowering_period'),
                    colors=info.get('colors'),
                    description=info.get('description'),
                    care_instructions=info.get('care_instructions'),
                    image_url=None
                )

                db.session.add(flower)
                added_count += 1
                print(f"Adăugat: {scientific_name} ({info['common_name']})")
            else:
                print(f"Există deja: {scientific_name}")

        try:
            db.session.commit()
            print(f"Au fost adăugate {added_count} flori românești în baza de date.")
        except Exception as e:
            print(f"Eroare la salvarea florilor românești: {e}")
            db.session.rollback()


def show_database_stats():
    """Afișează statistici despre baza de date"""
    with app.app_context():
        total_flowers = FlowerInfo.query.count()
        print(f"Total flori în baza de date: {total_flowers}")

        if total_flowers > 0:
            print("\nPrimele 5 flori din baza de date:")
            flowers = FlowerInfo.query.limit(5).all()
            for flower in flowers:
                print(f"- {flower.scientific_name} ({flower.common_name})")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'populate':
            populate_flower_database()
        elif command == 'romanian':
            add_romanian_flowers()
        elif command == 'stats':
            show_database_stats()
        elif command == 'all':
            populate_flower_database()
            add_romanian_flowers()
            show_database_stats()
        else:
            print("Comenzi disponibile:")
            print("  python populate_db.py populate  - Populează baza de date")
            print("  python populate_db.py romanian  - Adaugă flori românești")
            print("  python populate_db.py stats     - Afișează statistici")
            print("  python populate_db.py all       - Execută toate comenzile")
    else:
        print("Popularea automată a bazei de date...")
        populate_flower_database()
        add_romanian_flowers()
        show_database_stats()
        print("Toate florile au fost adăugate!")