import os
import cv2
import glob

blur_height=722;
blur_thickness=5;
gauss=51
rand_gauss=6
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
    img_min=img[(i_h-blur_height):(i_h-blur_height+blur_thickness),:,:]
    img_min_resize=cv2.resize(img_min, (i_w, blur_height))
    img_min_resize_gauss=cv2.GaussianBlur(img_min_resize,(gauss,gauss),0)


    img_result=img
    img_result[i_h-blur_height:i_h,:,:]=img_min_resize_gauss
    img_result[i_h-blur_height-rand_gauss:i_h-blur_height+rand_gauss]=cv2.GaussianBlur(img_result[i_h-blur_height-rand_gauss:i_h-blur_height+rand_gauss],(5,5),0)

    output_path=os.path.join(path_to_output_folder, file_name +"_blur"+ ".jpg")
    cv2.imwrite(output_path, img_result, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    if show:
        cv2.namedWindow(file_name,cv2.WINDOW_NORMAL)
        cv2.imshow(file_name,img_result)

if show:
    cv2.waitKey(0)
    cv2.destroyAllWindows()

print("_____________________")
print("Zakończono z SUKCESEM")