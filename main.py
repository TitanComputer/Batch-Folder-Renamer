import customtkinter as ctk
from PIL import ImageTk
from customtkinter import filedialog
import os
from tkinter import messagebox
import threading
import re
import string


class BatchFolderRenamer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Batch Folder Renamer")
        self.iconpath = ImageTk.PhotoImage(file="icon.png")
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        self.update_idletasks()
        width = 500
        height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        # Grid Configuration for main window
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=4, uniform="col")
        self.grid_columnconfigure(1, weight=1, uniform="col")
        font_bold = ctk.CTkFont(size=14, weight="bold")

        # Row 1: Entry + Browse Button
        self.path_entry = ctk.CTkEntry(self, height=20, placeholder_text="Target Directory", font=font_bold)
        self.path_entry.insert(0, "C:\\inetpub\\wwwroot\\T2")
        self.path_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.path_entry.configure(state="readonly")

        self.browse_btn = ctk.CTkButton(self, text="Browse", height=20)
        self.browse_btn.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        self.browse_btn.configure(font=font_bold)
        self.browse_btn.configure(command=self.browse_folder)

        # Row 2: Frame with Label + Textbox
        self.prefix_container = ctk.CTkFrame(self)
        self.prefix_container.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.prefix_container.grid_rowconfigure(1, weight=1)
        self.prefix_container.grid_columnconfigure(0, weight=1)

        self.prefix_label = ctk.CTkLabel(self.prefix_container, text="Prefixes To Remove", anchor="w")
        self.prefix_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

        self.prefix_text = ctk.CTkTextbox(
            self.prefix_container,
            wrap="word",
            font=ctk.CTkFont(size=16),
            corner_radius=0,
        )
        self.prefix_text.grid(row=1, column=0, sticky="nsew", padx=(5, 0), pady=5)
        self.prefix_text.insert("0.0", "Torrenting\n")
        self.prefix_text.insert("1.0", "www.UIndex.org\n")

        # Row 3: Start Button
        self.start_btn = ctk.CTkButton(self, text="Start Process", height=20)
        self.start_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.start_btn.configure(font=ctk.CTkFont(size=16, weight="bold"))
        self.start_btn.configure(command=self.start_process_threaded)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Target Folder")
        if folder_selected:
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder_selected)
            self.path_entry.configure(state="readonly")

    def start_process_threaded(self):
        threading.Thread(target=self.start_process, daemon=True).start()

    def start_process(self):
        folder_path = self.path_entry.get()
        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Selected folder does not exist.")
            return

        prefixes = [line.strip() for line in self.prefix_text.get("0.0", "end").splitlines() if line.strip()]

        count = 0
        for item in os.listdir(folder_path):
            full_path = os.path.join(folder_path, item)
            if os.path.isdir(full_path):
                new_name = item

                # Remove prefixes
                for prefix in prefixes:
                    if new_name.startswith(prefix):
                        new_name = new_name[len(prefix) :]
                new_name = new_name.strip()

                # Remove suffix starting from sXX or SXX
                match = re.search(r"(s\d{2})", new_name, re.IGNORECASE)
                if match:
                    index = match.start()
                    new_name = new_name[:index].strip()

                # Remove leading/trailing invalid chars
                allowed_chars = string.ascii_letters + string.digits
                new_name = re.sub(f"^[^{allowed_chars}]+|[^{allowed_chars}]+$", "", new_name)

                # Replace dots, dashes, underscores with spaces
                new_name = re.sub(r"[.\-_]+", " ", new_name)

                # Capitalize and convert spaces to hyphens
                new_name = new_name.title()
                new_name = new_name.replace(" ", "-")

                if new_name and new_name != item:
                    new_full_path = os.path.join(folder_path, new_name)
                    if not os.path.exists(new_full_path):
                        try:
                            os.rename(full_path, new_full_path)
                            count += 1
                        except PermissionError:
                            messagebox.showerror(
                                "Access Denied",
                                "Cannot access or modify the selected folder.\n"
                                "Please check permissions or run the program as Administrator.",
                            )
                            return

        if count == 0:
            messagebox.showinfo("Done", "No folders were processed.")
        else:
            messagebox.showinfo("Done", f"{count} folders renamed successfully.")


if __name__ == "__main__":
    app = BatchFolderRenamer()
    app.mainloop()
