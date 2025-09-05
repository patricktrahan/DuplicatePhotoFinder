from doctest import master
import os
import sys
from send2trash import send2trash
import hashlib
from tkinter import Tk, filedialog, PhotoImage
from tkinter import StringVar
from tkinter import ttk
from tkinter.ttk import Frame, Button, Label, Scrollbar, Checkbutton, Style
from tkinter import Listbox, SINGLE, Canvas, IntVar
from tkinter import Frame as tkFrame
from PIL import Image, ImageTk

class DuplicatePhotoFinder:
    def __init__(self, master):
        self.master = master
        master.title("Duplicate Photo Finder")
        master.state('zoomed')

        style = Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 12))
        style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), background='#e0e0e0')
        style.configure('TButton', font=('Segoe UI', 12), padding=6)
        style.configure('TCheckbutton', font=('Segoe UI', 11))

        self.header = Label(master, text="Duplicate Photo Finder", style='Header.TLabel', anchor='center')
        self.header.pack(fill='x', pady=(10, 0))

        self.label = Label(master, text="Select a folder to scan for duplicate photos.")
        self.label.pack(pady=(10, 0))

        self.select_button = Button(master, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=5)

        self.scan_button = Button(master, text="Scan for Duplicates", command=self.scan_folder, state='disabled')
        self.scan_button.pack(pady=5)

        self.delete_selected_button = Button(master, text="Delete Selected", command=self.delete_selected, state='disabled')
        self.delete_selected_button.pack(pady=5)

        self.listbox_label = Label(master, text="Duplicate Groups:", style='Header.TLabel')
        self.listbox_label.pack(fill='x', pady=(20, 0))

        self.listbox = Listbox(master, selectmode='extended', width=80, font=('Segoe UI', 11))
        self.listbox.pack(fill='both', expand=True, padx=20, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.show_images)

        self.preview_label = Label(master, text="Preview & Select Files to Delete:", style='Header.TLabel')
        self.preview_label.pack(fill='x', pady=(20, 0))

    
        self.preview_canvas = Canvas(master, height=500, bg='#f5f5f5', highlightthickness=0)
        self.preview_scrollbar = Scrollbar(master, orient='vertical', command=self.preview_canvas.yview)
        self.preview_canvas.configure(yscrollcommand=self.preview_scrollbar.set)
        self.preview_canvas.pack(fill='both', expand=True, side='left', padx=(20,0), pady=5)
        self.preview_scrollbar.pack(fill='y', expand=False, side='right', padx=(0,20), pady=5)
        self.preview_frame = tkFrame(self.preview_canvas)
        self.preview_canvas.create_window((0,0), window=self.preview_frame, anchor='nw')
        self.preview_frame.bind('<Configure>', lambda e: self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox('all')))
        self.button_frame = tkFrame(master)
        self.button_frame.pack(fill='x', pady=(20, 10))

        # Enable mouse wheel scrolling
        self.preview_canvas.bind('<MouseWheel>', self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.preview_canvas.yview_scroll(int(-1*(event.delta/120)), "units")



        self.folder_path = None
        self.duplicates = {}

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.scan_button.config(state='normal')
            self.label.config(text=f"Selected: {self.folder_path}")

    def scan_folder(self):
        self.duplicates = self.find_duplicates(self.folder_path)
        self.listbox.delete(0, 'end')
        self.preview_images = []
        self.hash_list = []
        for hash_val, files in self.duplicates.items():
            if len(files) > 1:
                self.listbox.insert('end', f"{len(files)} duplicates: {', '.join(os.path.basename(f) for f in files)}")
                self.hash_list.append(hash_val)
        if not self.duplicates:
            self.label.config(text="No duplicates found.")
            self.delete_selected_button.config(state='disabled')
        else:
            self.label.config(text="Select a group to preview and delete duplicates.")
            self.delete_selected_button.config(state='normal')

    def find_duplicates(self, folder):
        hashes = {}
        print("Scanning for image files...")
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                try:
                    with open(path, 'rb') as f:
                        filehash = hashlib.md5(f.read()).hexdigest()
                    hashes.setdefault(filehash, []).append(path)
                except Exception as e:
                    print(f"Error reading {path}: {e}")
        for h, f in hashes.items():
            if len(f) > 1:
                return {h: f for h, f in hashes.items() if len(f) > 1}

    def show_images(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        # Clear previous previews
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        self.preview_images = []
        self.delete_vars = []
        row = 0
        for idx in selection:
            hash_val = self.hash_list[idx]
            files = self.duplicates[hash_val]
            group_vars = []
            for i, file in enumerate(files):
                from tkinter import Frame as tkFrame, Label as tkLabel, Checkbutton as tkCheckbutton
                frame = tkFrame(self.preview_frame, bd=2, relief='solid')
                var = IntVar()
                chk = tkCheckbutton(frame, text="Delete", variable=var)
                chk.pack()
                try:
                    img = Image.open(file)
                    img.verify()  # Verify it's an image
                    img = Image.open(file)  # Reopen for thumbnail
                    img.thumbnail((200, 200))
                    photo = ImageTk.PhotoImage(img)
                    self.preview_images.append(photo)
                    lbl = tkLabel(frame, image=photo)
                    lbl.image = photo
                    lbl.pack()
                except Exception as e:
                    lbl = tkLabel(frame, text="Not an image", fg="red")
                    lbl.pack()
                name_lbl = tkLabel(frame, text=file, wraplength=200, justify='center')
                name_lbl.pack()
                # Bind click events to toggle checkbox
                def toggle_var(event, v=var):
                    v.set(0 if v.get() else 1)
                lbl.bind('<Button-1>', toggle_var)
                name_lbl.bind('<Button-1>', toggle_var)
                group_vars.append((file, var))
                frame.grid(row=row, column=i, padx=5, pady=5)
            self.delete_vars.append(group_vars)
            row += 1

    def delete_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        files_to_delete = []
        # Use checkboxes if any are selected, otherwise keep first file in each group
        for group in getattr(self, 'delete_vars', []):
            checked = [file for file, var in group if var.get()]
            if checked:
                files_to_delete.extend(checked)
            else:
                # Keep the first file, delete the rest
                files_to_delete.extend([file for file, _ in group][1:])
        for file in files_to_delete:
                import os
                normalized_path = os.path.normpath(file)
                print(f"Attempting to send to recycle bin: {normalized_path}")
                try:
                    send2trash(normalized_path)
                    print(f"Sent to recycle bin: {normalized_path}")
                except Exception as e:
                    print(f"Error sending {normalized_path} to recycle bin: {e}")
        if hasattr(self, 'preview_frame'):
            for widget in self.preview_frame.winfo_children():
                widget.destroy()
        self.scan_folder()
        # Automatically refresh preview for current selection
        self.show_images(None)

    def delete_file(self, file, window):
        try:
            send2trash(file)
            window.destroy()
            self.scan_folder()
        except Exception as e:
            print(f"Error sending {file} to recycle bin: {e}")

if __name__ == "__main__":
    root = Tk()
    app = DuplicatePhotoFinder(root)
    root.mainloop()
