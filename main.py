import customtkinter as ctk
from customtkinter import filedialog


class BatchFolderRenamer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Batch Folder Renamer")
        self.geometry("500x500")
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

        # Row 3: Start Button
        self.start_btn = ctk.CTkButton(self, text="Start Process", height=20)
        self.start_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.start_btn.configure(font=ctk.CTkFont(size=16, weight="bold"))

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Target Folder")
        if folder_selected:
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder_selected)
            self.path_entry.configure(state="readonly")


if __name__ == "__main__":
    app = BatchFolderRenamer()
    app.mainloop()
