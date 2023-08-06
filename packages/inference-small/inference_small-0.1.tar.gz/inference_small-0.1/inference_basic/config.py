from PIL import *
import sys
import torch
import torch.utils.data as data
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from PIL import Image
import os
import os.path
from torchvision import transforms
import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np
import cv2

# def pick_img():
#     root = tk.Tk()
#     root.withdraw()

#     file = filedialog.askopenfilenames()[0]
#     return file

# path = pick_img()