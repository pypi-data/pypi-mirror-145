from .config import *
from .model_activation import Model_activation
from .utils import Utils
import cv2 as cv
import cv2


class Single_inference(Model_activation,Utils):

    def __init__(self,path,transform):#,trans = False
        
        Model_activation.__init__(self)
        
        self.img=cv2.imread(path)
        self.mean=torch.tensor([0.3764, 0.5077, 0.2877])
        self.std = torch.tensor([0.0907, 0.0943, 0.1042])
        self.trans = transform

    def activation(self,RGB=True):
        
        transform_func = self.image_common_transforms() if self.trans else self.image_preprocess_transforms()

        img_instance = self.img.copy() if RGB else cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img_pil = transforms.functional.to_pil_image(img_instance)
        
        imgTransform = transform_func(img_pil)
        img_pil = transforms.functional.to_pil_image(imgTransform)

        image_data = np.asarray(img_pil)
        image_data= cv.resize(image_data,(image_data.shape[1]*4,image_data.shape[0]*4))
        inputs = torch.stack([imgTransform])
        preds = self.prediction(self.model, 'cpu', batch_input=inputs)
        cls_val = self.repalce_dict(preds[0])
        image_data = self.logo(image_data,cls_val)
        self.dis_im(image_data,f'Predicted area image --- cls: {preds[0]},values: {cls_val}, probability: {preds[1]}')
        image_data_full = self.logo(self.img,cls_val)
        self.dis_im(image_data_full,f'Predicted area image --- cls: {preds[0]},values: {cls_val}, probability: {preds[1]}')
#         self.dis_im(self.img,f'Full area image --- cls: {preds[0]},values: {cls_val}, probability: {preds[1]}')
        cv2.imwrite('inference_image.jpg',image_data_full)
