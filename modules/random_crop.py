from log_manager import get_logger
from random import choice
import math

logger = get_logger()


def get_random_indices(height, width, crop_dy, crop_dx, y_exception_indices, x_exception_indices):
    """
    This function will give you a random center without overlap based on the image height width and cropping dimension
    :param height: height of the image i.e 270
    :param width: width of the image i.e 270
    :param crop_dy: crop dimension i.e 80
    :param crop_dx: crop dimension x i.e 80
    :param y_exception_indices: list of y pixel position which can't be considered to make sure no overlap
    :param x_exception_indices:list of x pixel position which can't be considered to make sure no overlap
    :return: returns the two random pixel indices which will be used for cropping
    """
    try:
        rand_y_indices = choice([i for i in range(math.ceil(crop_dy / 2), math.ceil(height - (crop_dy / 2)))
                                 if i not in y_exception_indices])
        rand_x_indices = choice([i for i in range(math.ceil(crop_dy / 2), math.ceil(width - (crop_dx / 2)))
                                 if i not in x_exception_indices])
        return rand_y_indices, rand_x_indices
    except IndexError as e:
        logger.error("No More random index can be generated")
        logger.error(str(e))
        return 0, 0


def image_random_cropping(image_array, crop_dimensions, target_count):
    """
    :param image_array: input image array
    :param crop_dimensions: dimension of crop
    :param target_count: Number of random crop i.e 2 or 3
    :return: Generator of the cropped image
    """
    height, width = image_array.shape[0], image_array.shape[1]
    crop_dy, crop_dx = crop_dimensions[0], crop_dimensions[1]
    y_exception_indices = []
    x_exception_indices = []
    for i in range(target_count):
        rand_y_indices, rand_x_indices = get_random_indices(height, width, crop_dy, crop_dx,
                                                            y_exception_indices, x_exception_indices)
        y_exception_indices.extend([i for i in range(rand_y_indices - crop_dy, rand_y_indices + crop_dy)])
        x_exception_indices.extend([i for i in range(rand_x_indices - crop_dx, rand_y_indices + crop_dx)])
        if rand_y_indices != 0 or rand_x_indices != 0:
            yield image_array[rand_y_indices - 40:rand_y_indices + 40, rand_x_indices - 40:rand_x_indices + 40, :], [
                str(crop_dy), str(crop_dy), str(i)]


if __name__ == '__main__':
    # image_array = get_image_array('/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task/'
    #                               'sample_frames/10wh903u4rtuc1k643aqepn4yi_main_443.jpeg')
    # for out_img, prefix in image_random_cropping(image_array, [80, 80], 3):
    #     save_image(out_img, '/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task/destination/' +
    #                '_'.join(prefix) + '.jpeg')
    pass
