import os
import shutil
import tkinter.messagebox
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import ttk

from script.classifier import FilesClassifier

class FileClassifierApp:
    def __init__(self, master):
        self.master = master
        master.title("Classy")

        self.input_folder_var = ctk.StringVar()
        self.target_folder_var = ctk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.master, text="Input Folder:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(self.master, textvariable=self.input_folder_var, width=300).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(self.master, text="Browse Input Folder", command=self.browse_input_folder).grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkLabel(self.master, text="Target Folder:").grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkEntry(self.master, textvariable=self.target_folder_var, width=300).grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(self.master, text="Browse Target Folder", command=self.browse_target_folder).grid(row=1, column=2, padx=10, pady=10)

        ctk.CTkButton(self.master, text="Start Classification", command=self.start_classification).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.progress = ttk.Progressbar(self.master, length=500,orient="horizontal",mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def browse_input_folder(self):
        input_folder = ctk.filedialog.askdirectory(title="Select Input Folder")
        if input_folder:
            self.input_folder_var.set(input_folder)

    def browse_target_folder(self):
        target_folder = ctk.filedialog.askdirectory(title="Select Target Folder")
        if target_folder:
            self.target_folder_var.set(target_folder)

    def start_classification(self):
        input_folder = self.input_folder_var.get()
        target_folder = self.target_folder_var.get()

        if not os.path.exists(input_folder):
            tkinter.messagebox.showerror("Error", f"The specified input folder '{input_folder}' does not exist.")
            return

        if not os.path.exists(target_folder):
            tkinter.messagebox.showerror("Error", f"The specified target folder '{target_folder}' does not exist.")
            return

        confirm = tkinter.messagebox.askyesno("Confirmation", "Are you sure you want to proceed with classification?")
        if not confirm:
            return

        classifier = FilesClassifier()
        results = classifier.classify_folder(input_folder)

        total_files = len(results)
        self.progress["maximum"] = total_files

        for index, result in enumerate(results, 1):
            file_name, class_label = result
            source_path = os.path.join(input_folder, file_name)
            destination_folder = os.path.join(target_folder, class_label)

            destination_path = os.path.join(destination_folder, file_name)
            try:
                if not os.path.exists(os.path.dirname(destination_path)):
                    os.makedirs(os.path.dirname(destination_path))
                shutil.move(source_path, destination_path)
            except FileNotFoundError:
                tkinter.messagebox.showerror("Error", f"{source_path} not found.")
                return
            except Exception as e:
                tkinter.messagebox.showerror("Error", f"Error moving {file_name}: {e}")
                return

            self.progress["value"] = index
            self.master.update_idletasks()  

        tkinter.messagebox.showinfo("Info", "Classification completed.")
        self.progress["value"] = 0
        self.master.update_idletasks()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FileClassifierApp(root)
    root.mainloop()