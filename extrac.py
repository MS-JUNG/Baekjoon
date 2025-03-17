
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4 # To use 40% of memory
set_session(tf.Session(config=config))

import os
import numpy as np
import argparse
from colorcorrect.util import from_pil, to_pil
from colorcorrect import algorithm as cca
from tqdm import tqdm
from keras.applications.resnet50 import ResNet50
from keras.models import Model
from keras.applications.resnet50 import preprocess_input
from PIL import Image


def extract_and_save_features(path_to_tiles,
                              path_to_save_features):
    """Extract ResNet features from tile images.
    """
    model = ResNet50(weights='imagenet', include_top=True)
    model = Model(inputs=model.inputs, outputs=model.get_layer('avg_pool').output)

    if not os.path.exists(path_to_save_features):
        os.mkdir(path_to_save_features)
    for cat in ['ADI', 'MUC', 'BACK', 'LYM', 'NORM', 'DEB', 'MUS', 'STR', 'TUM']:
        X = []
        for filename in tqdm(os.listdir(os.path.join(path_to_tiles, cat))):
            try:
                tile = Image.open(os.path.join(path_to_tiles, cat, filename))
                tile = to_pil(cca.stretch(from_pil(tile)))
                tile = np.array(tile)
                features = model.predict(preprocess_input(tile[np.newaxis]), batch_size=1)
                X.append(features)
            except ZeroDivisionError:
                pass
        np.save(os.path.join(path_to_save_features, f'{cat}.npy'), np.array(X))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_to_tiles", help="path to folder containing tile images",
                        default='/data/home/brian1501/Minsu/MAI/train')
    parser.add_argument("--path_to_save_features", help="path to save features as npy files",
                        default='/data/home/brian1501/Minsu/MAI/train_feature')
    args = parser.parse_args()
    extract_and_save_features(
        path_to_tiles=args.path_to_tiles,
        path_to_save_features=args.path_to_save_features
    )
        
if __name__ == '__main__':
    main()