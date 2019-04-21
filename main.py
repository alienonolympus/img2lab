from tkinter import Tk, Label, Button, messagebox, filedialog, Checkbutton, BooleanVar, Frame, Entry, StringVar
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
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d" % (screen_width * 0.8, screen_height * 0.8))
window.configure(background='#ffffff')
window.update()
img_size = (int(window.winfo_width() / 3.5), int(window.winfo_height() / 3.5))


# Configuring grid
print('Configuring tkinter grids...')
window.grid_rowconfigure(0, weight = 3)
window.grid_rowconfigure(1, weight = 2)
for row in range(2, 9):
    window.grid_rowconfigure(row, weight = 1)
window.grid_columnconfigure(0, weight = 3)
window.grid_columnconfigure(1, weight = 3)
window.grid_columnconfigure(2, weight = 2)

# Labels
print('Creating labels...')
lbl_title = Label(window, text = '  Convert image to CIELAB values (L*, a* and b*)  ', background = '#ffffff', foreground = '#000000', font = ('Calibri', 36))
lbl_title.grid(row = 0, column = 0, columnspan = 3)

lbl_chosen = Label(window, text = 'Image chosen', background = '#ffffff', foreground = '#000000', font = ('Calibri', 18))
lbl_chosen.grid(row = 1, column = 0)
lbl_processed = Label(window, text = 'Processed image', background = '#ffffff', foreground = '#000000', font = ('Calibri', 18))
lbl_processed.grid(row = 1, column = 1)

lbl_status = Label(window, text = 'Status:', background = '#ffffff', foreground = '#000000', font = ('Calibri', 11))
lbl_status.grid(row = 1, column = 2)

def update_status(msg):
    print(msg)
    lbl_status.configure(text = 'Status:\n' + msg)
    window.update()

update_status('Ready.')

# Setting up images
print('Setting up images...')
img_chosen = Label(window, image = render_image(path = 'placeholder.png'), background = '#ffffff')
img_chosen.grid(row = 2, column = 0, rowspan = 6)
img_processed = Label(window, image = render_image(path = 'placeholder.png'), background = '#ffffff')
img_processed.grid(row = 2, column = 1, rowspan = 6)

# LAB labels
print('Creating LAB labels...')
string_l = StringVar()
string_a = StringVar()
string_b = StringVar()
string_browning = StringVar()
entry_l = Entry(window, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12), textvariable = string_l)
entry_l.grid(row = 4, column = 2)
entry_a = Entry(window, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12), textvariable = string_a)
entry_a.grid(row = 5, column = 2)
entry_b = Entry(window, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12), textvariable = string_b)
entry_b.grid(row = 6, column = 2)
entry_browning = Entry(window, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12), textvariable = string_browning)
entry_browning.grid(row = 7, column = 2)

def set_lab_values(lab):
    string_l.set('L* = ' + str(lab[0]))
    string_a.set('a* = ' + str(lab[1]))
    string_b.set('b* = ' + str(lab[2]))
    try:
        x = (lab[1] + 1.75 * lab[0]) / (5.645 * lab[0] + lab[1] - 0.3012 * lab[2])
        browning = (100 * (x - 0.31)) / 0.17
    except ZeroDivisionError:
        browning = 0
    string_browning.set('Browning Index = ' + str(browning))
    window.update()

set_lab_values([0.0, 0.0, 0.0])

# Creating buttons
print('Creating buttons...')
remove_img_bg = BooleanVar()
remove_img_bg.set(False)
check_remove_bg = Checkbutton(window, text = 'Remove background?', var = remove_img_bg, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
check_remove_bg.grid(row = 2, column = 2)
check_remove_bg.toggle()

def choose_file():
    # Asking for filename
    update_status('Asking for filename...')
    window.update()
    filename = filedialog.askopenfilename(initialdir = '~/Pictures')
    img = ''
    
    # Reading image
    update_status('Reading file...')
    try:
        img = io.imread(filename)
    except:
        if filename:
            messagebox.showinfo('Error', filename + 'Image file invalid.')
        update_status('Ready.')
        return
    try:
        img = rgba2rgb(img)
    except ValueError:
        pass
    
    # Rendering image
    update_status('Rendering image...')
    chosen_img = render_image(path = filename)
    img_chosen.configure(image = chosen_img)
    img_chosen.image = chosen_img
    window.update()

    if remove_img_bg.get():
        # Removing background
        update_status('Removing background...')
        masked = remove_bg(img)

        # Rendering image with removed background
        update_status('Rendering image...')
        processed_img = render_image(image = Image.fromarray(masked))
        img_processed.configure(image = processed_img)
        img_processed.img = processed_img
        window.update()

        # Converting to LAB
        update_status('Converting RGB to LAB...')
        lab = rgb2lab(masked)
    else:
        # Converting to LAB
        update_status('Converting RGB to LAB...')
        lab = rgb2lab(img)
        img_processed.configure(image = chosen_img)
        img_processed.image = chosen_img

    # Ignoring black pixels
    update_status('Ignoring mask pixels...')
    lab_array = lab.reshape(np.shape(lab)[0] * np.shape(lab)[1], np.shape(lab)[2])
    lab_no_black = [lab_value for lab_value in lab_array if lab_value[0] != 0.0]

    # Calculating values
    update_status('Calculating values...')
    avg_lab = np.average(lab_no_black, axis=0)

    # Displaying values
    update_status('Displaying values...')
    set_lab_values(avg_lab)
    window.update()

    update_status('Ready.')
    print()

btn_submit = Button(window, text = 'Choose File', command = choose_file, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
btn_submit.grid(row = 3, column = 2)

def exit_img2lab():
    update_status('Exiting img2lab...')
    window.destroy()

btn_exit = Button(window, text = 'Exit', command = exit_img2lab, background = '#ffffff', foreground = '#000000', font = ('Calibri', 12))
btn_exit.grid(row = 8, column = 2)

# Starting tkinter
print('Starting tkinter...')
window.mainloop()