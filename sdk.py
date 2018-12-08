import cv2 
import os
import time
import datetime

DEVICES_IP = str()

OPENED_CAMERA = False

def TakePhoto():
    global OPENED_CAMERA

    try:
        if not CheckStatus():
            return False

        result = os.popen("adb shell dumpsys activity | grep \"mFoc\" ").read()
        if "com.android.camera" in result:
            OPENED_CAMERA = True
        else:
            OPENED_CAMERA = False

        if not OPENED_CAMERA:
            os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")
            time.sleep(2)
    
        os.system("adb shell input keyevent 27")
        time.sleep(3)
    except:
        return False
    
    return True

def GetImgName():
    root_path = "storage/emulated/0/DCIM/Camera/"

    date = datetime.datetime.now().strftime("%Y%m%d")

    result = os.popen("adb shell ls "+ root_path).read()
    result_list = [i for i in result.split() if i != '' and date in i]
    
    if len(result_list) == 0:
        return result.split()[-1]
    return result_list[-1]

def GetImage(name):
    root_path = "storage/emulated/0/DCIM/Camera/"
    path = root_path + name
    os.system("adb pull " + path + " ./images")
    os.system("adb shell rm " + path)
    image = cv2.imread("./images/"+name)
    os.system("rm ./images/"+name)
    return image

# def ProcImage(image):
#     return 

def CheckStatus():
    global DEVICES_IP

    result = os.popen("adb devices").read()
    result_list = [i for i in result.split('\n') if i != '']

    status = len(result_list) > 1
    
    if status:
        return True
    else:
        print("The devices may not online...")
        if DEVICES_IP == '':
            print("and The DEVICES_IP is undefined!")
            DEVICES_IP = input("Please input DEVICES_IP : ")
    
        os.system("adb tcpip 5555")
        connect_result = os.popen("adb connect "+DEVICES_IP).read()
        if "unable to connect" in connect_result:
            return False
        else:  # connect may successfully
            result = os.popen("adb devices").read()
            result_list = [i for i in result.split('\n') if i != '']
            if len(result_list)>1:
                return True
            else:
                return False

def SetIP(IP):
    global DEVICES_IP
    DEVICES_IP = IP
    return 


if __name__ == "__main__":
    TakePhoto()
    time.sleep(3)
    image = GetImage(GetImgName())
    image = cv2.resize(image, (188, 250))
    cv2.imshow("233", image)
    cv2.waitKey()
    print(CheckStatus())