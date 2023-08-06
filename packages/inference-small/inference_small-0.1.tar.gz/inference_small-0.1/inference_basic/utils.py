import cv2
import cv2 as cv
import numpy as np
import os
class Utils():
    
    def repalce_dict(self,cls):
        values = {'0_5': 0,
         '6_15': 1,
         '16_25': 2,
         '26_35': 3,
         '36_50': 4,
         '51_65': 5,
         '66_8S0': 6,
         '81_110': 7,
         '111_above': 8}
        for key,val in values.items():
            if val==cls:
                return key

    def dis_im(self,img,title='presented_image'):
    #     img = transforms.functional.to_pil_image(img)
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow(f"{title}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def logo(self,img_t,level):  
        
        low_val = int(level.split('_')[0])
        val_found = int(((int(level.split('_')[1])-low_val)/2)+low_val) if low_val<110 else 130
        model_dir = os.path.join(os.getcwd(),'images')
        logo_path = os.path.join(model_dir, 'logo.jpg')
        logo = cv2.imread(logo_path)
        
        x = int(img_t.shape[1]*0.20)
        y = int(0.77*x)
        x_in = int(x*0.1)
        x_in_val = int(x*0.3)
        y_in1 = int(y*0.12)
        y_in2 = int(y_in1*2)
        y_in3 = int(y_in2*2.4)
        
        values_color =  (0,0,255) if val_found>70 else (0,165,255) if val_found>40 else (0,255,0)
        text_area = np.ones((y,x,3), dtype=np.int16)*255
        cv2.putText(img=text_area, text='MEAN VALUES DETECTED', org=(x_in, y_in1), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=x*0.002, color=(0, 0, 0),thickness=1)
        cv2.putText(img=text_area, text='FOR PC:', org=(x_in, y_in2), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=x*0.002, color=(0, 0, 0),thickness=1)
        cv2.putText(img=text_area, text=str(val_found), org=(x_in_val, y_in3), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=x*0.007, 
color=values_color,thickness=2)


        logo_new = cv.resize(logo, (int(text_area.shape[1]*0.6),int(text_area.shape[0]*0.26)),interpolation = cv2.INTER_AREA)

        x1 = text_area.shape[1]/2-logo_new.shape[1]/2
        x2 = text_area.shape[1]/2+logo_new.shape[1]/2
        y1 = text_area.shape[0]-logo_new.shape[0]
        y2 = text_area.shape[0]
        x1,x2,y1,y2= [int(i) for i in [x1,x2,y1,y2]]
        text_area[y1:y2,x1:x2]=logo_new


        yt = img_t.shape[0]-text_area.shape[0]
        y1t = img_t.shape[0]
        xt = img_t.shape[1]-text_area.shape[1]
        x1t = img_t.shape[1]
        img_t[yt:y1t,xt:x1t]=text_area
        return img_t