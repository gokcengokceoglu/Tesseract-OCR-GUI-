from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from PIL import Image

import pytesseract
import pdf2image
import glob, os, shutil

def perform_ocr(src_file, dst_folder ,language):
    src_file_name = src_file.split("/")[-1]
    images = pdf2image.convert_from_path(src_file)
    #pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.1.0/bin/tesseract'

    for image_idx in range(len(images)):
        text_file_path = os.path.join(dst_folder, src_file_name + "-page" + str(image_idx) + ".txt")
        text = pytesseract.image_to_string(images[image_idx], lang=language ,config='--psm 1')
        text_file = open(text_file_path, "w+")
        text_file.write(text)
        text_file.close()

class MyWindow:

    def __init__(self, win):

        self.mywindow = win
        # self.lblget = Label(win, text='Load the file.')
        # self.lblget.place(x = 10, y=10)

        self.getfilename = Button(win, text="Select the file", command=self.open)
        self.getfilename.place(x=10, y=10)

        self.getdstpath = Button(win, text="Select destination folder", command=self.get_folder_name)
        self.getdstpath.place(x=10, y=90)

        self.performocrbutton = Button(win, text="Perform OCR", command=self.ocr_with_tesseract)
        self.performocrbutton.place(x=10, y=170)

    def open(self):

        self.filetypes = (('PDF files', '*.pdf'),
                            ('All files', '*.*'))

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=self.filetypes)

        showinfo(
            title='Selected Files',
            message=self.filename)

        self.openedfilename = Label(self.mywindow, text= str(self.filename))
        self.openedfilename.place(x=10, y=50)

    def get_folder_name(self):
        self.dst_dir = fd.askdirectory()
        self.dst_dir_msg = Label(self.mywindow, text= str(self.dst_dir))
        self.dst_dir_msg.place(x=10, y=130)

    def ocr_with_tesseract(self):
        perform_ocr(self.filename, self.dst_dir ,'ara+fas')
        self.ocr_end_msg = Label(self.mywindow, text= str("OCR is finished"))
        self.ocr_end_msg.place(x=10, y=210)


window=Tk()
mywin=MyWindow(window)
window.title('OCR tool')
window.geometry("500x500+10+10")
window.mainloop()
