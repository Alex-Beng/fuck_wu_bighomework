from sdk import *

import cv2
import numpy as np
import time
import os
import math

if __name__ == "__main__":

    print("Need pre-take to get parameter...")
    TakePhoto()
    image = GetImage("storage/0E6F-D222/DCIM/Camera/")
    print("Pre-take done.")
    print()

    video_path = input("Where do you want to save the generated video?(end with '/') : ")
    save_img_flag = int(input("Do you want to save all images in your phone?(0/1) : "))
    if save_img_flag:
        save_img_path = input("Where do you want to save the image?(end with '/') : ")
    else:
        save_img_path = ''
    rm_img_flag = int(input("Do you want to remote the image in your devices? (0/1) : "))
    show_img_flag = int(input("Do you want to show the images while capturing?(0/1) :"))

    real_time  = float(input("How long are the real time you want?(in seconds) : "))    
    video_time = float(input("How long are the video you want to generate?(in seconds) : "))
    FPS        = int(input("What about frame per second?"))
    print()

    frame_nums = math.ceil(video_time*FPS) 
    interval   = real_time/frame_nums

    print("So you need to keep this thread alive for at least", 6*frame_nums, 's')
    print("And the interval should be %f and the sum of frames is %d"%(interval, frame_nums))
    print()

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videowriter = cv2.VideoWriter(video_path+"demo.avi",fourcc,FPS,(image.shape[1],image.shape[0]))
    
    
    now_time = time.time()
    
    print("Begin to run !\n")
    try:
        for i in range(frame_nums):
            print("Frame %d"%i)

            if i%10 == 0: # keep camera alive
                os.system("adb shell input tap 100 1800")

            TakePhoto()
            image = GetImage("storage/0E6F-D222/DCIM/Camera/", rm_img_flag, save_img_flag, save_img_path)
            
            if show_img_flag: 
                for_show = cv2.resize(image, (image.shape[1]//16, image.shape[0]//16))
                cv2.imshow("233", for_show)
                cv2.waitKey(500)
            
            videowriter.write(image)
            print("the connection valid? :", CheckStatus())

            t_interval = time.time()-now_time
            print("current time interval :", t_interval)
            if t_interval < interval:
                time.sleep(interval-t_interval)
            else:
                print("抱歉，我不是香港记者...")
            now_time = time.time()
            print()
        videowriter.release()
    except:
        videowriter.release()