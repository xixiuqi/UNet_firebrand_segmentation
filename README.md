# UNet_firebrand_segmentation

The repository is to create a ML configuration that uses UNet to identify the firebrands from images. 

---

## Data

The data are from the videos of firebrand generation experiments. Initial labelling is conducted manually through labelme [https://github.com/labelmeai/labelme]. 
The sample images can be found in folder ./Datalabelme

## Data Augmentation

Data augmentation is through Augmentor [https://github.com/mdbloice/Augmentor].
Associated pre-processing including moving files and change names can be found in folder ./DataAugumentation

## Model

Unet model can be found online. Reference goes [https://arxiv.org/abs/1505.04597]. The model is in UNetforfirebrand.ipynb. The famous network

![u-net-architecture.png](u-net-architecture.png)

## Training

The model is trained with 100 epochs.

---

## Results

With 100 epochs. the loss figure shows the convergence. 

![Results/loss.png](Results/loss.png)

The test image is

![Results/test.jpg](Results/test.jpg)

And the overlap between the predictions and ground-truth(manual labeled) is

![Results/overlay_image.jpg](Results/overlay_image.jpg)

The red ones are from ground-truth and white ones are from predictions. Most of the firebrand can be captured if my labelings are correct.
