import numpy as np
import tensorflow as tf

import skimage
import skimage.io
import skimage.transform

import vgg19

def load_image(path):
    # load image
    img = skimage.io.imread(path)
    img = img / 255.0
    assert (0 <= img).all() and (img <= 1.0).all()
    # print "Original Image Shape: ", img.shape
    # we crop image from center
    short_edge = min(img.shape[:2])
    yy = int((img.shape[0] - short_edge) / 2)
    xx = int((img.shape[1] - short_edge) / 2)
    crop_img = img[yy: yy + short_edge, xx: xx + short_edge]
    # resize to 224, 224
    resized_img = skimage.transform.resize(crop_img, (224, 224))
    return resized_img


class Cost(object):
    def __init__(self, style, device='/cpu:0'):
        self.device = device
        self.style_img = load_image(style).reshape((1, 224, 224, 3))

        with tf.device(self.device):
            with tf.compat.v1.Session() as sess:
                images = tf.compat.v1.placeholder("float", [1, 224, 224, 3])
                feed_dict = {images: self.style_img}

                vgg = vgg19.Vgg19()
                with tf.name_scope("content_vgg"):
                    vgg.build(images)

                self.Ss = sess.run([vgg.prob, vgg.pool1, vgg.pool2, vgg.pool3, vgg.pool4, vgg.pool5],
                                   feed_dict=feed_dict)

    def get_outputs(self, img):
        image = load_image(img).reshape((1, 224, 224, 3))

        with tf.device(self.device):
            with tf.compat.v1.Session() as sess:
                images = tf.compat.v1.placeholder("float", [1, 224, 224, 3])
                feed_dict = {images: image}

                vgg = vgg19.Vgg19()
                with tf.name_scope("content_vgg"):
                    vgg.build(images)

                out = sess.run([vgg.prob, vgg.pool1, vgg.pool2, vgg.pool3, vgg.pool4, vgg.pool5], feed_dict=feed_dict)

        return out

    @staticmethod
    def content_cost(C, G):
        m, h, w, c = C.shape

        C = C.reshape(m, -1, c)
        G = G.reshape(m, -1, c)

        J_content = np.sum((C - G) ** 2) / (4 * h * w * c)
        return J_content

    @staticmethod
    def style_cost(Ss, Gs, Ks):
        def style_cost_layer(S, G):
            m, h, w, c = S.shape

            S = S.T.reshape(c, h * w)
            G = G.T.reshape(c, h * w)

            GS = np.matmul(S, S.T)
            GG = np.matmul(G, G.T)

            J_style_layer = np.sum((GS - GG) ** 2) / (2 * h * w * c) ** 2
            return J_style_layer

        J_style = sum(Ki * style_cost_layer(Si, Gi) for Si, Gi, Ki in zip(Ss, Gs, Ks))
        return J_style

    def cost(self, content, generation, alpha=10, beta=40):
        Cs = self.get_outputs(content)
        Gs = self.get_outputs(generation)

        J_content = self.content_cost(Cs[4], Gs[4])
        J_style = self.style_cost(self.Ss[1:4], Gs[1:4], np.ones(3))

        J = alpha * J_content + beta * J_style

        return J, J_content, J_style
