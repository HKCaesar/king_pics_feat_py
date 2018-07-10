#-*- coding:utf-8 -*-
'''
NMF�Ǹ�����ֽ�
��ͼ�������о���ֽ⣬�õ��������ɷ֣��õ�ͼ��Ľṹ��Ԫ
��Ҫ˼�룺ÿһ��ͼ���СΪm*n�ľ��󣬱�Ϊm*n���ȵ���������S��ͼ�����Կ������S * (m*n)�ľ���Ȼ����зֽ��S * K�ľ������K * (m*n)�ľ���
���õ���K��(m*n)�ķ���������Щ�����ṹ��Ԫ��
'''

from PIL import Image
import numpy as np
import os
from sklearn.decomposition import NMF
from matplotlib import pyplot as plt

IMAGE_SIZE = 64
# ����ͼƬ����ÿ����ɫͼ���ΪRGB��ͨ��
# ����ͨ���ֱ����ͼ����󣬲�����ˮƽ��ת
def load_pics(pics_dir):
    pics_files = [os.path.join(pics_dir, fname) for fname in os.listdir(pics_dir)]
    imgs_arrays = []
    for img_path in pics_files:
        img = Image.open(img_path)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        img_array = np.array(img, dtype = np.float64)
        img_red_array = img_array[:, :, 0]
        img_green_array = img_array[:, :, 1]
        img_blue_array = img_array[:, :, 2]
        
        imgs_arrays.append(img_red_array.flatten())
        imgs_arrays.append(img_green_array.flatten())
        imgs_arrays.append(img_blue_array.flatten())
        
        imgs_arrays.append(img_red_array[:,::-1].flatten())
        imgs_arrays.append(img_green_array[:,::-1].flatten())
        imgs_arrays.append(img_blue_array[:,::-1].flatten())
        
    imgs_arrays = np.array(imgs_arrays)
    return imgs_arrays

# ����ͼƬ: ͼƬ���� * ͼƬ���ص�
imgs_arrays = load_pics(pics_dir = "pics/norm_small_pics")
print(imgs_arrays.shape)

# NMF����ֽ�
nmf = NMF(n_components = 80)
nmf.fit_transform(imgs_arrays)
comps = nmf.components_


for i, com in enumerate(comps):
    img_comp = com.reshape(IMAGE_SIZE, IMAGE_SIZE)
    plt.figure()
    plt.imshow(img_comp)
    plt.show()