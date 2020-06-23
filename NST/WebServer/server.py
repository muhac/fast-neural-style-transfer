import os
import time
import base64
from PIL import Image
from io import BytesIO

import torch
from torch.autograd import Variable
from torchvision.utils import save_image

from models import TransformerNet
from utils import *

from flask import *
from flask_cors import CORS

app = Flask(__name__, )
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(app, resources=r'/*')


# 上传文件
@app.route("/nst/", methods=['POST'])
def uploadFile():
    result_text = {"statusCode": 200}

    if not request.form:  # 检测是否有数据
        result_text['rc'] = 'fail'
    else:
        table = {
            '0': '/home/www/flask/nst/model/van_gogh.pth',
            '1': '/home/www/flask/nst/model/line_geometry.pth',
            '2': '/home/www/flask/nst/model/mona_lisa.pth',
            '3': '/home/www/flask/nst/model/rain_princess.pth',
            '4': '/home/www/flask/nst/model/starry_night.pth',
            '5': '/home/www/flask/nst/model/wave.pth',
            '6': '/home/www/flask/nst/model/plaid_portrait.pth',
            '7': '/home/www/flask/nst/model/obama_hope.pth',
            '8': '/home/www/flask/nst/model/sunday_afternoon.pth',
            '9': '/home/www/flask/nst/model/the_scream.pth',
        }
        ind = request.form.get('style')
        img64 = request.form.get('img')

        checkpoint_model = table[ind]

        byte_data = base64.b64decode(img64)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)

        device = torch.device("cpu")

        transform = style_transform()

        # Define model and load model checkpoint
        transformer = TransformerNet().to(device)
        transformer.load_state_dict(torch.load(checkpoint_model, map_location=torch.device('cpu')))
        transformer.eval()

        # Prepare input
        image_tensor = Variable(transform(img)).to(device)
        image_tensor = image_tensor.unsqueeze(0)

        # Stylize image
        with torch.no_grad():
            stylized_image = denormalize(transformer(image_tensor)).cpu()

        t = f"/home/www/flask/nst/tmp/{str(time.time())}.png"

        save_image(stylized_image, t)
        with open(t, "rb") as f:
            base64_str = base64.b64encode(f.read())

        os.remove(t)

        result_text['rc'] = base64_str.decode()

    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


if __name__ == '__main__':
    app.run(port=2306)
