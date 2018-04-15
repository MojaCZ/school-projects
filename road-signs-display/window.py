import tkinter as tk
from PIL import Image, ImageTk


class mainWindow:

	speed = "speed"
	sight1 = "/home/moja/Programming/Python/RoadSign/pictures/prednost/P01.jpg"
	sight2 = "/home/moja/Programming/Python/RoadSign/pictures/prikazove/C01.jpg"
	sight3 = "/home/moja/Programming/Python/RoadSign/pictures/vystrazne/A01a.jpg"
	sight4 = "/home/moja/Programming/Python/RoadSign/pictures/zakazove/B01.jpg"

	def __init__(self, master):

		frame_head = tk.Frame(master, height=100)
		frame_head.config(bg='blue')
		frame_head.pack(fill="x", expand=0)

		frame_body = tk.Frame(master)
		frame_body.config(bg='red')
		frame_body.pack(fill="both", expand=True)

		self.headBTN = tk.Button(frame_head, text="HISTORY")
		self.headBTN.pack()

		img1 = Image.open(self.sight1)
		img1 = img1.resize((100,100), Image.ANTIALIAS)
		self.img1Tk = ImageTk.PhotoImage(img1)
		self.S1 = tk.Button(frame_body, image=self.img1Tk)
		self.S1.pack()

		img2 = Image.open(self.sight2)
		img2 = img2.resize((100,100), Image.ANTIALIAS)
		self.img2Tk = ImageTk.PhotoImage(img2)
		self.sight2 = tk.Button(frame_body, image=self.img2Tk)
		self.sight2.pack()

		img3 = Image.open(self.sight3)
		img3 = img3.resize((100,100), Image.ANTIALIAS)
		self.img3Tk = ImageTk.PhotoImage(img3)
		self.sight3 = tk.Button(frame_body, image=self.img3Tk)
		self.sight3.pack()

		img4 = Image.open(self.sight4)
		img4 = img4.resize((100,100), Image.ANTIALIAS)
		self.img4Tk = ImageTk.PhotoImage(img4)
		self.sight4 = tk.Button(frame_body, image=self.img4Tk)
		self.sight4.pack()


def main():
	root = tk.Tk()
	root.geometry("384x512")	#tablet is 768x1024

	W = mainWindow(root)

	root.mainloop()

main()
