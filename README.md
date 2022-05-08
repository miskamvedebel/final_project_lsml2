# final_project_lsml2
HSE LSML2 final project


Idea: web app - where user can upload the picture and model will identify what food is it.

High-level architecture:
1. fastAPI - as backend for the webapplication;
2. pytorch model (resnet50) to make predictions;

# The dataset 
(https://www.kaggle.com/datasets/kmader/food41?resource=download):

The dataset contains a number of different subsets of the full food-101 data. The idea is to make a more exciting simple training set for image analysis than CIFAR10 or MNIST. For this reason the data includes massively downscaled versions of the images to enable quick tests. The data has been reformatted as HDF5 and specifically Keras HDF5Matrix which allows them to be easily read in. The file names indicate the contents of the file. For example:
 - foodc101n1000_r384x384x3.h5 means there are 101 categories represented, with n=1000 images, that have a resolution of 384x384x3 (RGB, uint8)
 - foodtestc101n1000r32x32x1.h5 means the data is part of the validation set, has 101 categories represented, with n=1000 images, that have a resolution of 32x32x1 (float32 from -1 to 1)

(The data was repackaged from the original source (gzip) available at https://www.vision.ee.ethz.ch/datasets_extra/food-101/)

# The model architecture:

It was decided to use pretrained RESNET50 available in pytorch package. Last fully connected layer has been changed accordingly, as 101 classes are represented in the dataset. The architecture of the net as follows:

![Architecture](picture.png)


