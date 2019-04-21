from tkinter import Tk, Label, Button, messagebox, filedialog, Checkbutton, BooleanVar, Frame, Entry, StringVar
import numpy as np
from skimage import io
from skimage.color import rgb2lab, rgba2rgb
from os.path import abspath, join
from PIL import Image, ImageTk, ImageChops
from math import atan
from remove_bg import remove_bg

def validate():
    return False

# Create window
print('Creating tkinter window...')
window = Tk()
window.title('CIELAB Values Calculator - img2lab')
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d" % (screen_width * 0.8, screen_height * 0.8))
window.configure(background='#ffffff')
window.update()
img_size = (int(window.winfo_width() / 3), int(window.winfo_height() / 2.5))
window.minsize(int(window.winfo_width() / 1.3), int(window.winfo_height() / 1.3))

def render_image(path = '', image = 0):
    image_to_render = Image.new('1', img_size)
    if path:
        image_to_render = Image.open(path)
    if image:
        image_to_render = image
    image_to_render = image_to_render.resize(img_size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image_to_render)

# Configuring frames
print('Configuring frames...')
frame_title = Frame(window, background = '#ffffff', borderwidth =  1, relief = 'flat')
frame_title.pack(side = 'top', fill = 'x', anchor = 'n')

frame_bottom = Frame(window, background = '#ffffff', borderwidth = 1, relief = 'flat')
frame_bottom.pack(side = 'bottom', fill = 'x', anchor = 's')

frame_images = Frame(window, background = '#ffffff', borderwidth = 2, relief = 'groove')
frame_images.pack(side = 'left', fill = 'both', expand = 1)
frame_images.grid_rowconfigure(0, weight = 1)
frame_images.grid_rowconfigure(1, weight = 0)
frame_images.grid_rowconfigure(2, weight = 2)
frame_images.grid_columnconfigure(0, weight = 1)
frame_images.grid_columnconfigure(1, weight = 1)

frame_right = Frame(window, background = '#ffffff', borderwidth = 2, relief = 'groove')
frame_right.pack(side = 'right', fill = 'both', expand = 1)
frame_status = Frame(frame_right, background = '#ffffff')
frame_status.pack(side = 'top', fill = 'both', expand = 1, anchor = 'nw')
frame_settings = Frame(frame_right, background = '#ffffff')
frame_settings.pack(side = 'top', fill = 'both', expand = 1, anchor = 'center')
frame_values = Frame(frame_right, background = '#ffffff')
frame_values.pack(side = 'top', fill = 'both', expand = 1, anchor = 'center')



# Labels
print('Creating labels...')
lbl_title_top_margin = Label(frame_title, text = ' ', background = '#ffffff', foreground = '#000000', font = ('Arial', 12))
lbl_title_top_margin.pack(anchor = 'center')
lbl_title = Label(frame_title, text = '  Convert image to CIELAB values (L*, a* and b*)  ', background = '#ffffff', foreground = '#000000', font = ('Arial', 24))
lbl_title.pack(anchor = 'center')
lbl_title_bottom_margin = Label(frame_title, text = ' ', background = '#ffffff', foreground = '#000000', font = ('Arial', 12))
lbl_title_bottom_margin.pack(anchor = 'center')

lbl_spacing = Label(frame_images, text = '   ', background = '#ffffff', foreground = '#000000', font = ('Arial', 18))
lbl_chosen = Label(frame_images, text = 'Image chosen', background = '#ffffff', foreground = '#000000', font = ('Arial', 18))
lbl_chosen.grid(row = 1, column = 0)
lbl_processed = Label(frame_images, text = 'Processed image', background = '#ffffff', foreground = '#000000', font = ('Arial', 18))
lbl_processed.grid(row = 1, column = 1)

lbl_status = Label(frame_status, text = 'Status: ', background = '#ffffff', foreground = '#000000', font = ('Arial', 11))
lbl_status.grid(row = 0, column = 0)

def update_status(msg):
    print(msg)
    lbl_status.configure(text = 'Status: ' + msg)
    window.update()

update_status('Ready.')

# Setting up images
print('Setting up images...')
img_chosen = Label(frame_images, image = render_image(path = 'placeholder.png'), background = '#fafafa', borderwidth = 2, relief = 'groove')
img_chosen.grid(row = 2, column = 0)
img_processed = Label(frame_images, image = render_image(path = 'placeholder.png'), background = '#fafafa', borderwidth = 2, relief = 'groove')
img_processed.grid(row = 2, column = 1)

# LAB labels
print('Creating LAB labels...')
string_l = StringVar()
string_a = StringVar()
string_b = StringVar()
string_browning = StringVar()
string_hue = StringVar()
entry_l = Entry(frame_values, background = '#ffffff', foreground = '#000000', font = ('Arial', 11), textvariable = string_l, validatecommand = validate)
entry_l.pack(side = 'top', anchor = 'center')
entry_a = Entry(frame_values, background = '#ffffff', foreground = '#000000', font = ('Arial', 11), textvariable = string_a, validatecommand = validate)
entry_a.pack(side = 'top', anchor = 'center')
entry_b = Entry(frame_values, background = '#ffffff', foreground = '#000000', font = ('Arial', 11), textvariable = string_b, validatecommand = validate)
entry_b.pack(side = 'top', anchor = 'center')
entry_browning = Entry(frame_values, background = '#ffffff', foreground = '#000000', font = ('Arial', 11), textvariable = string_browning, validatecommand = validate)
entry_browning.pack(side = 'top', anchor = 'center')
entry_hue = Entry(frame_values, background = '#ffffff', foreground = '#000000', font = ('Arial', 11), textvariable = string_hue, validatecommand = validate)
entry_hue.pack(side = 'top', anchor = 'center')

def set_lab_values(lab):
    string_l.set('L* = ' + str(lab[0]))
    string_a.set('a* = ' + str(lab[1]))
    string_b.set('b* = ' + str(lab[2]))
    try:
        x = (lab[1] + 1.75 * lab[0]) / (5.645 * lab[0] + lab[1] - 0.3012 * lab[2])
        browning = (100 * (x - 0.31)) / 0.17
        hue = atan(lab[2] - lab[1])
    except ZeroDivisionError:
        browning = 0
        hue = 0
    string_browning.set('Browning Index = ' + str(browning))
    string_hue.set('Hue Angle = ' + str(hue))
    entry_l.configure(validate = 'key')
    entry_a.configure(validate = 'key')
    entry_b.configure(validate = 'key')
    entry_browning.configure(validate = 'key')
    entry_hue.configure(validate = 'key')
    window.update()

set_lab_values([0.0, 0.0, 0.0])

# Creating buttons
print('Creating buttons...')
remove_img_bg = BooleanVar()
remove_img_bg.set(False)
check_remove_bg = Checkbutton(frame_settings, text = 'Remove background?', var = remove_img_bg, background = '#ffffff', foreground = '#000000', font = ('Arial', 12))
check_remove_bg.pack(side = 'top', anchor = 'center')
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

btn_submit = Button(frame_settings, text = 'Choose File', command = choose_file, background = '#fafafa', foreground = '#000000', font = ('Arial', 12))
btn_submit.pack(side = 'top', anchor = 'n')

def exit_img2lab():
    update_status('Exiting img2lab...')
    window.destroy()

lbl_exit_top_margin = Label(frame_bottom, text = ' ', background = '#ffffff', foreground = '#000000', font = ('Arial', 3))
lbl_exit_top_margin.pack(anchor = 'center')
btn_exit = Button(frame_bottom, text = '  Exit  ', command = exit_img2lab, background = '#fafafa', foreground = '#000000', font = ('Arial', 12))
btn_exit.pack(anchor = 'center')
lbl_exit_bottom_margin = Label(frame_bottom, text = ' ', background = '#ffffff', foreground = '#000000', font = ('Arial', 3))
lbl_exit_bottom_margin.pack(anchor = 'center')


# Starting tkinter
print('Starting tkinter...')
window.mainloop()