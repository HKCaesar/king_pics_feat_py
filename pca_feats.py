#-*- coding:utf-8 -*-
'''
��ͼ�������о���ֽ⣬�õ��������ɷ֣��õ�ͼ��Ľṹ��Ԫ
��Ҫ˼�룺ÿһ��ͼ���СΪm*n�ľ��󣬱�Ϊm*n���ȵ���������S��ͼ�����Կ������S * (m*n)�ľ���Ȼ����зֽ��S * K�ľ������K * (m*n)�ľ���
���õ���K��(m*n)�ķ���������Щ�����ṹ��Ԫ��
'''

from PIL import Image
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

IMAGE_SIZE = 64
# ����ͼƬ����ÿ����ɫͼ���ΪRGB��ͨ��
# RGB��ͨ������ͼ����󣬲�ˮƽ��ת
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

# ��׼��
scaler = StandardScaler()
scaler.fit(imgs_arrays)
imgs_arrays = scaler.transform(imgs_arrays)
print(np.mean(imgs_arrays[:, 0]), np.var(imgs_arrays[:, 0]))

# PCA��ά
pca = PCA(n_components = 80)
pca.fit(imgs_arrays)
comps = pca.components_

print(np.sum(pca.explained_variance_ratio_))
print(pca.n_components_)
print(comps.shape)

for i, com in enumerate(comps):
    if i % 10 != 0:
        continue
    img_comp = com.reshape(IMAGE_SIZE, IMAGE_SIZE)
    plt.figure()
    plt.imshow(img_comp)
    plt.show()