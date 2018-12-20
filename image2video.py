import cv2
import glob
import datetime
import shutil
import os

def GetImagePaths(root_path, date = ''):
    if date == '':
        date = datetime.datetime.now().strftime("%Y%m%d")

    file_path_list = [i for i in glob.glob(root_path) if date in i]
    # image_list = [cv2.imread(i) for i in file_path_list]

    # for i in files_list:
    #     t_img = cv2.imread(i)
    #     image_list.append(t_img) 

    return file_path_list

def VideoMake(paths_list, save_path, shape, fps = 25):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    Videomaker = cv2.VideoWriter(save_path+"demo.avi", fourcc, fps,(shape[1], shape[0]))
    for i in paths_list:
        img = cv2.imread(i)
        Videomaker.write(img)
    Videomaker.release()

def MoveImage2Else(paths_list, else_path):
    if not os.path.exists(else_path):
        try:
            os.makedirs(else_path)
        except:
            print("error in mkdir")
    for i in paths_list:
        try:
            shutil.move(i, else_path)
        except:
            print("error in moving files")
            

if __name__ == "__main__":
    path_lists = ["./222.txt"]
    MoveImage2Else(path_lists, "./233/")

    img_paths =  GetImagePaths("./images/*", "20181219")
    # for i in img_paths:
    #     img = cv2.imread(i)
    #     img = cv2.resize(img, (int(img.shape[1]/8), int(img.shape[0]/8)))
    #     img = cv2.flip(img, -1)
    #     cv2.imshow("233", img)
    #     cv2.waitKey(50)
    img = cv2.imread(img_paths[7])
    VideoMake(img_paths, "./", img.shape)

    