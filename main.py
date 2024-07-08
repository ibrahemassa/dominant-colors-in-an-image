from flask import Flask, render_template, request
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

def get_colors_codes(image, no):
    image = Image.open(image)
    image = image.convert("RGB")  # Convert to RGB format
    w, h = image.size
    pixel = np.array(image).reshape(w * h, 3)

    model = KMeans(n_clusters=no, random_state=42).fit(pixel)

    B = model.cluster_centers_
    rgb2hex = lambda r, g, b: '#%02x%02x%02x' % (int(r), int(g), int(b))
    return [rgb2hex(*B[i, :]) for i in range(B.shape[0])]

@app.route('/', methods=['POST', 'GET'])
def home():   
    if request.method == 'POST':
        if 'img' in request.files:
            img = request.files['img']
            no_colors = int(request.form['no_colors'])
            if img:
                # Use Pillow to open and convert the image
                image = Image.open(img)
                image = image.convert("RGB")

                img_path = "static/images/temp_image.png"
                image.save(img_path, format="PNG")

                colors = [color.upper() for color in get_colors_codes(img_path, no_colors)]
                return render_template('index.html', colors=colors, image='static/images/temp_image.png')
        return "No image uploaded."
    else:
        colors = ['#344554', '#e7abb5', '#4f606f', '#795153', '#302b36', '#b6818e', '#221c20', '#eae2dc', '#6ea6bd', '#cf9d3e']
        return render_template('index.html', colors=colors, image='static/images/Bocchi_Mc.jpeg') 

if __name__ == '__main__':
    app.run()
