from tkinter import Tk, Label, Button, messagebox, filedialog, Checkbutton, BooleanVar
from numpy import average
from skimage import io
from skimage.color import rgb2lab, rgba2rgb
from os.path import abspath, join
from remove_bg import remove_bg

window = Tk()
window.title('LAB')
window.geometry('200x200')


lbl_l = Label(window, text = 'L* = 0')
lbl_l.grid(row = 2)
lbl_a = Label(window, text = 'a* = 0')
lbl_a.grid(row = 3)
lbl_b = Label(window, text = 'b* = 0')
lbl_b.grid(row = 4)

remove_img_bg = BooleanVar()
remove_img_bg.set(False)
check_remove_bg = Checkbutton(window, text = 'Remove background?', var = remove_img_bg)
check_remove_bg.grid(row = 0)

def choose_file():
    filename = filedialog.askopenfilename(initialdir = '~')
    img = ''
    try:
        img = io.imread(join(abspath(''), filename))
    except:
        if filename:
            messagebox.showinfo('Error', filename + 'Image file invalid.')
        return
    try:
        img = rgba2rgb(img)
    except ValueError:
        pass
    if remove_img_bg.get():
        removed_bg = remove_bg(img)
        lab = rgb2lab(removed_bg)
    else:
        lab = rgb2lab(img)
    avg_lab = average(average(lab, axis=0), axis=0)
    lbl_l.configure(text = 'L* = ' + str(avg_lab[0]))
    lbl_a.configure(text = 'a* = ' + str(avg_lab[1]))
    lbl_b.configure(text = 'b* = ' + str(avg_lab[2]))

btn_submit = Button(window, text = 'Choose File', command = choose_file)
btn_submit.grid(row = 1)

window.mainloop()