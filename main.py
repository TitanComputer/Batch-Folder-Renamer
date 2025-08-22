import customtkinter as ctk
import tkinter as tk


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

        # Row 1: Entry + Browse Button
        self.path_entry = ctk.CTkEntry(self)
        self.path_entry.insert(0, "C:\\inetpub\\wwwroot\\T2")
        self.path_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")

        self.browse_btn = ctk.CTkButton(self, text="Browse")
        self.browse_btn.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")

        # Row 2: Frame with Label + Text + Scrollbar
        self.prefix_container = ctk.CTkFrame(self)
        self.prefix_container.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.prefix_container.grid_rowconfigure(1, weight=1)
        self.prefix_container.grid_columnconfigure(0, weight=1)

        self.prefix_label = ctk.CTkLabel(self.prefix_container, text="Prefixes To Remove", anchor="w")
        self.prefix_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

        self.prefix_text = tk.Text(
            self.prefix_container, wrap="word", bg="#2b2b2b", fg="white", insertbackground="white"
        )
        self.prefix_text.grid(row=1, column=0, sticky="nsew", padx=(5, 0), pady=5)

        self.scrollbar = tk.Scrollbar(self.prefix_container, command=self.prefix_text.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns", pady=5)
        self.prefix_text.config(yscrollcommand=self.scrollbar.set)

        # Row 3: Start Button
        self.start_btn = ctk.CTkButton(self, text="Start Process")
        self.start_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


if __name__ == "__main__":
    app = BatchFolderRenamer()
    app.mainloop()
