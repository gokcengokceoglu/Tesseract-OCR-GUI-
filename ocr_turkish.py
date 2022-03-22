from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from turtle import color
#
from PIL import Image
#
import pytesseract
import pdf2image
import glob, os, shutil
#pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.1.0/bin/tesseract'

def perform_ocr(src_file, dst_folder ,language):
    src_file_name = src_file.split("/")[-1]
    images = pdf2image.convert_from_path(src_file)
    if not os.path.exists(os.path.join(dst_folder, src_file_name.split('.pdf')[0])):
        try:
            os.makedirs(os.path.join(dst_folder, src_file_name.split('.pdf')[0]))
            dst_folder_final = os.path.join(dst_folder, src_file_name.split('.pdf')[0])
        except:
            dst_folder_final = dst_folder
    else:
        dst_folder_final = os.path.join(dst_folder, src_file_name.split('.pdf')[0])

    try:
        for image_idx in range(len(images)):
                    
            text_file_path = os.path.join(dst_folder_final, src_file_name.split('.pdf')[0] + "-page" + str(image_idx) + ".txt")
            text = pytesseract.image_to_string(images[image_idx], lang=language ,config = '--psm 1')
            text_file = open(text_file_path, "w+", encoding='utf-8')
            text_file.write(text)
            text_file.close()

        return (1, dst_folder_final)
    except:
        return (-1, dst_folder_final)

class MyWindow:

    def __init__(self, win):

        self.mywindow = win
        # self.lblget = Label(win, text='Load the file.')
        # self.lblget.place(x = 10, y=10)

        self.openedfilename = None
        self.dst_dir_msg = None
        self.ocr_end_msg = None
        self.ocr_end_msg_folder = None
        
        self.getlanguage = Label(win, text="Select the language")
        self.getlanguage.place(x=10, y=10)

        self.getfilename = Button(win, text="Select the file", command=self.open)
        self.getfilename.place(x=10, y=100)


        self.getdstpath = Button(win, text="Select destination folder", command=self.get_folder_name)
        self.getdstpath.place(x=10, y=160)

        self.performocrbutton = Button(win, text="Perform OCR", command=self.ocr_with_tesseract)
        self.performocrbutton.place(x=10, y=220)

        self.Checkbutton1 = IntVar()  
        self.Checkbutton2 = IntVar()  
        
        self.Button1 = Checkbutton(self.mywindow, text = "Turkish", 
                            variable = self.Checkbutton1,
                            onvalue = 1,
                            offvalue = 0,
                            height = 2,
                            width = 10)
        
        self.Button2 = Checkbutton(self.mywindow, text = "English",
                            variable = self.Checkbutton2,
                            onvalue = 1,
                            offvalue = 0,
                            height = 2,
                            width = 10)

        self.Button1.place(x=10, y=40)

        self.Button2.place(x=110, y=40)

    #def get_language(self):

    def open(self):
        if self.openedfilename != None:
            self.openedfilename.destroy()

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
        self.openedfilename.place(x=10, y=130)


    def get_folder_name(self):
        if self.dst_dir_msg != None:
            self.dst_dir_msg.destroy()
        self.dst_dir = fd.askdirectory()
        self.dst_dir_msg = Label(self.mywindow, text= str(self.dst_dir))
        self.dst_dir_msg.place(x=10, y=190)

    def ocr_with_tesseract(self):
        # if self.ocr_end_msg != None:
        #     self.ocr_end_msg.after(10, self.ocr_end_msg.destroy())
        if self.ocr_end_msg_folder != None:
            self.ocr_end_msg_folder.destroy()

        finished_flag = None

        if (self.Checkbutton1.get()== 0) and (self.Checkbutton2.get() ==0):
            showinfo(
                title='Error',
                message='Please select the source language.')
        elif (self.Checkbutton1.get()== 1) and (self.Checkbutton2.get() ==1):
            showinfo(
                title='Error',
                message='Please select only one language.')

        elif self.Checkbutton1.get() == 1:
            finished_flag, dst = perform_ocr(self.filename, self.dst_dir ,'tur')

        else:
            finished_flag, dst = perform_ocr(self.filename, self.dst_dir, 'eng')

        if finished_flag == 1:
            # self.ocr_end_msg = Label(self.mywindow, text= str("OCR is finished"))
            # self.ocr_end_msg.place(x=10, y=250)
            self.ocr_end_msg_folder = Label(self.mywindow, text= str("OCR output is written to " + dst))
            self.ocr_end_msg_folder.place(x=10, y=250)

        # else:
        #     self.ocr_end_msg = Label(self.mywindow, text= str("An error occured during OCR."))
        #     self.ocr_end_msg.place(x=10, y=250)

window=Tk()
mywin=MyWindow(window)
window.title('OCR tool')
window.geometry("500x500+10+10")
window.mainloop()
