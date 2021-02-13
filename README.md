# XAOM: A method for automatic alignment and orientation of radiographs for computer-aided medical diagnosis

XAOM: X-ray Alignment and Orientation Method is a two-stage method for X-ray image alignment and orientation. The first stage of the XAOM is aligning images, while the second stage is orienting them by giving an orientation label (north, south, east, west). The labels and set standard is given in the notebook and in the image "Standard.png".

---

The "DataExamples" folder contains representative X-ray images for each body part so the user can test the proposed method.


---

In the "Notebooks" folder, you can find the "XAOM.ipynb" that is utilizing the proposed method with full comments. The required TensorFlow version is ">2.0.0". 
The necessary "VGG16" model can be obtained from the following link: https://drive.google.com/file/d/1HIsqdnSUe_BFAtN-jB9lWMfTlgfPBYqC/view?usp=sharing

---

Last but not least, in "ExporDicomToPng" we offer a tool for exporting pixel data of the medical "Dicom" files to ".png" files that the proposed method uses.
