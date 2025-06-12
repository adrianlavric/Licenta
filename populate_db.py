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
    "colt's foot": {
        "common_name": "Podbal",
        "family": "Asteraceae",
        "origin": "Europa și Asia",
        "flowering_period": "Februarie - Aprilie",
        "colors": "Galben",
        "description": "Plantă medicinală cu flori galbene care apar înaintea frunzelor.",
        "care_instructions": "Preferă sol umed și argilos, tolerează umbra."
    },
    "king protea": {
        "common_name": "Protea rege",
        "family": "Proteaceae",
        "origin": "Africa de Sud",
        "flowering_period": "Iulie - Octombrie",
        "colors": "Roz, Alb",
        "description": "Floarea națională a Africii de Sud, cu aspect exotic.",
        "care_instructions": "Necesită sol acid și bine drenat, expunere la soare."
    },
    "spear thistle": {
        "common_name": "Ciulin cu lance",
        "family": "Asteraceae",
        "origin": "Europa",
        "flowering_period": "Iunie - Septembrie",
        "colors": "Violet, Roz",
        "description": "Plantă spinoasă cu capitule violete sau roz.",
        "care_instructions": "Foarte rezistentă, preferă sol uscat și expunere la soare."
    },
    "yellow iris": {
        "common_name": "Iris galben",
        "family": "Iridaceae",
        "origin": "Europa",
        "flowering_period": "Mai - Iulie",
        "colors": "Galben",
        "description": "Iris acvatic cu flori galbene strălucitoare.",
        "care_instructions": "Preferă sol umed sau apă stagnantă, expunere la soare."
    },
    "globe-flower": {
        "common_name": "Trollius",
        "family": "Ranunculaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Mai - Iulie",
        "colors": "Galben, Portocaliu",
        "description": "Floare sferică cu petale suprapuse, asemănătoare cu peonia.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "purple coneflower": {
        "common_name": "Echinacea purpurie",
        "family": "Asteraceae",
        "origin": "America de Nord",
        "flowering_period": "Iunie - Septembrie",
        "colors": "Violet, Roz",
        "description": "Plantă medicinală cu proprietăți imunostimulatoare.",
        "care_instructions": "Foarte rezistentă, preferă sol bine drenat și soare."
    },
    "peruvian lily": {
        "common_name": "Alstroemeria",
        "family": "Alstroemeriaceae",
        "origin": "America de Sud",
        "flowering_period": "Iunie - Septembrie",
        "colors": "Variată",
        "description": "Floare elegantă cu petale cu dungi și pete distinctive.",
        "care_instructions": "Preferă sol bine drenat și climat temperat."
    },
    "balloon flower": {
        "common_name": "Platycodon",
        "family": "Campanulaceae",
        "origin": "Asia de Est",
        "flowering_period": "Iunie - Septembrie",
        "colors": "Albastru, Alb, Roz",
        "description": "Floare cu muguri în formă de balon înainte de deschidere.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare parțială."
    },
    "giant white arum lily": {
        "common_name": "Cala albă gigant",
        "family": "Araceae",
        "origin": "Africa de Sud",
        "flowering_period": "Primăvara - Vara",
        "colors": "Alb",
        "description": "Floare albă elegantă în formă de pâlnie cu spadice galben.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "fire lily": {
        "common_name": "Crinul de foc",
        "family": "Liliaceae",
        "origin": "Africa de Sud",
        "flowering_period": "Vara - Toamna",
        "colors": "Roșu, Portocaliu",
        "description": "Crin spectaculos cu flori roșii-portocalii intense.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "pincushion flower": {
        "common_name": "Scabiosa",
        "family": "Dipsacaceae",
        "origin": "Europa și Africa",
        "flowering_period": "Iunie - Octombrie",
        "colors": "Albastru, Violet, Alb",
        "description": "Floare cu aspect de pernuță de ace datorită staminelor proeminente.",
        "care_instructions": "Preferă sol calcaros și expunere la soare."
    },
    "fritillary": {
        "common_name": "Lalea bălțată",
        "family": "Liliaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Aprilie - Mai",
        "colors": "Violet cu alb",
        "description": "Floare cu petale în formă de șah, cu model distinctive.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "red ginger": {
        "common_name": "Ghimbir roșu",
        "family": "Zingiberaceae",
        "origin": "Asia de Sud-Est",
        "flowering_period": "Tot anul (clima tropicală)",
        "colors": "Roșu",
        "description": "Plantă tropicală cu flori roșii strălucitoare în spice.",
        "care_instructions": "Necesită umiditate ridicată și temperaturi calde."
    },
    "grape hyacinth": {
        "common_name": "Muscari",
        "family": "Asparagaceae",
        "origin": "Regiunea Mediteraneană",
        "flowering_period": "Martie - Mai",
        "colors": "Albastru, Violet",
        "description": "Flori mici în formă de clopot dispuse în spice compacte.",
        "care_instructions": "Foarte rezistent, preferă sol bine drenat."
    },
    "corn poppy": {
        "common_name": "Mac de câmp",
        "family": "Papaveraceae",
        "origin": "Europa și Asia",
        "flowering_period": "Mai - Iulie",
        "colors": "Roșu",
        "description": "Floare sălbatică roșie cu petale delicate și efemere.",
        "care_instructions": "Preferă sol sărac și expunere la soare."
    },
    "prince of wales feathers": {
        "common_name": "Celosia",
        "family": "Amaranthaceae",
        "origin": "Africa tropicală",
        "flowering_period": "Vara - Toamna",
        "colors": "Roșu, Galben, Portocaliu",
        "description": "Floare cu inflorescență în formă de pene colorate.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "stemless gentian": {
        "common_name": "Gențiană fără tulpină",
        "family": "Gentianaceae",
        "origin": "Munții Europei",
        "flowering_period": "Mai - August",
        "colors": "Albastru intens",
        "description": "Floare alpină cu albastru intens, crește în tufe compacte.",
        "care_instructions": "Necesită sol calcaros și climat rece de munte."
    },
    "artichoke": {
        "common_name": "Anghinare",
        "family": "Asteraceae",
        "origin": "Regiunea Mediteraneană",
        "flowering_period": "Iunie - August",
        "colors": "Violet, Albastru",
        "description": "Plantă comestibilă cu capitule mari și bractee spinoase.",
        "care_instructions": "Preferă climat temperat și sol fertil."
    },
    "sweet william": {
        "common_name": "Garoafă turcească",
        "family": "Caryophyllaceae",
        "origin": "Europa de Sud",
        "flowering_period": "Mai - Iulie",
        "colors": "Roz, Roșu, Alb",
        "description": "Flori mici și parfumate grupate în capitule dense.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "carnation": {
        "common_name": "Garoafă",
        "family": "Caryophyllaceae",
        "origin": "Regiunea Mediteraneană",
        "flowering_period": "Mai - Septembrie",
        "colors": "Roz, Roșu, Alb, Galben",
        "description": "Floare clasică cu petale zimțate și parfum dulce.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "garden phlox": {
        "common_name": "Flox de grădină",
        "family": "Polemoniaceae",
        "origin": "America de Nord",
        "flowering_period": "Iulie - Septembrie",
        "colors": "Roz, Alb, Violet",
        "description": "Flori parfumate în corimburi dense și colorate.",
        "care_instructions": "Preferă sol fertil și umed, expunere la soare parțială."
    },
    "love in the mist": {
        "common_name": "Nigella",
        "family": "Ranunculaceae",
        "origin": "Europa de Sud",
        "flowering_period": "Iunie - August",
        "colors": "Albastru, Alb, Roz",
        "description": "Floare delicată înconjurată de frunze filiformes.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "mexican aster": {
        "common_name": "Cosmos mexican",
        "family": "Asteraceae",
        "origin": "Mexic",
        "flowering_period": "Vara - Toamna",
        "colors": "Roz, Alb, Violet",
        "description": "Floare simplă cu petale delicate și frunze filiformes.",
        "care_instructions": "Foarte rezistent, preferă sol sărac și soare."
    },
    "alpine sea holly": {
        "common_name": "Spânz de mare alpin",
        "family": "Apiaceae",
        "origin": "Europa",
        "flowering_period": "Iulie - Septembrie",
        "colors": "Albastru, Violet",
        "description": "Plantă perenă cu frunze spinoase și flori albastru-violet.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "ruby-lipped cattleya": {
        "common_name": "Cattleya cu buze rubinii",
        "family": "Orchidaceae",
        "origin": "America Centrală și de Sud",
        "flowering_period": "Variabil",
        "colors": "Alb cu roz",
        "description": "Orhidee epifită cu flori mari și buze colorate distinctiv.",
        "care_instructions": "Necesită umiditate ridicată și lumină indirectă."
    },
    "cape flower": {
        "common_name": "Floarea Capului",
        "family": "Proteaceae",
        "origin": "Africa de Sud",
        "flowering_period": "Primăvara - Vara",
        "colors": "Variată",
        "description": "Floare exotică specifică regiunii Cape din Africa de Sud.",
        "care_instructions": "Necesită sol acid și climat mediteranean."
    },
    "great masterwort": {
        "common_name": "Astrantia mare",
        "family": "Apiaceae",
        "origin": "Europa Centrală",
        "flowering_period": "Iunie - August",
        "colors": "Alb, Roz",
        "description": "Floare cu umbelă caracteristică înconjurată de bractee colorate.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "siam tulip": {
        "common_name": "Lalua siameză",
        "family": "Zingiberaceae",
        "origin": "Asia de Sud-Est",
        "flowering_period": "Vara",
        "colors": "Roz, Violet",
        "description": "Plantă tropicală cu inflorescență asemănătoare lalelei.",
        "care_instructions": "Necesită umiditate ridicată și climat tropical."
    },
    "lenten rose": {
        "common_name": "Helleborus",
        "family": "Ranunculaceae",
        "origin": "Europa",
        "flowering_period": "Februarie - Aprilie",
        "colors": "Alb, Roz, Violet",
        "description": "Floare de iarnă/primăvară timpurie cu aspect elegant.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "barbeton daisy": {
        "common_name": "Gerbera",
        "family": "Asteraceae",
        "origin": "Africa de Sud",
        "flowering_period": "Primăvara - Toamna",
        "colors": "Variată",
        "description": "Floare cu petale mari și colorate, folosită în buchete.",
        "care_instructions": "Preferă sol bine drenat și lumină indirectă."
    },
    "daffodil": {
        "common_name": "Narcisă",
        "family": "Amaryllidaceae",
        "origin": "Europa și Africa de Nord",
        "flowering_period": "Februarie - Mai",
        "colors": "Galben, Alb",
        "description": "Floare de primăvară cu coroană centrală caracteristică.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "sword lily": {
        "common_name": "Gladiolă",
        "family": "Iridaceae",
        "origin": "Africa și Europa",
        "flowering_period": "Vara",
        "colors": "Variată",
        "description": "Floare înaltă cu inflorescență în spic și frunze în formă de spadă.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "poinsettia": {
        "common_name": "Steaua Crăciunului",
        "family": "Euphorbiaceae",
        "origin": "Mexic",
        "flowering_period": "Decembrie - Februarie",
        "colors": "Roșu, Alb, Roz",
        "description": "Plantă decorativă de Crăciun cu bractee colorate.",
        "care_instructions": "Necesită temperaturi constante și lumină indirectă."
    },
    "bolero deep blue": {
        "common_name": "Petunie Bolero albastru închis",
        "family": "Solanaceae",
        "origin": "Hibrid horticol",
        "flowering_period": "Primăvara - Toamna",
        "colors": "Albastru închis",
        "description": "Varietate hibridă de petunie cu flori albastre intense.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "wallflower": {
        "common_name": "Micsandra",
        "family": "Brassicaceae",
        "origin": "Europa de Sud",
        "flowering_period": "Aprilie - Iunie",
        "colors": "Galben, Portocaliu, Roșu",
        "description": "Floare parfumată care crește pe ziduri și stânci.",
        "care_instructions": "Preferă sol calcaros și expunere la soare."
    },
    "marigold": {
        "common_name": "Gălbenele",
        "family": "Asteraceae",
        "origin": "America Centrală",
        "flowering_period": "Mai - Octombrie",
        "colors": "Galben, Portocaliu",
        "description": "Floare anuală cu proprietăți insecticide naturale.",
        "care_instructions": "Foarte rezistentă, preferă sol bine drenat și soare."
    },
    "buttercup": {
        "common_name": "Piciorul cocorului",
        "family": "Ranunculaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Aprilie - Septembrie",
        "colors": "Galben",
        "description": "Floare sălbatică cu petale galbene lucioase.",
        "care_instructions": "Preferă sol umed și expunere la soare parțială."
    },
    "oxeye daisy": {
        "common_name": "Margaretă de câmp",
        "family": "Asteraceae",
        "origin": "Europa",
        "flowering_period": "Mai - Septembrie",
        "colors": "Alb cu centru galben",
        "description": "Floare clasică de margaretă cu petale albe și centru galben.",
        "care_instructions": "Foarte rezistentă, preferă sol bine drenat."
    },
    "common dandelion": {
        "common_name": "Păpădie",
        "family": "Asteraceae",
        "origin": "Europa și Asia",
        "flowering_period": "Martie - Noiembrie",
        "colors": "Galben",
        "description": "Plantă medicinală și comestibilă cu flori galbene.",
        "care_instructions": "Extrem de rezistentă, crește în orice tip de sol."
    },
    "petunia": {
        "common_name": "Petunie",
        "family": "Solanaceae",
        "origin": "America de Sud",
        "flowering_period": "Primăvara - Toamna",
        "colors": "Variată",
        "description": "Floare populară de grădină cu inflorire abundentă.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "wild pansy": {
        "common_name": "Panseluta sălbatică",
        "family": "Violaceae",
        "origin": "Europa",
        "flowering_period": "Aprilie - Septembrie",
        "colors": "Violet, Galben, Alb",
        "description": "Floare mică cu față asemănătoare cu pisica, strămoșa panselutelor de grădină.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "primula": {
        "common_name": "Ciuboțica cucului",
        "family": "Primulaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Martie - Mai",
        "colors": "Variată",
        "description": "Floare de primăvară timpurie cu culori vii.",
        "care_instructions": "Preferă sol umed și umbră parțială."
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
    "pelargonium": {
        "common_name": "Mușcată",
        "family": "Geraniaceae",
        "origin": "Africa de Sud",
        "flowering_period": "Primăvara - Toamna",
        "colors": "Roșu, Roz, Alb",
        "description": "Plantă populară de balcon cu flori colorate și frunze parfumate.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "bishop of llandaff": {
        "common_name": "Dalia Episcopul din Llandaff",
        "family": "Asteraceae",
        "origin": "Hibrid horticol",
        "flowering_period": "Vara - Toamna",
        "colors": "Roșu închis",
        "description": "Varietate de dalie cu flori roșii intense și frunzaj închis.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "gaura": {
        "common_name": "Gaura",
        "family": "Onagraceae",
        "origin": "America de Nord",
        "flowering_period": "Mai - Octombrie",
        "colors": "Alb, Roz",
        "description": "Plantă perenă cu flori delicate care dansează în vânt.",
        "care_instructions": "Foarte rezistentă la secetă, preferă sol drenat."
    },
    "geranium": {
        "common_name": "Geranium",
        "family": "Geraniaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Mai - Septembrie",
        "colors": "Roz, Violet, Alb",
        "description": "Plantă perenă cu flori delicate în cupe sau farfurii.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "orange dahlia": {
        "common_name": "Dalia portocalie",
        "family": "Asteraceae",
        "origin": "Mexic",
        "flowering_period": "Vara - Toamna",
        "colors": "Portocaliu",
        "description": "Dalie cu flori mari portocalii în diverse forme.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "pink-yellow dahlia": {
        "common_name": "Dalia roz-galbenă",
        "family": "Asteraceae",
        "origin": "Mexic",
        "flowering_period": "Vara - Toamna",
        "colors": "Roz și galben",
        "description": "Dalie cu petale bicolore roz și galbene.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "cautleya spicata": {
        "common_name": "Cautleya",
        "family": "Zingiberaceae",
        "origin": "Himalaya",
        "flowering_period": "Toamna",
        "colors": "Galben cu roșu",
        "description": "Plantă din familia ghimbirului cu flori galbene și bractee roșii.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "japanese anemone": {
        "common_name": "Anemonă japoneză",
        "family": "Ranunculaceae",
        "origin": "Asia de Est",
        "flowering_period": "August - Octombrie",
        "colors": "Roz, Alb",
        "description": "Plantă perenă cu flori elegante de toamnă.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "black-eyed susan": {
        "common_name": "Susan cu ochi negri",
        "family": "Asteraceae",
        "origin": "America de Nord",
        "flowering_period": "Iunie - Octombrie",
        "colors": "Galben cu centru negru",
        "description": "Floare sălbatică cu petale galbene și centru întunecat.",
        "care_instructions": "Foarte rezistentă, preferă sol drenat și soare."
    },
    "silverbush": {
        "common_name": "Tufișul argintiu",
        "family": "Solanaceae",
        "origin": "America de Sud",
        "flowering_period": "Vara - Toamna",
        "colors": "Alb, Violet",
        "description": "Arbust cu frunze argintii și flori albe sau violete.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "californian poppy": {
        "common_name": "Maca californiană",
        "family": "Papaveraceae",
        "origin": "California, SUA",
        "flowering_period": "Februarie - Septembrie",
        "colors": "Portocaliu, Galben",
        "description": "Floarea oficială a Californiei, cu petale delicate portocalii.",
        "care_instructions": "Preferă sol uscat și expunere la soare."
    },
    "osteospermum": {
        "common_name": "Margareta africană",
        "family": "Asteraceae",
        "origin": "Africa de Sud",
        "flowering_period": "Primăvara - Toamna",
        "colors": "Alb, Violet, Roz",
        "description": "Margaretă cu petale alungite și centru colorat distinctiv.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "spring crocus": {
        "common_name": "Brândușă de primăvară",
        "family": "Iridaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Februarie - Aprilie",
        "colors": "Violet, Alb, Galben",
        "description": "Prima floare de primăvară, cu flori în formă de cupă.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "bearded iris": {
        "common_name": "Iris bărbos",
        "family": "Iridaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Mai - Iunie",
        "colors": "Variată",
        "description": "Iris cu pene caracteristice pe petalele inferioare.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "windflower": {
        "common_name": "Anemonă",
        "family": "Ranunculaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Martie - Mai",
        "colors": "Alb, Roz, Albastru",
        "description": "Floare delicată de primăvară cu petale ca mătasea.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "tree poppy": {
        "common_name": "Maca arbustivă",
        "family": "Papaveraceae",
        "origin": "California, SUA",
        "flowering_period": "Vara - Toamna",
        "colors": "Galben",
        "description": "Arbust cu flori mari galbene și frunze argintii.",
        "care_instructions": "Preferă sol bine drenat și climat mediteranean."
    },
    "gazania": {
        "common_name": "Gazania",
        "family": "Asteraceae",
        "origin": "Africa de Sud",
        "flowering_period": "Primăvara - Toamna",
        "colors": "Galben, Portocaliu, Roșu",
        "description": "Floare cu petale strălucitoare care se închid pe timp înnorat.",
        "care_instructions": "Preferă sol uscat și expunere la soare."
    },
    "azalea": {
        "common_name": "Azalee",
        "family": "Ericaceae",
        "origin": "Asia",
        "flowering_period": "Aprilie - Mai",
        "colors": "Roz, Alb, Roșu, Violet",
        "description": "Arbust ornamental cu inflorire spectaculoasă.",
        "care_instructions": "Preferă sol acid și umbră parțială."
    },
    "water lily": {
        "common_name": "Nufăr",
        "family": "Nymphaeaceae",
        "origin": "Răspândit global",
        "flowering_period": "Mai - Septembrie",
        "colors": "Alb, Roz, Galben",
        "description": "Plantă acvatică cu flori flotante și frunze mari rotunde.",
        "care_instructions": "Necesită apă stagnantă și expunere la soare."
    },
    "rose": {
        "common_name": "Trandafir",
        "family": "Rosaceae",
        "origin": "Asia, Europa, America de Nord",
        "flowering_period": "Mai - Octombrie",
        "colors": "Roșu, Roz, Alb, Galben",
        "description": "Regina florilor, cu parfum intens și frumusețe clasică.",
        "care_instructions": "Necesită sol fertil, expunere la soare și udare regulată."
    },
    "thorn apple": {
        "common_name": "Ciumăfaie",
        "family": "Solanaceae",
        "origin": "America Centrală",
        "flowering_period": "Iulie - Octombrie",
        "colors": "Alb, Violet",
        "description": "Plantă toxică cu flori mari în formă de trompetă.",
        "care_instructions": "Foarte rezistentă, preferă sol bogat. ATENȚIE: Toxică!"
    },
    "morning glory": {
        "common_name": "Volbură",
        "family": "Convolvulaceae",
        "origin": "America tropicală",
        "flowering_period": "Vara - Toamna",
        "colors": "Albastru, Violet, Roz",
        "description": "Plantă cățărătoare cu flori în formă de pâlnie care se deschid dimineața.",
        "care_instructions": "Preferă sol fertil și expunere la soare."
    },
    "passion flower": {
        "common_name": "Floarea patimilor",
        "family": "Passifloraceae",
        "origin": "America de Sud",
        "flowering_period": "Vara - Toamna",
        "colors": "Alb, Violet, Albastru",
        "description": "Floare exotică cu structură complexă simbolizând patimile lui Hristos.",
        "care_instructions": "Preferă sol umed și expunere la soare parțială."
    },
    "lotus": {
        "common_name": "Lotus",
        "family": "Nelumbonaceae",
        "origin": "Asia și Australia",
        "flowering_period": "Vara",
        "colors": "Roz, Alb",
        "description": "Floare sacră în buddhism și hinduism, cu petale mari și parfum intens.",
        "care_instructions": "Necesită apă adâncă și expunere la soare."
    },
    "toad lily": {
        "common_name": "Crinul broască",
        "family": "Liliaceae",
        "origin": "Asia de Est",
        "flowering_period": "Toamna",
        "colors": "Alb cu puncte violete",
        "description": "Floare exotică cu petale pătate, înflorește târziu în sezon.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "anthurium": {
        "common_name": "Anthurium",
        "family": "Araceae",
        "origin": "America Centrală și de Sud",
        "flowering_period": "Tot anul",
        "colors": "Roșu, Roz, Alb",
        "description": "Plantă tropicală cu spata lucioasă în formă de inimă.",
        "care_instructions": "Necesită umiditate ridicată și temperaturi constante."
    },
    "frangipani": {
        "common_name": "Frangipani",
        "family": "Apocynaceae",
        "origin": "America Centrală",
        "flowering_period": "Primăvara - Toamna",
        "colors": "Alb, Galben, Roz",
        "description": "Floare tropicală extrem de parfumată, simbolul Hawaiiului.",
        "care_instructions": "Necesită climat cald și sol bine drenat."
    },
    "clematis": {
        "common_name": "Clematită",
        "family": "Ranunculaceae",
        "origin": "Europa, Asia, America de Nord",
        "flowering_period": "Variabil",
        "colors": "Violet, Alb, Roz",
        "description": "Plantă cățărătoare cu flori mari și spectaculoase.",
        "care_instructions": "Preferă rădăcinile la umbră și capul la soare."
    },
    "hibiscus": {
        "common_name": "Hibiscus",
        "family": "Malvaceae",
        "origin": "Asia și Pacific",
        "flowering_period": "Vara - Toamna",
        "colors": "Roșu, Roz, Galben, Alb",
        "description": "Floare tropicală mare cu stamine proeminente.",
        "care_instructions": "Preferă sol umed și expunere la soare."
    },
    "columbine": {
        "common_name": "Căldărușă",
        "family": "Ranunculaceae",
        "origin": "Emisfira nordică",
        "flowering_period": "Mai - Iulie",
        "colors": "Albastru, Violet, Alb, Roz",
        "description": "Floare cu pinteni caracteristici și forme elegante.",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "desert-rose": {
        "common_name": "Trandafirul deșertului",
        "family": "Apocynaceae",
        "origin": "Africa și Arabia",
        "flowering_period": "Primăvara - Vara",
        "colors": "Roz, Alb",
        "description": "Plantă suculentă cu flori roz și tulpină îngroșată.",
        "care_instructions": "Necesită sol foarte bine drenat și puțină apă."
    },
    "tree mallow": {
        "common_name": "Năprasnica arbustivă",
        "family": "Malvaceae",
        "origin": "Europa de Sud",
        "flowering_period": "Vara - Toamna",
        "colors": "Roz, Violet",
        "description": "Arbust cu flori mari în formă de cupă și frunze palmate.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare."
    },
    "magnolia": {
        "common_name": "Magnolia",
        "family": "Magnoliaceae",
        "origin": "Asia și America",
        "flowering_period": "Primăvara",
        "colors": "Alb, Roz, Violet",
        "description": "Arbore cu flori mari și parfumate care apar înaintea frunzelor.",
        "care_instructions": "Preferă sol acid și protecție de vânturile reci."
    },
    "cyclamen": {
        "common_name": "Ciclamen",
        "family": "Primulaceae",
        "origin": "Regiunea Mediteraneană",
        "flowering_period": "Toamna - Iarna",
        "colors": "Roz, Alb, Roșu",
        "description": "Plantă de interior cu flori răsfrânte și frunze în formă de inimă.",
        "care_instructions": "Preferă temperaturi răcoroase și sol bine drenat."
    },
    "watercress": {
        "common_name": "Năsturel",
        "family": "Brassicaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Mai - Septembrie",
        "colors": "Alb",
        "description": "Plantă acvatică comestibilă cu flori mici albe.",
        "care_instructions": "Necesită apă curgătoare și umbră parțială."
    },
    "canna lily": {
        "common_name": "Canna",
        "family": "Cannaceae",
        "origin": "America tropicală",
        "flowering_period": "Vara - Toamna",
        "colors": "Roșu, Galben, Portocaliu",
        "description": "Plantă cu flori mari și frunze largi decorative.",
        "care_instructions": "Preferă sol umed și expunere la soare."
    },
    "hippeastrum": {
        "common_name": "Hippeastrum",
        "family": "Amaryllidaceae",
        "origin": "America de Sud",
        "flowering_period": "Iarna - Primăvara",
        "colors": "Roșu, Alb, Roz",
        "description": "Plantă de bulb cu flori mari în formă de trompetă.",
        "care_instructions": "Necesită perioadă de repaus și sol bine drenat."
    },
    "bee balm": {
        "common_name": "Mentă sălbatică",
        "family": "Lamiaceae",
        "origin": "America de Nord",
        "flowering_period": "Iulie - Septembrie",
        "colors": "Roșu, Roz, Violet",
        "description": "Plantă aromatică care atrage albinele și fluturii.",
        "care_instructions": "Preferă sol umed și expunere la soare sau umbră parțială."
    },
    "ball moss": {
        "common_name": "Mușchi bilă",
        "family": "Bromeliaceae",
        "origin": "America de Nord și Sud",
        "flowering_period": "Primăvara",
        "colors": "Verde, Gri",
        "description": "Plantă epifită care crește pe copaci, formând bile compacte.",
        "care_instructions": "Nu necesită sol, absoarbe nutrienții din aer."
    },
    "foxglove": {
        "common_name": "Degetuș",
        "family": "Plantaginaceae",
        "origin": "Europa",
        "flowering_period": "Iunie - August",
        "colors": "Violet, Alb, Roz",
        "description": "Plantă înaltă cu flori tubulare dispuse în spic. ATENȚIE: Toxică!",
        "care_instructions": "Preferă sol umed și umbră parțială."
    },
    "bougainvillea": {
        "common_name": "Bougainvillea",
        "family": "Nyctaginaceae",
        "origin": "America de Sud",
        "flowering_period": "Tot anul (clima caldă)",
        "colors": "Roz, Violet, Alb, Portocaliu",
        "description": "Plantă cățărătoare cu bractee colorate și flori mici albe.",
        "care_instructions": "Preferă climat cald și sec, sol bine drenat."
    },
    "camellia": {
        "common_name": "Camelie",
        "family": "Theaceae",
        "origin": "Asia de Est",
        "flowering_period": "Noiembrie - Aprilie",
        "colors": "Alb, Roz, Roșu",
        "description": "Arbust cu flori mari și frunze lucioase, înflorește iarna.",
        "care_instructions": "Preferă sol acid și umbră parțială."
    },
    "mallow": {
        "common_name": "Nalbă",
        "family": "Malvaceae",
        "origin": "Europa și Asia",
        "flowering_period": "Iunie - Septembrie",
        "colors": "Roz, Alb, Violet",
        "description": "Plantă cu flori mari în formă de cupă și proprietăți medicinale.",
        "care_instructions": "Preferă sol umed și expunere la soare."
    },
    "mexican petunia": {
        "common_name": "Petunie mexicană",
        "family": "Acanthaceae",
        "origin": "Mexic și America Centrală",
        "flowering_period": "Vara - Toamna",
        "colors": "Violet, Alb",
        "description": "Plantă perenă cu flori violete și frunze alungite.",
        "care_instructions": "Preferă sol umed și poate fi invazivă."
    },
    "bromelia": {
        "common_name": "Bromelia",
        "family": "Bromeliaceae",
        "origin": "America tropicală",
        "flowering_period": "Variabil",
        "colors": "Roșu, Galben, Roz",
        "description": "Plantă tropicală cu frunze în rozeta și flori colorate.",
        "care_instructions": "Necesită umiditate ridicată și temperaturi constante."
    },
    "blanket flower": {
        "common_name": "Gaillardia",
        "family": "Asteraceae",
        "origin": "America de Nord și Sud",
        "flowering_period": "Iunie - Octombrie",
        "colors": "Roșu, Galben, Portocaliu",
        "description": "Floare cu petale colorate în nuanțe calde, foarte rezistentă.",
        "care_instructions": "Preferă sol uscat și expunere la soare complet."
    },
    "trumpet creeper": {
        "common_name": "Bignonia",
        "family": "Bignoniaceae",
        "origin": "America de Nord",
        "flowering_period": "Vara - Toamna",
        "colors": "Portocaliu, Roșu",
        "description": "Plantă cățărătoare viguroasă cu flori în formă de trompetă.",
        "care_instructions": "Foarte rezistentă, poate fi invazivă."
    },
    "blackberry lily": {
        "common_name": "Crinul cu fructe negre",
        "family": "Iridaceae",
        "origin": "Asia",
        "flowering_period": "Iulie - August",
        "colors": "Portocaliu cu pete roșii",
        "description": "Plantă cu flori portocalii cu pete roșii și fructe negre asemănătoare murelor.",
        "care_instructions": "Preferă sol bine drenat și expunere la soare sau umbră parțială."
    }
}

def populate_flower_database():
    """Populează baza de date cu informații despre flori"""

    with app.app_context():
        print("Începe popularea bazei de date cu informații despre flori...")

        db.create_all()

        added_count = 0
        for scientific_name, info in FLOWER_DATA.items():
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