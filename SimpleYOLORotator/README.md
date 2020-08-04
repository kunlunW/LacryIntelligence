# **Reference:** <br/>
https://usmanr149.github.io/urmlblog/yolo/2020/03/05/rotate_yolo_bbox.html <br/>


# **How to run the code:** <br/>
1. Go to your terminal/command prompt 
2. Activate the environment containing the proper packages of opencv2, numpy, and argparse
3. locate the current working directory 
4. use command: `python rotate.py -i some_image.jpg -a some_angle`

# **What the code does?** <br/>
Essentially we are trying to rotate the images, meanwhile maintaining the correct YOLO format annotation. 

# **YOLO format Annotation** <br/>
As we know, the YOLO format annotation has the below format:
<img width="607" alt="Screen Shot 2020-08-04 at 9 06 23 AM" src="https://user-images.githubusercontent.com/52982585/89303472-da27bb80-d631-11ea-9a75-e18ef1c5724e.png"> <br/>
where the W is the width of the image and the H is the height of the image. And bbox_width and bbox_height are the width and height of each bounding box we made. 

# **Rotation matrix** <br/>
If we want to rotate a point by (x,y) counterclockwise by a certain angle *theta*, then we can apply the below rotation matrix: 
<img width="204" alt="Screen Shot 2020-08-04 at 9 12 53 AM" src="https://user-images.githubusercontent.com/52982585/89304148-ba44c780-d632-11ea-9e56-5051f0cd0104.png"> <br/>
And to abtain the new position, we can basically multiply the current position (x,y) by the rotation matrix: 
<img width="368" alt="Screen Shot 2020-08-04 at 9 14 32 AM" src="https://user-images.githubusercontent.com/52982585/89304561-30e1c500-d633-11ea-8258-f5b52220cdbe.png"> <br/> 

# **Determine eew width and new hieght** <br/>
Once we have rotated all four corners of the bounding box this way, we need to find the 2 farthest rotated points along the the x-axis (this will correspond to the new width of the new bounding box) and the y-axis (this will correspond to the new height of the bounding box): 
<img width="425" alt="Screen Shot 2020-08-04 at 9 17 39 AM" src="https://user-images.githubusercontent.com/52982585/89304901-9fbf1e00-d633-11ea-8a8e-a0b80342891e.png"> <br/>

The old bounding box is in blue, the new rotated bounding box is in red. The new bounding box whose dimensions we need for YOLO is shown in black.<br/>

We need to recalculate the height and width of the rotatd box this way because YOLO only takes in bounding boxes parallel to the x-y axis.

# **Code explanation** <br/> 
## `class yoloRotatebbox:` <br/>
initialize name of the image, its extension and the angle you want to rotate <br/>

## `def rotate_image(self):` <br/>
Rotating the image easy using cv2. <br/>

## `def rotateYolobbox(self):` <br/>
Once we have the image name and the rotated image dimension, we can read in the .txt file that has the bounding box information from Yolo_mark and rotate the bounding the box. <br/>



