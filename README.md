# Analog-to-Digital-Conversion-of-Gauge-Meter-using-OpenCV

Conversion of Analog Reading from gauge into Digital Data using OpenCV

The Analog Gauge being used is of a tensiometer. The main motive of the project is to convert the values of the tensiometer into digital form.

Programmed in Python with OpenCV library for Image Processing

Used line and circle detection techniques

Hardware setup consisted of Raspberry Pi as the processing module along with a RPi Camera Module

In the Code, the user has to adjust certain parameters such as Binary Threshold, and parameters related to the HoughCircles() and HoughLinesP() depending upon the image quality and the gauge meter.

Also the scale of the Gauge meter needs to be taken care of. The scale of the Gauge meter attached above might not be the same as another Gauge meter's scale that you are using for your purpose.
