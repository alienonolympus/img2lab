from tkinter import Tk, Label, Button, messagebox, filedialog, Checkbutton, BooleanVar, Frame
import numpy as np
from skimage import io
from skimage.color import rgb2lab, rgba2rgb
from os.path import abspath, join
from PIL import Image, ImageTk, ImageChops

def render_image(path = '', image = 0):
    image_to_render = Image.new('1', img_size)
    if path:
        image_to_render = Image.open(path)
    if image:
        image_to_render = image
    image_to_render = image_to_render.resize(img_size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image_to_render)
from remove_bg import remove_bg

# Create window
print('Creating tkinter window...')
window = Tk()
window.title('CIELAB Values Calculator - img2lab')
window.attributes('-fullscreen', True)
window.configure(background='#ffffff')

screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
img_size = (int(screen_width / 3.5), int(screen_width / 3.5))

# Configuring grid
print('Configuring tkinter grids...')
window.grid_rowconfigure(0, weight = 3)
window.grid_rowconfigure(1, weight = 2)
for row in range(2, 6):
    window.grid_rowconfigure(row, weight = 1)
window.grid_columnconfigure(0, weight = 2)
window.grid_columnconfigure(1, weight = 2)
window.grid_columnconfigure(2, weight = 1)

# Labels
print('Creating labels...')
lbl_title = Label(window, text = '  Convert image to CIELAB values (L*, a* and b*)  ', background = '#ffffff', foreground = '#000000', font = ('Calibri', 36))
lbl_title.grid(row = 0, column = 0, columnspan = 3)

lbl_chosen = Label(window, text = 'Image chosen', background = '#ffffff', foreground = '#000000', font = ('Calibri', 18))
lbl_chosen.grid(row = 1, column = 0)
lbl_processed = Label(window, text = 'Processed image', background = '#ffffff', foreground = '#000000', font = ('Calibri', 18))
lbl_processed.grid(row = 1, column = 1)

# Setting up images
print('Setting up images...')
img_chosen = Label(window, image = render_image(path = 'placeholder.png'), background = '#ffffff')
img_chosen.grid(row = 2, column = 0, rowspan = 6)
img_processed = Label(window, image = render_image(path = 'placeholder.png'), background = '#ffffff')
img_processed.grid(row = 2, column = 1, rowspan = 6)

# LAB labels
print('Creating LAB labels...')
lbl_lab = Label(window, text = 'L* = 0\na* = 0\nb* = 0', background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
lbl_lab.grid(row = 4, column = 2)

# Creating buttons
print('Creating buttons...')
remove_img_bg = BooleanVar()
remove_img_bg.set(False)
check_remove_bg = Checkbutton(window, text = 'Remove background?', var = remove_img_bg, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
check_remove_bg.grid(row = 2, column = 2)
check_remove_bg.toggle()

def choose_file():
    # Asking for filename
    print('Asking for filename')
    filename = filedialog.askopenfilename(initialdir = '~/Pictures')
    img = ''
    
    # Reading image
    print('Reading file...')
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
    
    # Rendering image
    print('Rendering image...')
    chosen_img = render_image(path = filename)
    img_chosen.configure(image = chosen_img)
    img_chosen.image = chosen_img

    if remove_img_bg.get():
        # Removing background
        print('Removing background...')
        masked = remove_bg(img)

        # Rendering image with removed background
        print('Rendering image without background...')
        processed_img = render_image(image = Image.fromarray(masked))
        img_processed.configure(image = processed_img)
        img_processed.img = processed_img

        # Converting to LAB
        print('Converting RGB values to LAB values...')
        lab = rgb2lab(masked)
    else:
        # Converting to LAB
        print('Converting RGB values to LAB values...')
        lab = rgb2lab(img)
        img_processed.configure(image = chosen_img)
        img_processed.image = chosen_img

    # Ignoring black pixels
    print('Ignoring mask pixels...')
    lab_array = lab.reshape(np.shape(lab)[0] * np.shape(lab)[1], np.shape(lab)[2])
    lab_no_black = [lab_value for lab_value in lab_array if lab_value[0] != 0.0]

    # Calculating values
    print('Calculating values...')
    avg_lab = np.average(lab_no_black, axis=0)

    # Displaying values
    print('Displaying values...')
    lbl_lab.configure(text = 'L* = ' + str(avg_lab[0]) + '\na* = ' + str(avg_lab[1]) + '\nb* = ' + str(avg_lab[2]))

    print('Done.\n')

btn_submit = Button(window, text = 'Choose File', command = choose_file, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
btn_submit.grid(row = 3, column = 2)

def exit_img2lab():
    print('Exiting img2lab...')
    window.destroy()

btn_exit = Button(window, text = 'Exit', command = exit_img2lab, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
btn_exit.grid(row = 5, column = 2)

# Starting tkinter
print('Starting tkinter...')
window.mainloop()