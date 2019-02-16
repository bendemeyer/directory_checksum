import os
import sys
from multiprocessing import Process
from time import sleep

from tkinter import Tk, filedialog, messagebox, END, N, S, E, W
from tkinter.ttk import Frame, Label, Entry, Button, Style
from PIL import Image, ImageTk

from build_csv import build_checksum_csv


if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


class Gif(object):
    def __init__(self, file):
        self._filename = file
        self._img = Image.open(self._filename)
        self._delay = self._img.info.get("duration", 100)
        self._index = 0
        self._frames = self._get_frames()
        self._length = len(self._frames)

    def _get_frames(self):
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(self._img.copy()))
                self._img.seek(len(frames))
        except EOFError:
            pass
        self._img.seek(self._index)
        return frames

    def get_frame_and_advance(self):
        old_index = self._index
        self._index += 1
        if self._index == self._length:
            self._index = 0
        return self._frames[old_index]

    def get_delay(self):
        return self._delay


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Generate Checksum CSV")
        self.init_ui()
        self.build_fields()
        self.build_buttons()
        self.position_window()

    def init_ui(self):
        self.background_frame = Frame(self.master)
        self.background_frame.pack()

        self.main_frame = Frame(self.background_frame)
        self.main_frame.grid()
        self.main_frame.grid_configure(padx=20, pady=20)

    def build_fields(self):
        self.field_frame = Frame(self.main_frame)
        self.field_frame.grid(row=0, column=0)

        self.dir_label = Label(self.field_frame, text="Select a folder to scan")
        self.dir_label.grid(row=0, column=0, columnspan=2, sticky=W)

        self.dir_entry = Entry(self.field_frame, width=35)
        self.dir_entry.grid(row=1, column=0, ipadx=3, ipady=3)

        self.dir_dialog = Button(self.field_frame, text="...", command=self.get_directory, width=3)
        self.dir_dialog.grid(row=1, column=1, padx=(5,0))

        self.file_label = Label(self.field_frame, text="Choose a location to save your CSV")
        self.file_label.grid(row=2, column=0, columnspan=2, sticky=W, pady=(30,0))

        self.file_entry = Entry(self.field_frame, width=35)
        self.file_entry.grid(row=3, column=0, ipadx=3, ipady=3)

        self.file_dialog = Button(self.field_frame, text="...", command=self.get_savefile, width=3)
        self.file_dialog.grid(row=3, column=1, padx=(5,0))

    def build_buttons(self):
        self.button_frame = Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, sticky=E, pady=(30,0))

        self.run_button = Button(self.button_frame, text="Run", command=self.run_process)
        self.run_button.grid(row=0, column=2, padx=(5,0))

        self.cancel_button = Button(self.button_frame, text="Cancel", command=self.master.quit)
        self.cancel_button.grid(row=0, column=1, padx=(5,0))

        self.empty_gif = Gif(os.path.join(application_path, "resources", "empty_32.gif"))
        self.running_gif = Gif(os.path.join(application_path, "resources", "running_32.gif"))
        self.gif_label = Label(self.button_frame, image=self.empty_gif.get_frame_and_advance())
        self.gif_label.grid(row=0, column=0)

    def position_window(self):
        self.master.update_idletasks()
        screen_w = self.master.winfo_screenwidth()
        screen_h = self.master.winfo_screenheight()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = int((screen_w - width) / 2)
        y = int((screen_h - height) / 2)
        self.master.geometry("{w}x{h}+{x}+{y}".format(w=width, h=height, x=x, y=y))
        self.master.update()

    def animate_while_alive(self, process):
        if process.is_alive():
            self.gif_label.configure(image=self.running_gif.get_frame_and_advance())
            self.master.update()
            sleep(self.running_gif.get_delay() / 1000)
            self.animate_while_alive(process)
        else:
            self.gif_label.configure(image=self.empty_gif.get_frame_and_advance())
            self.master.update()

    def get_directory(self):
        directory = filedialog.askdirectory()
        self.dir_entry.delete(0, END)
        self.dir_entry.insert(0, directory)

    def get_savefile(self):
        savefile = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv")])
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, savefile)

    def run_process(self):
        directory = self.dir_entry.get()
        savefile = self.file_entry.get()
        if not directory or not savefile:
            messagebox.showwarning("Missing Required Fields", "You are missing a required field!")
            return
        try:
            self.master.configure(cursor="watch")
            self.dir_entry.configure(state="disabled", cursor="watch")
            self.dir_dialog.configure(state="disabled")
            self.file_entry.configure(state="disabled", cursor="watch")
            self.file_dialog.configure(state="disabled")
            self.cancel_button.configure(state="disabled")
            self.run_button.configure(state="disabled")
            self.master.update()
            csv_process = Process(target=build_checksum_csv, args=(directory, savefile))
            csv_process.start()
            self.animate_while_alive(csv_process)
            csv_process.join()
        except Exception as e:
            messagebox.showerror("Error!", "The process failed with the following error:\n\n{0}".format(str(e)))
            return
        finally:
            self.master.configure(cursor="")
            self.dir_entry.configure(state="enabled", cursor="xterm")
            self.dir_dialog.configure(state="enabled")
            self.file_entry.configure(state="enabled", cursor="xterm")
            self.file_dialog.configure(state="enabled")
            self.cancel_button.configure(state="enabled")
            self.run_button.configure(state="enabled")
            self.master.update()
        messagebox.showinfo("Complete!", "The process completed successfully")
        self.dir_entry.delete(0, END)
        self.file_entry.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    my_gui = App(root)
    root.mainloop()