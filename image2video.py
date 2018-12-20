import cv2
import glob
import datetime

def GetImagesPaths(root_path, date = ''):
    if date == '':
        date = datetime.datetime.now().strftime("%Y%m%d")

    files_list = [i for i in glob.glob(root_path) if date in i]
    
    for i in files_list:
        img = cv2.imread(i)
        img = cv2.resize(img, (int(img.shape[1]/8), int(img.shape[0]/8)))
        img = cv2.flip(img, -1)
        cv2.imshow("233", img)
        cv2.waitKey(50)

if __name__ == "__main__":
    GetImagesPaths("./images/*", "20181219")