from tkinter import Tk, Label, Button, messagebox, filedialog
from numpy import average
from skimage import io
from skimage.color import rgb2lab, rgba2rgb
from os.path import abspath, join

window = Tk()
window.title('LAB')
window.geometry('200x200')

lbl_l = Label(window, text = 'L* = 0')
lbl_l.grid(row = 1)
lbl_a = Label(window, text = 'a* = 0')
lbl_a.grid(row = 2)
lbl_b = Label(window, text = 'b* = 0')
lbl_b.grid(row = 3)

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
        lab = rgb2lab(img)
    except ValueError:
        lab = rgb2lab(rgba2rgb(img))
    avg_lab = average(average(lab, axis=0), axis=0)
    lbl_l.configure(text = 'L* = ' + str(avg_lab[0]))
    lbl_a.configure(text = 'a* = ' + str(avg_lab[1]))
    lbl_b.configure(text = 'b* = ' + str(avg_lab[2]))

btn_submit = Button(window, text = 'Choose File', command = choose_file)
btn_submit.grid(row = 0)

window.mainloop()