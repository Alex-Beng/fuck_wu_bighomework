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

def GetImage(root_path, delete_flag = True, save_flag = True, save_path = './images/'):
    # root_path = "storage/0E6F-D222/DCIM/Camera/"

    date = datetime.datetime.now().strftime("%Y%m%d")

    result = os.popen("adb shell ls "+ root_path).read()
    result_list = [i for i in result.split() if i != '' and date in i]
    
    if len(result_list) == 0:
        file_name = result.split()[0]
    else: 
        file_name = result_list[-1]

    path = root_path + file_name
    os.system("adb pull " + path + ' ' + save_path)
    if delete_flag:
        os.system("adb shell rm " + path)

    image = cv2.imread(save_path + file_name)
    if not save_flag:
        os.system("rm " + save_path + " " + file_name)
    return image


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