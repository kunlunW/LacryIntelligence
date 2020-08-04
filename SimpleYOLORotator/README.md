Reference:
https://usmanr149.github.io/urmlblog/yolo/2020/03/05/rotate_yolo_bbox.html <br/>


How to run the code: <br/>
1. Go to your terminal/command prompt 
2. Activate the environment containing the proper packages of opencv2, numpy, and argparse
3. locate the current working directory 
4. use command: python rotate.py -i some_image.jpg -a some_angle

What the code does? 
Essentially we are trying to rotate the images, meanwhile maintaining the correct YOLO format annotation. 

As we know, the YOLO format annotation has the below format:
<img width="607" alt="Screen Shot 2020-08-04 at 9 06 23 AM" src="https://user-images.githubusercontent.com/52982585/89303472-da27bb80-d631-11ea-9a75-e18ef1c5724e.png">

