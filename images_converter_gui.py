import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import pillow_heif
import os
import threading
import sys
import webbrowser
import subprocess

class ImageConverterApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Converter — JSOFT")
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            self.iconbitmap(os.path.join(base_path, "icon.ico"))
            self.tk.call("source", os.path.join(base_path, "azure-dark.tcl"))
        except Exception as e:
            print("Resource load failed:", e)

        pillow_heif.register_heif_opener()

        self.configure(bg="#1E1E1E")
        self.geometry("560x500")
        self.minsize(520, 480)
        self.file_paths = []
        self.output_dir = None

        self.supported_input_exts = [".heic", ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"]
        self.supported_output_formats = ["PNG", "JPEG", "WEBP", "BMP", "TIFF"]

        style = ttk.Style(self)
        style.theme_use("azure-dark")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.map("TButton",
                  background=[("active", "#d17c00")],
                  foreground=[("active", "#ffffff")])

        style.configure("green.Horizontal.TProgressbar", troughcolor="#3c3f41", bordercolor="#3c3f41",
                        background="#00C853", lightcolor="#00C853", darkcolor="#00C853")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Selected files:", fg="white", bg="#1E1E1E",
                 font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))

        self.file_listbox = tk.Listbox(self, width=60, height=10, bg="#2D2D30", fg="white",
                                       selectbackground="#d17c00", relief=tk.FLAT)
        self.file_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        self.file_listbox.drop_target_register(DND_FILES)
        self.file_listbox.dnd_bind("<<Drop>>", self.drop_files)

        button_frame = tk.Frame(self, bg="#1E1E1E")
        button_frame.pack(pady=5)

        button_width = 20
        self.add_button = ttk.Button(button_frame, text="➕   Add Files   ", command=self.add_files, width=button_width)
        self.add_button.grid(row=0, column=0, padx=5)

        self.remove_button = ttk.Button(button_frame, text="❌ Remove Selected", command=self.remove_selected, width=button_width)
        self.remove_button.grid(row=0, column=1, padx=5)

        format_label = tk.Label(self, text="Output Format:", fg="white", bg="#1E1E1E",
                                font=("Segoe UI", 10))
        format_label.pack(pady=(10, 0))

        self.output_format = ttk.Combobox(self, values=self.supported_output_formats, state="readonly")
        self.output_format.current(0)
        self.output_format.pack(pady=5)

        path_frame = tk.Frame(self, bg="#1E1E1E")
        path_frame.pack(pady=5)

        self.path_button = ttk.Button(path_frame, text="📁 Choose Output Folder", command=self.choose_output_folder)
        self.path_button.grid(row=0, column=0, padx=5)

        self.open_folder_button = ttk.Button(path_frame, text="📂 Open Output Folder", command=self.open_output_folder)
        self.open_folder_button.grid(row=0, column=1, padx=5)

        self.path_label = tk.Label(self, text="No folder selected", fg="#aaa", bg="#1E1E1E", font=("Segoe UI", 9))
        self.path_label.pack()

        self.progress = ttk.Progressbar(self, style="green.Horizontal.TProgressbar",
                                        orient="horizontal", mode="determinate", length=300)
        self.progress.pack(pady=10)

        self.convert_button = ttk.Button(self, text="🖌 Convert", command=self.start_conversion_thread)
        self.convert_button.pack(pady=10)

        contact_frame = tk.Frame(self, bg="#1E1E1E")
        contact_frame.pack(pady=(0, 8))

        tk.Label(contact_frame, text="© 2025 JSOFT | ", fg="#888", bg="#1E1E1E", font=("Segoe UI", 8)).pack(side=tk.LEFT)

        tg_link = tk.Label(contact_frame, text="Telegram", fg="#00AEEF", bg="#1E1E1E", font=("Segoe UI", 8, "underline"), cursor="hand2")
        tg_link.pack(side=tk.LEFT)
        tg_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/psygrammator"))

        tk.Label(contact_frame, text=" | ", fg="#888", bg="#1E1E1E", font=("Segoe UI", 8)).pack(side=tk.LEFT)

        dc_link = tk.Label(contact_frame, text="Discord: psygrammator", fg="#00AEEF", bg="#1E1E1E", font=("Segoe UI", 8, "underline"), cursor="hand2")
        dc_link.pack(side=tk.LEFT)
        dc_link.bind("<Button-1>", lambda e: webbrowser.open("https://discord.com/users/830176153029050368"))

    def add_files(self):
        filetypes = [("Supported Images", " ".join(f"*{ext}" for ext in self.supported_input_exts))]
        paths = filedialog.askopenfilenames(filetypes=filetypes)
        self._add_paths(paths)

    def drop_files(self, event):
        paths = self.tk.splitlist(event.data)
        self._add_paths(paths)

    def _add_paths(self, paths):
        for path in paths:
            ext = os.path.splitext(path)[1].lower()
            if ext in self.supported_input_exts and path not in self.file_paths:
                self.file_paths.append(path)
                self.file_listbox.insert(tk.END, os.path.basename(path))

    def remove_selected(self):
        selected_indices = list(self.file_listbox.curselection())
        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.file_paths[index]

    def choose_output_folder(self):
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.output_dir = folder
            self.path_label.config(text=f"📂 {folder}")

    def open_output_folder(self):
        if self.output_dir and os.path.isdir(self.output_dir):
            os.startfile(self.output_dir)
        else:
            messagebox.showwarning("Warning", "No valid folder to open.")

    def start_conversion_thread(self):
        threading.Thread(target=self.convert_files, daemon=True).start()

    def convert_files(self):
        if not self.file_paths:
            messagebox.showerror("Error", "No files selected.")
            return

        if not self.output_dir:
            messagebox.showwarning("Folder not selected", "Please select a folder to save.")
            return

        output_format = self.output_format.get().upper()
        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_paths)

        success = 0
        for i, path in enumerate(self.file_paths):
            try:
                img = Image.open(path)
                filename = os.path.splitext(os.path.basename(path))[0] + "." + output_format.lower()
                out_path = os.path.join(self.output_dir, filename)
                if output_format in ["JPG", "JPEG"]:
                    img = img.convert("RGB")
                    img.save(out_path, format="JPEG")
                else:
                    img.save(out_path, format=output_format)
                success += 1
            except Exception as e:
                print(f"Error converting {path}: {e}")
            self.progress["value"] = i + 1
            self.update_idletasks()

        messagebox.showinfo("Done", f"Successfully converted: {success} files.")

if __name__ == "__main__":
    app = ImageConverterApp()
    app.mainloop()
