from log_manager import get_logger

log = get_logger()


def image_cropping(raw_img, crop_dimensions, crop_type='random'):
    """
    :param raw_img: input image array
    :param crop_dimensions: list of dimensions for the cropping
    :param crop_type: crop type , towards center or random etc
    :return: generator of cropped image array and a prefix
    """
    for dim in crop_dimensions:
        try:
            crop_dy, crop_dx = dim[0], dim[1]
        except IndexError:
            log.error("Please pass the appropriate dimension of the log")
            raise ValueError("Please provide the dimension in list of list format")
        if crop_type == 'left_down_center':
            yield raw_img[0:crop_dy, 0:crop_dx, :], [str(crop_dy), str(crop_dy)]
        if crop_type == 'random':
            log.error("This type of cropping is not implemented")
            raise ValueError("Right Now crop except only left down center")


if __name__ == '__main__':
    # test_destination = '/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task/destination/test.jpeg'
    # for img in image_cropping('/Users/surajitkundu/Google Drive/Cloud & DevOps/ML Tasks/ML Engineer task/sample_frames'
    #                           '/10wh903u4rtuc1k643aqepn4yi_main_443.jpeg', [[270, 270]], crop_type='left_down_center'):
    #     save_image(img, test_destination)
    # image_array = get_image_array('')
    # aug_images = do_crop(image_array, [[270, 270]], crop_type='left_down_center')
    # for aug_img in aug_images:
    #     save_image(aug_img, '')
    pass
