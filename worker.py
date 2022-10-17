import importlib
from tensorflow.keras.preprocessing import image
from log_manager import get_logger
import os
import random
import numpy as np

logger = get_logger()


def execute_job(job_ticket):
    """
    :param job_ticket: job_ticket received from task manager, In production worker should take the job ticket
    from a message queue.
    :return:
    """
    file_path = job_ticket['file']
    target_dir = job_ticket['target_dir']
    display_name = job_ticket['display_name']
    file_name = os.path.split(file_path)[1]
    augmentations = job_ticket['augmentations']
    image_array = get_image_array(file_path, job_ticket['input_image_size'])
    total_number_of_job = len(augmentations)
    for image_array, prefix in do_augmentation(display_name, image_array, augmentations[0]):
        save_image_to_train_test(image_array, target_dir, prefix + '_' + file_name, job_ticket['train_test_split'])
        if total_number_of_job >= 2:
            for sec_aug_img, sec_prefix in do_augmentation(display_name, image_array, augmentations[1]):
                save_image_to_train_test(sec_aug_img, target_dir, sec_prefix + '_' + file_name,
                                         job_ticket['train_test_split'])
        if total_number_of_job >= 3:
            for thd_aug_img, thd_prefix in do_augmentation(display_name, image_array, augmentations[2]):
                save_image_to_train_test(thd_aug_img, target_dir, thd_prefix + '_' + file_name,
                                         job_ticket['train_test_split'])


def do_train_test_split(source_dir, train_ratio, test_ratio):
    """
    :description: This is a placeholder function to do train test split after augmentation
    :param source_dir: directory where imagaes are located
    :param train_ratio: train ratio
    :param test_ratio: test ratio
    :return: list of train, test and validation image set
    """
    file_list = []
    validation = []
    for root_dir, dirs, files in os.walk(source_dir):
        file_list.extend([os.path.join(os.path.abspath(root_dir), file) for file in files if file.endswith('.jpeg')
                          or file.endswith('.png')])
    train = random.sample(file_list, int(len(file_list) * test_ratio/100))
    rest = [x for x in file_list if x not in train]
    if train_ratio + test_ratio == 1:
        logger.info("No validation set required")
        test = rest
    else:
        test = random.sample(rest, int(len(file_list) * test_ratio/100))
        validation = [x for x in rest if x not in test]
    return train, test, validation


def do_augmentation(display_name, raw_image, augmentation):
    """
    :description: This function will import the related module dynamically and execute the function to do
    the augmentation
    :param display_name: Name of the Job i.e MotoGp
    :param raw_image: image array as a input to do the augmentation
    :param augmentation: dictionary of augmentation parameter i.e type of augmentation , module name, function name etc
    :return: Generator of the augmented image array and a prefix
    """
    module_name = augmentation['module_name']
    pre_processing_function = augmentation['pre_processing_function']
    kwargs = augmentation['kwargs']
    aug_type = augmentation['name']
    try:
        module_obj = importlib.import_module('.' + module_name, package='modules')
        pre_processing_func = getattr(module_obj, pre_processing_function)
        logger.info(raw_image.shape)
        for out_img, prefix in pre_processing_func(raw_image, **kwargs):
            prefix_str = '_'.join(prefix)
            target_file_name = aug_type + '_' + prefix_str
            yield out_img, target_file_name
    except AttributeError as e:
        logger.error("Failed to import module {0} from {1} package".format(module_name, 'modules'))
        logger.error(str(e))
    except Exception as e:
        logger.error("Failed to do {0} on {1} data set".format(aug_type, display_name))
        logger.error(str(e))


def save_image_to_train_test(raw_image, target_dir, target_file_name, split_ratio=None):
    """
    :param split_ratio:
    :param raw_image: image array to save
    :param target_dir: location where to save the images
    :param target_file_name: name of the images
    :return:
    """
    if split_ratio:
        train_ratio = split_ratio['train_ratio']
    else:
        train_ratio = None
    try:
        if train_ratio:
            train_filter = 1 - train_ratio/100
            if np.random.rand(1) < train_filter:
                target_dir = os.path.join(target_dir, 'test')
                target_abs_path = os.path.join(target_dir, target_file_name)
                save_image(raw_image, target_abs_path)
            else:
                target_dir = os.path.join(target_dir, 'train')
                target_abs_path = os.path.join(target_dir, target_file_name)
                save_image(raw_image, target_abs_path)
        else:
            target_abs_path = os.path.join(target_dir, target_file_name)
            save_image(raw_image, target_abs_path)
    except Exception as e:
        logger.error("Failed to save images in directory {0}".format(str(target_abs_path)))
        logger.error(str(e))


def get_image_array(path, input_image_size=None):
    """
    :description: This function take the image path as an input and give image array as a output, image array get
    resized if input image size is given.
    :param path: jpeg, png or any other image input path
    :param input_image_size: By default it's none if you provide then images will be resized to the given size
    :return: Returns the image array
    """
    try:
        img = image.load_img(path)
        image_size = img.size
        if input_image_size:
            input_size = tuple(input_image_size)
            if image_size != input_size:
                img = img.resize(tuple(input_size))
        img_array = image.img_to_array(img)
        return img_array
    except FileNotFoundError:
        logger.error("Image not found {0}".format(path))
    except Exception as e:
        logger.error("Failed to load the image {0}".format(path.rsplit(os.sep, 1)[1]))
        logger.error(str(e))


def save_image(img, path):
    """
    :param img: image array
    :param path: absolute path of the target file
    :return:
    """
    try:
        image.save_img(path, img)
        logger.info("Done :: Image saved {0}".format(path.rsplit(os.sep, 1)[1]))
    except FileNotFoundError:
        os.mkdir(path.rsplit(os.sep, 1)[0])
        image.save_img(path, img)
        logger.info("Done :: Image saved {0}".format(path.rsplit(os.sep, 1)[1]))
    except Exception as e:
        logger.error("Failed to save the image in directory {0}".format(path))
        logger.error(str(e))


if __name__ == '__main__':
    # test_destination = '/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task/destination/test.jpeg'
    # kwargs = {
    #         "crop_dimensions": [
    #             [240, 240]
    #         ],
    #         "crop_type": "left_down_center"
    #     }
    # job_tickets = {
    #     "display_name": "MOTOGP",
    #     "file": '/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task/sample_frames/10wh903u4rtuc1k643aqepn4yi_main_443.jpeg',
    #     "module_name": 'crop',
    #     "pre_process_func": 'image_cropping',
    #     "post_processing_function": '',
    #     "target_dir": test_destination,
    #     "kwargs": kwargs,
    #     "aug_type": "Crop",
    # }
    # job_ticket = {'display_name': 'MotoGP', 'file': '/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task/sample_frames/10wh903u4rtuc1k643aqepn4yi_main_443.jpeg', 'target_dir': '/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task/destination/', 'augmentations': [{'name': 'CROP', 'module_name': 'crop', 'pre_processing_function': 'image_cropping', 'post_processing_function': '', 'kwargs': {'crop_dimensions': [[270, 270]], 'crop_type': 'left_down_center'}}, {'name': 'RANDOM_CROP', 'module_name': 'crop', 'pre_processing_function': 'image_random_cropping', 'post_processing_function': '', 'kwargs': {'crop_dimensions': [[80, 80]], 'crop_type': 'random', 'target_count': 3}}]}
    # execute_job(job_ticket)
    im_arr = get_image_array('/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task'
                             '/sample_frames/10wh903u4rtuc1k643aqepn4yi_main_443.jpeg', [480, 270])
    save_image(im_arr, 'test.jpeg')