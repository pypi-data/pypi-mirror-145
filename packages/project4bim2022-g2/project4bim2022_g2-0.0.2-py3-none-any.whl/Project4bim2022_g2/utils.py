import numpy as np
import cv2
import os
import tensorflow as tf
import matplotlib.pyplot as plt


def center_crop(image, out_height, out_width):
    """

    Args:
        image(numpy ndarray): list of floats representing the pixels of an image
        out_height(int) : height targeted
        out_width(int) : width targeted
    Return:
        image(numpy ndarray) : image of size out_height*out_width
    """
    input_height, input_width = image.shape[:2]
    offset_height = (input_height - out_height) // 2
    offset_width = (input_width - out_width) // 2
    image = image[offset_height:offset_height+out_height,
                  offset_width:offset_width+out_width, :]
    return image


def resize_maintain_aspect(image, target_h, target_w):
    """resize the image while maintaining the proportions

    Args:
        image (numpy ndarray): list of floats representing the pixels of an image
        target_h (int): targeted height
        target_w (int): targeted width

    Returns:
        ndarray: resized image
    """
    input_height, input_width = image.shape[:2]
    if input_height > input_width:
        new_width = target_w
        new_height = int(input_height*(target_w/input_width))
    else:
        new_height = target_h
        new_width = int(input_width*(target_h/input_height))

    image = cv2.resize(image, (new_width, new_height),
                       interpolation=cv2.INTER_CUBIC)
    return image


def save_dataset(path, imageList, height, width, channels, out):
    """method to save a list of images from a directory into a binary numpy array
    file .npy

    Args:
        path (string): path to the directory where the images are
        imageList (list<string>): list of the targeted images
        height (int): targeted height
        width (int): targeted width
        channels (int): color channels
        out (string): location where the file will be saved
    """
    # placeholder arrays for data and labels
    # data is float32, labels are integers
    x = np.ndarray(shape=(len(imageList), height,
                   width, channels), dtype=np.float32)

    # loop through all images
    for i in range(len(imageList)):
        # open image to numpy array
        img = cv2.imread(path + imageList[i])

        # do all the pre-processing…
        img = resize_maintain_aspect(img, height, width)
        img = center_crop(img, height, width)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = (img/255.0).astype(np.float32)

        # insert into placeholder array
        x[i] = img

    # write placeholder arrays into a binary npy file
    np.save(out, x)

    return None


# Acknowledgement to https://github.com/foolmarks/images_to_npy/blob/8b85c5d40346b7bf60ac340e42faa2bc5508b0cf/img_to_npy.py#L19


def load_dataset(split):
    """method to load the dataset from a .npy file with the 'split' name

    Args:
        split (string): names of the dataset targeted

    Returns:
        tensorflow.python.data.ops.dataset_ops.BatchDataset: Tensorflow Dataset containing the images
    """
    if os.path.exists('../img_align_celeba/{}.npy'.format(split)):
        list_ds = tf.data.Dataset.from_tensor_slices(
            np.load('../img_align_celeba/{}.npy'.format(split)))
        ds = list_ds.map(lambda x: (x, x))
        return ds
    else:
        print("save the data first")
        return None


def load_datasets():
    height = 64
    width = 64
    channels = 3
    out_train = '../img_align_celeba/dataset.npy'
    out_val = '../img_align_celeba/dataset_val.npy'
    out_test = '../img_align_celeba/dataset_test.npy'

    if not os.path.exists(out_test):
        path = "../img_align_celeba/training/"
        files = os.listdir(path)
        imageList_test = files[11001:12000]
        save_dataset(path, imageList_test, height, width, channels, out_test)
    if not os.path.exists(out_val):
        path = "../img_align_celeba/training/"
        files = os.listdir(path)
        imageList_val = files[10001:11000]
        save_dataset(path, imageList_val, height, width, channels, out_val)

    # Load the training, validation and testing datasets splits
    train_ds = load_dataset('dataset')
    val_ds = load_dataset('dataset_val')
    test_ds = load_dataset('dataset_test')

    # Batch the Dataset objects

    batch_size = 32
    train_ds = train_ds.batch(batch_size)
    val_ds = val_ds.batch(batch_size)
    test_ds = test_ds.batch(batch_size)

    return train_ds, val_ds, test_ds


def display_examples(ds):
    """Display a few examples

    Args:
        ds (Dataset): dataset from which we want the examples
    """
    n_examples_shown = 6
    f, axs = plt.subplots(1, n_examples_shown, figsize=(16, 3))

    for j, image in enumerate(ds.take(n_examples_shown)):
        axs[j].imshow(image[0])
        axs[j].axis('off')

    return None
