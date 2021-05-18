# ObjectDetection_Yolov4

An object detection end-to-end application built to identify beach plastics and detect them.

## Abstract

A streamlined process of classifying and detecting beach litter. This is done by using an object detection model YOLOv4 suing transfer learning 
which takes in images of size (416,416) and classifies and deetcts the litter class from the four labels/classes in the dataset. The dataset was built using google images and social media images and using LabelImg tool manually annotated images.
This model is exposed as an API using a flask server and for this React server acts as a front end component. The React component or the front-end
of the application displays the detected image with bounding boxes drawn for the objects on the image.

## Technology stack
*Programming languages & Libraries*: Python, keras, scikit-learn, tensorflow

*Technologies*: Machine Learning, Computer Vision, Deep Learning

*Web Technologies*: HTML5, CSS3, JavaScript, React, Redux, Node.JS, REST API(flask)

*Miscellaneous* : SOA, Agile, Git, Anaconda

## Steps to run the application
0. Clone the repository
1. Once you're in the repo, create a conda virtual environment and install the dependancies and required libraries using the following commands

*conda env create -f conda-cpu.yml (replace with condo-gpu.yml if GPU is available)*

*conda activate (Activating the virtual env)*

2. Up the backend server by running app_v2.py python file within the virtual environment
	 *$python app.py*
3. Run the front-end React Server in the directory of base_react_app by executing the command 
	 *$npm i *
	to install the node modules
4. After installing the node modules run the following command to start the front-end server
	*$npm start*
5. The front-end server redirects to http://localhost:3000 there you can upload the image you want to detect which displays the 
detected image along with the embedded	bounding boxes in the image

## Sample Output
<img width="900" alt="sample output" src="https://github.com/SantoshBoga/ObjectDetection_Yolov4/blob/master/base_react_app/src/detections/beach_bottles_detection.jpg">
