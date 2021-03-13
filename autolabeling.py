import cv2
import xml.etree.ElementTree as gfg  
import os
import time
import keyboard
import pyttsx3


def GenerateXML(fileName,folder_loc,name_CapImg , x_min , y_min , x_max, y_max,width,height): 
      
    root = gfg.Element("annotation") 
      
    
#root,filename, & folder tag
    folder_tag = gfg.SubElement(root, "folder") 
    folder_tag.text =str(folder_loc)
    
    filename_tag = gfg.SubElement(root, "filename") 
    filename_tag.text = name_CapImg + '.jpg'
    
#source tag further tags 
    source_tag = gfg.SubElement(root, "source") 
    
    database_tag = gfg.SubElement(source_tag, "database") 
    database_tag.text = "Unknown"
    
    
    annotation_tag = gfg.SubElement(source_tag, "annotation") 
    annotation_tag.text = "Unknown"
    
    image_tag = gfg.SubElement(source_tag, "image") 
    image_tag.text = "Unknown"

#size tag further 

    size_tag = gfg.SubElement(root, "size") 
    
    width_tag = gfg.SubElement(size_tag, "width") 
    
    width_tag.text = str(width)
    
    
    height_tag = gfg.SubElement(size_tag, "height") 
    
    height_tag.text = str(height)
    
    depth_tag = gfg.SubElement(size_tag, "depth") 
    depth_tag.text = "0"

# segmentated       
    segmentated_tag = gfg.SubElement(root, "segmentated") 
    segmentated_tag.text = "0"


#object tag further 

    object_tag = gfg.SubElement(root, "object") 
    
    name_tag = gfg.SubElement(object_tag, "name") 
    name_tag.text = name_CapImg
    
    
    occluded_tag = gfg.SubElement(object_tag, "occluded") 
    occluded_tag.text = "0"
    
    bndbox_tag = gfg.SubElement(object_tag, "bndbox") 
#bndbox tags
    xmin_tag = gfg.SubElement(bndbox_tag, "xmin") 
    xmin_tag.text = str(x_min)
    
    ymin_tag = gfg.SubElement(bndbox_tag, "ymin") 
    ymin_tag.text = str(y_min)
    
    xmax_tag = gfg.SubElement(bndbox_tag, "xmax") 
    xmax_tag.text = str(x_max)
    
    ymax_tag = gfg.SubElement(bndbox_tag, "ymax") 
    ymax_tag.text = str(y_max)
    
    
    
    tree = gfg.ElementTree(root) 
      
    with open (fileName, "wb") as files : 
        tree.write(files) 


def append_func(name_CapImg):
    #appending in a file in train.txt
    train_file_object = open(os.path.join(os.getcwd(),f'ImageSets/Main/train.txt'), 'a')
    train_file_object.write(f'{name_CapImg}\n')
    train_file_object.close()


    #appending in a file in traival.txt
    trainval_file_object = open(os.path.join(os.getcwd(),f'ImageSets/Main/trainval.txt'), 'a')
    trainval_file_object.write(f'{name_CapImg}\n')
    trainval_file_object.close()

    
    #appending in a file in labels.txt

    f = open("labels.txt", "a")
    f.write(f'{name_CapImg}\n')
    f.close()


def initialize_cv2(name_CapImg,x_min , y_min , x_max, y_max):
   
    cond = True
   
    while cond:
        key_board = keyboard.wait('s')
        while key_board == None:
            

            
            
            cam = " v4l2src device='/dev/video0' ! \
                    video/x-raw, width=640, height=480, format=(string)YUY2 ! \
                    xvimagesink -e"
            # cam=cv2.VideoCapture('/dev/video0')
            cam=cv2.VideoCapture(cam)



            ret,frame = cam.read()

            frame = cv2.rectangle(frame,(x_min,y_min),(x_max,y_max),(255,0,0),4)

            cv2.imshow('nanoCam',frame)

            cv2.moveWindow('nanoCam',0,0)

            #save path of current directory 
            time.sleep(1)
                



            save_path = f'./JPEGImages/'

            saved_img = cv2.imwrite(os.path.join(save_path, f'{name_CapImg}'+".jpg") ,frame)
            saved_img = cv2.imread(os.path.join(save_path, f'{name_CapImg}'+".jpg"), cv2.IMREAD_UNCHANGED)
            height = saved_img.shape[0]
            width = saved_img.shape[1]
            cam.release()
            cv2.destroyAllWindows()
            key_board = False
        cond = False

    return height,width
            
            
        

        

    


#def text_speech(name_CapImg):

 #   engine = pyttsx3.init()
  #  engine.say(f'Hi How are  {name_CapImg}')
   # engine.runAndWait()

# def error_text_speech_msg():

#     engine = pyttsx3.init()
#     engine.say(f'there is an error')
#     engine.runAndWait()




#bounding boxes dimensions 
x_min = 100
y_min = 150

x_max = 500
y_max = 480




cond = True 

while cond:
    
    if keyboard.wait('s') == None:

        name_CapImg = input("Please Enter the Name of the image \n")

        #text_speech(name_CapImg)
        
            
        i = 0

        while i<3:
            height,width = initialize_cv2(name_CapImg,x_min , y_min , x_max, y_max)        
            name_CapImg = str(name_CapImg + str(i)) 

            
            
            folder_loc = os.path.join(os.getcwd(),f'Annotations')

            file_name = os.path.join(folder_loc, f'{name_CapImg}'+".xml")


            GenerateXML(str(file_name), folder_loc,name_CapImg , x_min , y_min , x_max, y_max,width,height)
            append_func(name_CapImg)
            
            
            i+=1
        cond = False

    else:
        # error_text_speech_msg()
        print("error")


