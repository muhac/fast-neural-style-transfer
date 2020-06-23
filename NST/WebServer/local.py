import os
import time
import base64
from PIL import Image

import torch
from torch.autograd import Variable
from torchvision.utils import save_image

from models import TransformerNet
from utils import *

if __name__ == "__main__":
    table = {
        0: '../server/model/van_gogh.pth',
        1: '../server/model/line_geometry.pth',
        2: '../server/model/mona_lisa.pth',
        3: '../server/model/rain_princess.pth',
        4: '../server/model/starry_night.pth',
        5: '../server/model/wave.pth',
        6: '../server/model/plaid_portrait.pth',
        7: '../server/model/obama_hope.pth',
        8: '../server/model/sunday_afternoon.pth',
        9: '../server/model/the_scream.pth',
    }

    for content in range(1, 9):
        for style in range(10):
            checkpoint_model = table[style]
            image_path = f'../model/images/contents/{content}.jpg'

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            transform = style_transform()

            # Define model and load model checkpoint
            transformer = TransformerNet().to(device)
            transformer.load_state_dict(torch.load(checkpoint_model))
            transformer.eval()

            # Prepare input
            image_tensor = Variable(transform(Image.open(image_path))).to(device)
            image_tensor = image_tensor.unsqueeze(0)

            # Stylize image
            with torch.no_grad():
                stylized_image = denormalize(transformer(image_tensor)).cpu()

            t = f"./{content}_{checkpoint_model.split('/')[-1].split('.')[0]}.png"

            save_image(stylized_image, t)
            with open(t, "rb") as f:
                base64_str = base64.b64encode(f.read())

            # os.remove(t)
            print(base64_str)
