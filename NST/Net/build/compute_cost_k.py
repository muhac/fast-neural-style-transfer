import numpy as np
from keras import backend as K
from efficientnet.keras import center_crop_and_resize, preprocess_input


class Cost(object):
    def __init__(self, style, model):
        self.model = model
        self.get_layer_output = K.function([self.model.layers[0].input, K.learning_phase()],
                                           [self.model.layers[49].output,   # 49:  block1d_add
                                            self.model.layers[152].output,  # 152: block2g_add
                                            self.model.layers[255].output,  # 255: block3g_add
                                            self.model.layers[403].output,  # 403: block4j_add
                                            self.model.layers[551].output,  # 551: block5j_add
                                            self.model.layers[744].output,  # 744: block6m_add
                                            self.model.layers[802].output,  # 802: block7d_add
                                            self.model.layers[808].output,  # 808: probs
                                            ])

        self.S_img = style
        self.Ss = self.get_outputs(self.S_img)

    def get_outputs(self, img):
        img_size = self.model.input_shape[1]
        x = center_crop_and_resize(img, image_size=img_size)
        x = preprocess_input(x)
        x = np.expand_dims(x, 0)
        out = self.get_layer_output([x, 0])
        return out

    def content_cost(self, C, G):
        m, h, w, c = C.shape

        C = C.reshape(m, -1, c)
        G = G.reshape(m, -1, c)

        J_content = np.sum((C - G) ** 2) / (4 * h * w * c)
        return J_content

    def style_cost(self, Ss, Gs):
        def style_cost_layer(S, G):
            m, h, w, c = S.shape

            S = S.T.reshape(c, h * w)
            G = G.T.reshape(c, h * w)

            GS = np.matmul(S, S.T)
            GG = np.matmul(G, G.T)

            J_style_layer = np.sum((GS - GG) ** 2) / (2 * h * w * c) ** 2
            return J_style_layer

        J_style = sum(style_cost_layer(Ss[i], Gs[i]) for i in range(len(Ss)))
        return J_style

    def cost(self, content, generation, alpha=10, beta=40):
        Cs = self.get_outputs(content)
        Gs = self.get_outputs(generation)

        J_content = self.content_cost(Cs[-3], Gs[-3])
        J_style = self.style_cost(self.Ss[1:-3], Gs[1:-3])

        J = alpha * J_content + beta * J_style
        return J
