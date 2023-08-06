from .config import *
from .small_inference import Single_inference
def pick_img():
    root = tk.Tk()
    root.withdraw()

    file = filedialog.askopenfilenames()[0]
    return file
path = pick_img()
try:
    transform = bool(int(sys.argv[1]))
except IndexError:
    transform=False

if __name__ == '__main__':

    s = Single_inference(path,transform)
    s.activation()