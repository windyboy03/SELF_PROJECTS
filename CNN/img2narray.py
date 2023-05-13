import cv2
import glob
import numpy as np

def get_data_from_folder(path, class_names=[], IMG_SIZE=32):
    data = []
    for class_name in class_names:
        try:
            files = glob.glob(path+"/"+class_name+"/*")
            for f in files:
                img = cv2.imread(f)
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                img = np.transpose(img, (2, 0, 1))  # Swap axis to match expected input shape of the CNN model
                data.append([np.array(img), class_names.index(class_name)])
        except:
            pass
    np.random.shuffle(data)
    return data
