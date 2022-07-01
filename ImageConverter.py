#!/bin/env python

import os

# import schedule
# import tkinter GUI lib
from tkinter import *

# from tkinter import ttk
from tkinter import filedialog

# import Pillow(PIL) image lib
from PIL import Image

# from PIL import ImageFilter
from PIL import ImageEnhance

# import time
import threading

# kreiram klasu u kojoj cu dobiti okvir glavnog prozora
class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.button_clicks = 0  # relativno besmisleno
        self.create_widget()  # dodavanje elemenata

    def create_widget(self):
        # prvi widget - samo text
        self.instruction = Label(self)
        self.instruction["text"] = "Select an image to convert:"
        self.instruction.grid(row=0, column=0, sticky=W, columnspan=3)

        # za prikazivanje imena datoteka
        self.imgName = Entry(self)
        self.imgName.config(state="readonly")
        self.imgName.grid(
            row=1, column=0, sticky=W, columnspan=2
        )  # nikako ne funkcionira columnspan

        # za otvaranje skocnog prozora koji otvara odabir datoteka
        self.browseIMG = Button(self)
        self.browseIMG["text"] = "Browse"
        self.browseIMG["command"] = self.selectedIMGs
        self.browseIMG.grid(row=1, column=2)

        # prazni row radi preglednosti
        self.blankspace1 = Label(self)
        self.blankspace1["text"] = " "
        self.blankspace1.grid(row=2, column=0, sticky=W)

        # odabir kvalitete od 1 do 100, default je 80
        self.qualbl = Label(self)
        self.qualbl["text"] = "Image quality (1-100): "
        self.qualbl.grid(row=3, column=0, sticky=W)
        self.imgQuality = Entry(self)
        self.imgQuality.config(width=3)
        self.imgQuality.insert(0, "80")
        self.imgQuality.grid(row=3, column=1, sticky=W)

        # odabir svjetline od 1 do 10, default je 5
        self.brightnesslbl = Label(self)
        self.brightnesslbl["text"] = "Brightness (1-10): "
        self.brightnesslbl.grid(row=4, column=0, sticky=W)
        self.brightlvl = Entry(self)
        self.brightlvl.config(width=3)
        self.brightlvl.insert(0, "5")
        self.brightlvl.grid(row=4, column=1, sticky=W)

        # odabir kontrasta od 1 do 10, default je 5
        self.contrastlbl = Label(self)
        self.contrastlbl["text"] = "Contrast (1-10): "
        self.contrastlbl.grid(row=5, column=0, sticky=W)
        self.contrastlvl = Entry(self)
        self.contrastlvl.config(width=3)
        self.contrastlvl.insert(0, "5")
        self.contrastlvl.grid(row=5, column=1, sticky=W)

        # odabir ostrine od 1 do 10, default je 5
        self.sharpnesslbl = Label(self)
        self.sharpnesslbl["text"] = "Sharpness (1-10): "
        self.sharpnesslbl.grid(row=4, column=2, sticky=W)
        self.sharpnesslvl = Entry(self)
        self.sharpnesslvl.config(width=3)
        self.sharpnesslvl.insert(0, "5")
        self.sharpnesslvl.grid(row=4, column=3, sticky=W)

        # odabir balansa boje od 1 do 10, default je 5
        self.colourlbl = Label(self)
        self.colourlbl["text"] = "Colour (1-10): "
        self.colourlbl.grid(row=5, column=2, sticky=W)
        self.colourlvl = Entry(self)
        self.colourlvl.config(width=3)
        self.colourlvl.insert(0, "5")
        self.colourlvl.grid(row=5, column=3, sticky=W)

        # prazni row radi preglednosti nr2
        self.blankspace2 = Label(self)
        self.blankspace2["text"] = " "
        self.blankspace2.grid(row=6, column=0, sticky=W)

        # glavni info box koji prikazuje stanje procesa u samom programu
        self.text = Label(self)
        self.text["text"] = "Information box: "
        self.text.grid(row=7, column=0, sticky=W)
        self.text = Text(self, width=40, height=5, wrap=WORD)
        self.text.grid(row=8, column=0, columnspan=3, sticky=W)

        # prikaz patha foldera za spremanje slika
        self.destination = Entry(self)
        self.destination.insert(0, os.getcwd() + " ")
        self.destination.grid(
            row=9, column=0, columnspan=8, sticky=W
        )  # i ovdje nikako ne funkcionira columnspan

        # za otvaranje skocnog prozorcica kojim odredujemo folder u kojem se spremaju slike
        self.saveIn = Button(self, text="Path")
        self.saveIn["command"] = self.savePath
        self.saveIn.grid(row=9, column=2, sticky=W)

        # za otvaranje skocnog prozorcica kojim vidimo kako ce izgledati slika koju pretvaramo
        self.preview_button = Button(self)
        self.preview_button["text"] = "Preview"
        self.preview_button["command"] = self.previewIMG
        self.preview_button.grid(row=9, column=3)

        # ovim gumbom pretvaramo zadane slike u .jpg format
        self.submit_jpg_button = Button(self)
        self.submit_jpg_button["text"] = "Convert to JPG"
        self.submit_jpg_button["command"] = self.convertJPG
        self.submit_jpg_button.grid(row=11, column=3, sticky=W)

        # ovim gumbom pretvaramo zadane slike u .png format
        self.submit_png_button = Button(self)
        self.submit_png_button["text"] = "Convert to PNG"
        self.submit_png_button["command"] = self.convertPNG
        self.submit_png_button.grid(row=11, column=2, sticky=W)

        # ovim gumbom pretvaramo zadane slike u .bmp format
        self.submit_bmp_button = Button(self)
        self.submit_bmp_button["text"] = "Convert to BMP"
        self.submit_bmp_button["command"] = self.convertBMP
        self.submit_bmp_button.grid(row=12, column=3, sticky=W)

        # ovim gumbom pretvaramo zadane slike u .gif format
        self.submit_gif_button = Button(self)
        self.submit_gif_button["text"] = "Convert to GIF"
        self.submit_gif_button["command"] = self.convertGIF
        self.submit_gif_button.grid(row=12, column=2, sticky=W)

        # ovim gumbom pretvaramo zadane slike u .webp format
        self.submit_webp_button = Button(self)
        self.submit_webp_button["text"] = "Convert to WebP"
        self.submit_webp_button["command"] = self.convertWEBP
        self.submit_webp_button.grid(row=12, column=1, sticky=W)

        # prazni row radi preglednosti nr3
        self.blankspace3 = Label(self)
        self.blankspace3["text"] = " "
        self.blankspace3.grid(row=10, column=0, sticky=W)

        # checkbox da pretvorimo sliku u crnobijelu
        self.greyscale = BooleanVar()
        Checkbutton(self, text="To grayscale", variable=self.greyscale).grid(
            row=3, column=2, sticky=W
        )

    # def retentionPeriod(i):
        # os.remove(i)

        # time.sleep(10)
        # os.remove(i)

    # def threadingTimer():
    #    t = threading.Timer(30.0, retentionPeriod(i))
    #    t.start()

    def selectedIMGs(self):  # funkcija kojom odredujemo sliku/slike - array
        self.imgName.configure(state="normal")
        self.imgName.delete(0, END)
        self.text.delete(0.0, END)
        path = filedialog.askopenfilenames(
            filetypes=[
                ("All files", "*.*"),
                ("JPEG", "*.jpg;*.jpeg"),
                ("PNG", "*.png"),
                ("WebP", "*.webp"),
                ("BMP", ".bmp"),
                ("GIF", ".gif"),
            ]
        )

        self.selectedIMGs = {}

        for (
            img
        ) in path:  # formatiramo opis slike da nam pase i prikazujemo je u prvom boxu
            oriSize = os.path.getsize(img)
            self.selectedIMGs[img] = oriSize
            fileName = os.path.basename(img)
            # print(fileName)
            self.imgName.configure(state="normal")
            self.imgName.insert(END, fileName + ";")
            self.imgName.configure(state="readonly")
            self.text.insert(
                END, fileName + ":" + str(round(oriSize / 1000 / 1000, 3)) + "MB\n"
            )

        return self.selectedIMGs

    def savePath(self):  # odredi direktorij u kojem se sprema slika
        self.destination.delete(0, END)
        savePath = filedialog.askdirectory(initialdir=os.getcwd())
        self.destination.insert(0, savePath)

    def adjustment(
        self, imgDict
    ):  # unutra dodajemo adjustmente, tj. sve sto smo odredili i pripremamo ime slike za spremanje van programa
        self.preConvertIMGs = {}
        for path, size in imgDict.items():

            image = Image.open(path)  # odabir prave slike po pathu
            if (
                image.mode != "RGBA" or image.mode != "RGB"
            ):  # mali safety flag posto bolje funkcionira za sve formate
                image = image.convert("RGB")
            fileName = os.path.basename(path)
            imgname = fileName.split(".")
            saveAs = imgname[0]

            # ovdje formiramo prethodno definirane varijable
            bright = int(self.brightlvl.get()) / 4.0
            contra = int(self.contrastlvl.get()) / 4.0
            sharp = int(self.sharpnesslvl.get()) / 4.0
            colour = int(self.colourlvl.get()) / 4.0

            # ovdje prilagodujemo sliku
            brightEnhancer = ImageEnhance.Brightness(image)
            image = brightEnhancer.enhance(bright)

            contraEnhancer = ImageEnhance.Contrast(image)
            image = contraEnhancer.enhance(contra)

            sharpEnhancer = ImageEnhance.Sharpness(image)
            image = sharpEnhancer.enhance(sharp)

            colourEnhancer = ImageEnhance.Color(image)
            image = colourEnhancer.enhance(colour)

            if self.greyscale.get():
                image = image.convert("L")

            self.preConvertIMGs[
                saveAs
            ] = image  # key: ime datoteke pod kojim ce se spremiti
            # value: stvarni objekt slike kojeg smo prilagodili
        return self.preConvertIMGs

    def previewIMG(self):  # prikazuje sve prilagodene slike
        self.adjustment(self.selectedIMGs)
        for image in self.preConvertIMGs.values():
            image.show()

    def convertJPG(self):  # funkcija pretvaranja u .jpg
        os.chdir(self.destination.get())
        self.text.delete(0.0, END)  # radi čišćenja info boxa
        self.adjustment(
            self.selectedIMGs
        )  # ono prethodno korigiranje slike sada iskorištavam
        oriSize = list(self.selectedIMGs.values())
        i = 0
        qualvl = int(self.imgQuality.get())
        for saveAs, image in self.preConvertIMGs.items():
            saveAsJPG = saveAs + ".jpg"
            image.save(saveAsJPG, "JPEG", quality=qualvl)  # spremanje slike

            self.text.insert(END, "Selected image saved as " + saveAsJPG + "\n")

            self.convertedSize = os.path.getsize(
                saveAsJPG
            )  # sve nadalje je extra za prikazivanje kompresije
            compressRatio = round(oriSize[i] / self.convertedSize, 3)
            self.text.insert(
                END,
                "Ratio: "
                + str(round(oriSize[i] / 1000 / 1000, 3))
                + " / "
                + str(round(self.convertedSize / 1000 / 1000, 3))
                + "="
                + str(compressRatio)
                + "\n",
            )
            i = i + 1
            self.text.insert(
                END, "Save picture elsewhere or it will be destroyed in 10 seconds.\n"
            )

            def retentionPeriod():
                os.remove(saveAsJPG)
                self.text.insert(END, "Saved picture deleted.\n")

            t = threading.Timer(10.0, retentionPeriod)
            t.start()

    def convertPNG(self):  # funkcija pretvaranja u .png, po uzoru na .jpg
        os.chdir(self.destination.get())
        self.text.delete(0.0, END)
        self.adjustment(self.selectedIMGs)
        oriSize = list(self.selectedIMGs.values())
        i = 0
        qualvl = int(self.imgQuality.get())
        for saveAs, image in self.preConvertIMGs.items():
            saveAsPNG = saveAs + ".png"
            image.save(saveAsPNG, "PNG", quality=qualvl)

            self.text.insert(END, "Selected image saved as " + saveAsPNG + ".\n")

            self.convertedSize = os.path.getsize(saveAsPNG)
            compressRatio = round(oriSize[i] / self.convertedSize, 3)
            self.text.insert(
                END,
                "Ratio: "
                + str(round(oriSize[i] / 1000 / 1000, 3))
                + " / "
                + str(round(self.convertedSize / 1000 / 1000, 3))
                + "="
                + str(compressRatio)
                + "\n",
            )
            i = i + 1
            self.text.insert(
                END, "Save picture elsewhere or it will be destroyed in 10 seconds.\n"
            )

            def retentionPeriod():
                os.remove(saveAsPNG)
                self.text.insert(END, "Saved picture deleted.\n")

            tPNG = threading.Timer(10.0, retentionPeriod)
            tPNG.start()

    def convertBMP(self):  # funkcija pretvaranja u .bmp, po uzoru na .jpg
        os.chdir(self.destination.get())
        self.text.delete(0.0, END)
        self.adjustment(self.selectedIMGs)
        oriSize = list(self.selectedIMGs.values())
        i = 0
        qualvl = int(self.imgQuality.get())
        for saveAs, image in self.preConvertIMGs.items():
            saveAsBMP = saveAs + ".bmp"
            image.save(saveAsBMP, "BMP", quality=qualvl)

            self.text.insert(END, "Selected image saved as " + saveAsBMP + "\n")

            self.convertedSize = os.path.getsize(saveAsBMP)
            compressRatio = round(oriSize[i] / self.convertedSize, 3)
            self.text.insert(
                END,
                "Ratio: "
                + str(round(oriSize[i] / 1000 / 1000, 3))
                + " / "
                + str(round(self.convertedSize / 1000 / 1000, 3))
                + "="
                + str(compressRatio)
                + "\n",
            )
            i = i + 1
            self.text.insert(
                END, "Save picture elsewhere or it will be destroyed in 10 seconds.\n"
            )

            def retentionPeriod():
                os.remove(saveAsBMP)
                self.text.insert(END, "Saved picture deleted.\n")

            t = threading.Timer(10.0, retentionPeriod)
            t.start()

    def convertWEBP(self):  # funkcija pretvaranja u .webp, po uzoru na .jpg
        os.chdir(self.destination.get())
        self.text.delete(0.0, END)
        self.adjustment(self.selectedIMGs)
        oriSize = list(self.selectedIMGs.values())
        i = 0
        qualvl = int(self.imgQuality.get())
        for saveAs, image in self.preConvertIMGs.items():
            saveAsWEBP = saveAs + ".webp"
            image.save(saveAsWEBP, "WEBP", quality=qualvl)

            self.text.insert(END, "Selected image saved as " + saveAsWEBP + "\n")

            self.convertedSize = os.path.getsize(saveAsWEBP)
            compressRatio = round(oriSize[i] / self.convertedSize, 3)
            self.text.insert(
                END,
                "Ratio: "
                + str(round(oriSize[i] / 1000 / 1000, 3))
                + " / "
                + str(round(self.convertedSize / 1000 / 1000, 3))
                + "="
                + str(compressRatio)
                + "\n",
            )
            i = i + 1
            self.text.insert(
                END, "Save picture elsewhere or it will be destroyed in 10 seconds.\n"
            )

            def retentionPeriod():
                os.remove(saveAsWEBP)
                self.text.insert(END, "Saved picture deleted.\n")

            t = threading.Timer(10.0, retentionPeriod)
            t.start()

    def convertGIF(self):  # funkcija pretvaranja u .gif, po uzoru na .jpg
        os.chdir(self.destination.get())
        self.text.delete(0.0, END)
        self.adjustment(self.selectedIMGs)
        oriSize = list(self.selectedIMGs.values())
        i = 0
        qualvl = int(self.imgQuality.get())
        for saveAs, image in self.preConvertIMGs.items():
            saveAsGIF = saveAs + ".gif"
            image.save(saveAsGIF, "GIF", quality=qualvl)

            self.text.insert(END, "Selected image saved as " + saveAsGIF + "\n")

            self.convertedSize = os.path.getsize(saveAsGIF)
            compressRatio = round(oriSize[i] / self.convertedSize, 3)
            self.text.insert(
                END,
                "Ratio: "
                + str(round(oriSize[i] / 1000 / 1000, 3))
                + " / "
                + str(round(self.convertedSize / 1000 / 1000, 3))
                + "="
                + str(compressRatio)
                + "\n",
            )
            i = i + 1
            self.text.insert(
                END, "Save picture elsewhere or it will be destroyed in 10 seconds.\n"
            )

            def retentionPeriod():
                os.remove(saveAsGIF)
                self.text.insert(END, "Saved picture deleted.\n")

            t = threading.Timer(10.0, retentionPeriod)
            t.start()


root = Tk()

root.title("Image Converter")

root.geometry()

app = Application(root)

root.mainloop()

# schedule.every(10).minutes.do(retentionPeriod)

# while True:
# schedule.run_pending()
# time.sleep(1)
