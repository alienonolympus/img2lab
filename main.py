from tkinter import Tk, Label, Button, messagebox, filedialog, Checkbutton, BooleanVar, Frame
import numpy as np
from skimage import io
from skimage.color import rgb2lab, rgba2rgb
from os.path import abspath, join
from PIL import Image, ImageTk, ImageChops
from remove_bg import remove_bg

window = Tk()
window.title('CIELAB Values Calculator - img2lab')
window.attributes('-fullscreen', True)
window.configure(background='#ffffff')

screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
img_size = (int(screen_width / 3.5), int(screen_width / 3.5))

window.grid_rowconfigure(0, weight = 3)
window.grid_rowconfigure(1, weight = 2)
for row in range(2, 6):
    window.grid_rowconfigure(row, weight = 1)
window.grid_columnconfigure(0, weight = 2)
window.grid_columnconfigure(1, weight = 2)
window.grid_columnconfigure(2, weight = 1)

lbl_title = Label(window, text = '  Convert image to CIELAB values (L*, a* and b*)  ', background = '#ffffff', foreground = '#000000', font = ('Calibri', 36))
lbl_title.grid(row = 0, column = 0, columnspan = 3)

lbl_chosen = Label(window, text = 'Image chosen', background = '#ffffff', foreground = '#000000', font = ('Calibri', 18))
lbl_chosen.grid(row = 1, column = 0)
lbl_processed = Label(window, text = 'Processed image', background = '#ffffff', foreground = '#000000', font = ('Calibri', 18))
lbl_processed.grid(row = 1, column = 1)

def render_image(path = '', image = 0):
    image_to_render = Image.new('1', img_size)
    if path:
        image_to_render = Image.open(path)
    if image:
        image_to_render = image
    image_to_render = image_to_render.resize(img_size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image_to_render)

img_chosen = Label(window, image = render_image(path = 'placeholder.png'), background = '#ffffff')
img_chosen.grid(row = 2, column = 0, rowspan = 6)
img_processed = Label(window, image = render_image(path = 'placeholder.png'), background = '#ffffff')
img_processed.grid(row = 2, column = 1, rowspan = 6)

lbl_lab = Label(window, text = 'L* = 0\na* = 0\nb* = 0', background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
lbl_lab.grid(row = 4, column = 2)

remove_img_bg = BooleanVar()
remove_img_bg.set(False)
check_remove_bg = Checkbutton(window, text = 'Remove background?', var = remove_img_bg, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
check_remove_bg.grid(row = 2, column = 2)
check_remove_bg.toggle()

def choose_file():
    filename = filedialog.askopenfilename(initialdir = '~/Pictures')
    img = ''
    try:
        img = io.imread(filename)
    except:
        if filename:
            messagebox.showinfo('Error', filename + 'Image file invalid.')
        return
    try:
        img = rgba2rgb(img)
    except ValueError:
        pass
    chosen_img = render_image(path = filename)
    img_chosen.configure(image = chosen_img)
    img_chosen.image = chosen_img
    if remove_img_bg.get():
        masked = remove_bg(img)
        processed_img = render_image(image = Image.fromarray(masked))
        img_processed.configure(image = processed_img)
        img_processed.img = processed_img
        lab = rgb2lab(masked)
    else:
        lab = rgb2lab(img)
        img_processed.configure(image = chosen_img)
        img_processed.image = chosen_img
        '''
    lab_no_black = []
    for i in range(np.shape(lab)[0]):
        for j in range(np.shape(lab)[1]):
            if lab[i][j][0] != 0.0:
                print(lab[i][j])
                lab_no_black.append(lab[i][j])
                '''
    lab_array = lab.reshape(np.shape(lab)[0] * np.shape(lab)[1], np.shape(lab)[2])
    lab_no_black = [lab_value for lab_value in lab_array if lab_value[0] != 0.0]
    avg_lab = np.average(lab_no_black, axis=0)
    lbl_lab.configure(text = 'L* = ' + str(avg_lab[0]) + '\na* = ' + str(avg_lab[1]) + '\nb* = ' + str(avg_lab[2]))

btn_submit = Button(window, text = 'Choose File', command = choose_file, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
btn_submit.grid(row = 3, column = 2)

btn_exit = Button(window, text = 'Exit', command = window.destroy, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
btn_exit.grid(row = 5, column = 2)

window.mainloop()