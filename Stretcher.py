import os
import cv2
import glob
import numpy as np


blur_thickness=5;
gauss=1
offset=8;
blur_threshold=8
show=False

path_to_input_folder = input('Ścieżka do folderu ze zdjęciami: ')
if not path_to_input_folder:
    raise ValueError('Zła ścieżka! Uruchom program ponowanie')
path_to_output_folder = input('Ścieżka do folderu z wygenerowanymi zdjęciami: ')
if not path_to_output_folder:
    raise ValueError('Zła ścieżka! Uruchom program ponowanie')


file_search_string=os.path.join(path_to_input_folder, "*" + ".jpg")
jpg_files=glob.glob(file_search_string)
print("Wczytano %d zdjęć" % len(jpg_files))

for i, path in enumerate(jpg_files):
    file_name=os.path.splitext(os.path.basename(path))[0]
    print("Przetwarzanie pliku %s. Pozostało jeszcze %d plików" % (file_name,len(jpg_files)-(i+1)))
    img=cv2.imread(path)
    i_h=img.shape[0]
    i_w=img.shape[1]
    layer=np.zeros([i_h,i_w,3],dtype=img.dtype)

    for i in range(0,i_w-1):
        for j in range(i_h-1,0,-1):
            if(np.any(np.array(img[j,i,:])>blur_threshold)):
                img_min=img[(j-offset-blur_thickness):(j-offset),i,:]
                img_min_resize = cv2.resize(img_min, (3,(i_h-j)+offset+blur_thickness))
                layer[(j-offset-blur_thickness):i_h,i,:]=img_min_resize
                break

    r,thresh = cv2.threshold(layer, 1, 1, cv2.THRESH_BINARY)
    layer_gauss = cv2.GaussianBlur(layer, (gauss, gauss), 0)
    layer_gauss=layer_gauss*thresh

    result_img=img
    for i in range(0,i_w-1):
        for j in range(0,i_h):
            if(np.any(np.array(layer_gauss[j,i,:])!=0)):
                result_img[j:i_h,i,:]=layer_gauss[j:i_h,i,:]
                break

    output_path=os.path.join(path_to_output_folder, file_name +"_blur"+ ".jpg")
    cv2.imwrite(output_path, result_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    if show:
        cv2.namedWindow(file_name,cv2.WINDOW_NORMAL)
        cv2.imshow(file_name,result_img)

if show:
    cv2.waitKey(0)
    cv2.destroyAllWindows()

print("_____________________")m
print("Zakończono z SUKCESEM")