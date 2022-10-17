from log_manager import get_logger
from config_manager import ConfigurationManager
from worker import execute_job
from multiprocessing import Process
import os

logger = get_logger()


def start_task(tasks_details):
    """
    :description: This Function will check the certain parameters in the input dictionary and call handle_task
    to create the job ticket
    :param tasks_details: It's a dictionary contains the details of the task it's going to execute
    :return: It will validate the input dictionary and send a response back either Success or Failed
    """
    for task_info in tasks_details:
        task_element = task_info.keys()
        if all(element in task_element for element in ['name', 'augmentations']):
            task = Process(target=handle_task, kwargs=task_info)
            task.start()
            logger.info("Started task {0}".format(task_info['name']))
        else:
            logger.error("Invalid request")
            return "Failed to load the task please double check !!"
    return "{0} tasks started".format(len(tasks_details))


def crawl_dir(source_directory):
    """
    :description: This function is to crawl the given directory and return a generator of the images
    :param source_directory: Directory to crawl and find out all the images
    :return: Generator of the image's absolute path
    """
    for root_dir, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith('.jpeg') or file.endswith('.png'):
                file_absolute_path = os.path.join(os.path.abspath(root_dir), file)
                yield file_absolute_path


def handle_task(name, augmentations, train_test_split=None, input_image_size=None):
    """
    :description: This function will merge the user input with the configuration and create a job ticket for
    each images and then worker will further process the images. For this project I am directly sending the
    request to worker in production it should go to a message queue and and worker should consume it from a queue
    this way we can achieve high level of parallelism.
    :param name: Name of the task it's going to handle.
    :param augmentations: List of dictionary containing the augmentation details.
    :param train_test_split: Dictionary of train test split ratio.
    :param input_image_size: If provided it will resize the images as per this parameter else it will consider
    the size of the raw images.
    :return: Create a job ticket and submit it to worker to process them images.
    """
    conf = ConfigurationManager('dev')
    data_source = conf.get_data_source(name)
    source_dirs = data_source['source_dir']
    target_dir = data_source['target_dir']
    for source_dir in source_dirs:
        for file in crawl_dir(source_dir):
            for aug in augmentations:
                merged_aug_parameters = []
                for aug_type in list(aug.keys()):
                    aug_parameters = conf.get_aug_parameters(aug_type)
                    aug_parameters['kwargs'] = aug[aug_type]
                    merged_aug_parameters.append(aug_parameters)
                job_ticket = {
                    "display_name": name,
                    "file": file,
                    "target_dir": target_dir,
                    "augmentations": merged_aug_parameters,
                    "train_test_split": train_test_split,
                    "input_image_size": input_image_size
                }
                execute_job(job_ticket)
    logger.info("Done Task {0}".format(name))


if __name__ == '__main__':
    user_req = [
            {
                "name": "MotoGP",
                "augmentations": [
                  {
                    "CROP": {
                      "crop_dimensions": [
                          [240,240]
                       ],
                      "crop_type": "left_down_center"
                    }
                  }
                ]
            }
        ]
    start_task(user_req)
