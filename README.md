# image-augmentation

You are working on a new computer vision project and are being asked to construct a data pipeline for loading and processing images. This pipeline will be used for initial model building for this project which will likely occur in a Jupyter notebook.
You have been provided with a .zip file containing some frames taken from DAZN content.
The objective of this assignment is to create a data pipeline that satisfies the following acceptance criteria:
• Read images from a local directory
• Ensure each image is 480 x 270 x 3 (Resize if required)
• Crop the image down to the central 270 x 270 x 3 region
• Randomly extract 3, 80 x 80 x 3 samples that do not overlap
• Allow for shuffling & separation into training & test sets. The proportions of which should be able to
be defined by the end user. Samples from the same image should not appear in both training and
test sets.
