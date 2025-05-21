from flask import Flask, render_template, request, jsonify
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import io
import base64

app = Flask(__name__)

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


def preprocess_image(img_data):
    """Preproceseaza imaginea pentru predictie"""
    if ',' in img_data:
        img_data = img_data.split(',')[1]

    img_bytes = base64.b64decode(img_data)
    img = Image.open(io.BytesIO(img_bytes))

    img = img.resize(IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalizare

    return img_array


@app.route('/')
def index():
    """Ruta pentru pagina principala"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Ruta pentru procesarea predictiilor"""
    try:
        data = request.json
        img_data = data['image']

        processed_image = preprocess_image(img_data)

        predictions = model.predict(processed_image)

        top_indices = predictions[0].argsort()[-5:][::-1]
        top_predictions = [(flower_classes[i], float(predictions[0][i]) * 100) for i in top_indices]

        result = {
            'success': True,
            'predictions': [{
                'class': pred[0],
                'confidence': round(pred[1], 2)
            } for pred in top_predictions],
            'flower_classes': flower_classes
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)