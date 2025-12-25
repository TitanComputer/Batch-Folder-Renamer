import customtkinter as ctk
from customtkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from idlelib.tooltip import Hovertip
import os
import threading
import re
import string
import sys
import time
import webbrowser

APP_VERSION = "1.4.1"
APP_NAME = "Batch Folder Renamer"

# --- Single Instance Logic START with Timeout ---
APP_LOCK_DIR = os.path.join(os.getenv("LOCALAPPDATA", os.getenv("HOME", "/tmp")), APP_NAME)
LOCK_FILE = os.path.join(APP_LOCK_DIR, "app.lock")
LOCK_TIMEOUT_SECONDS = 60

os.makedirs(APP_LOCK_DIR, exist_ok=True)
IS_LOCK_CREATED = False

if os.path.exists(LOCK_FILE):
    try:
        lock_age = time.time() - os.path.getmtime(LOCK_FILE)

        if lock_age > LOCK_TIMEOUT_SECONDS:
            os.remove(LOCK_FILE)
            print(f"Removed stale lock file (Age: {int(lock_age)}s).")
        else:
            try:
                temp_root = tk.Tk()
                temp_root.withdraw()
                messagebox.showwarning(
                    f"{APP_NAME} v{APP_VERSION}",
                    f"{APP_NAME} is already running.\nOnly one instance is allowed.",
                )
                temp_root.destroy()
            except Exception:
                print("Application is already running.")

            sys.exit(0)

    except Exception as e:
        print(f"Error checking lock file: {e}. Exiting.")
        sys.exit(0)

try:
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    IS_LOCK_CREATED = True
except Exception as e:
    print(f"Could not create lock file: {e}")
    sys.exit(1)

# --- Single Instance Logic END with Timeout ---


class BatchFolderRenamer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")

        # Load assets safely (assuming 'assets' folder is alongside the script)
        # Using a resource path helper if needed, but for simplicity we rely on relative path here.
        temp_dir = os.path.dirname(__file__)
        try:
            self.iconpath = ImageTk.PhotoImage(file=self.resource_path(os.path.join(temp_dir, "assets", "icon.png")))
            heart_path = self.resource_path(os.path.join(temp_dir, "assets", "heart.png"))
            img = Image.open(heart_path)
            width_img, height_img = img.size
            # For CTk widgets (scaled, recommended)
            self.heart_image = ctk.CTkImage(
                light_image=Image.open(heart_path), dark_image=Image.open(heart_path), size=(width_img, height_img)
            )

            # For window icon (must be PhotoImage)
            self.heart_icon = ImageTk.PhotoImage(file=heart_path)
            self.wm_iconbitmap()
            self.iconphoto(False, self.iconpath)
        except Exception:
            # Fallback if assets are missing
            self.iconpath = None
            self.heart_image = None
            print("Warning: Could not load application icons.")

        # Window Configuration
        self.protocol("WM_DELETE_WINDOW", self.on_close)
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

        # Row 3: Start + Donate Buttons (inside a local frame)
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

        # Local grid configuration (no changes to main layout)
        button_frame.grid_columnconfigure(0, weight=3)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)

        # Start Button
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Start Process",
            height=20,
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.start_process_threaded,
        )
        self.start_btn.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        # Donate Button
        self.donate_button = ctk.CTkButton(
            button_frame,
            text="Donate",
            image=self.heart_image,
            compound="right",
            fg_color="#FFD700",
            hover_color="#FFC400",
            text_color="#000000",
            font=ctk.CTkFont(size=20, weight="bold"),
            height=20,
            command=self.donate,
        )
        self.donate_button.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        # --- Lock Updater Control START ---
        self.lock_refresh_active = True
        if "IS_LOCK_CREATED" in globals() and IS_LOCK_CREATED:
            self.lock_thread = threading.Thread(target=self._lock_updater, daemon=True)
            self.lock_thread.start()
            print("Started lock refresh thread.")
        # --- Lock Updater Control END ---

    def _lock_updater(self):
        """
        Periodically updates the lock file timestamp to keep the lock fresh.
        Runs in a separate thread.
        """
        global IS_LOCK_CREATED
        if not IS_LOCK_CREATED:
            return

        while self.lock_refresh_active:
            try:
                os.utime(LOCK_FILE, None)
                print("Lock file timestamp updated.")
            except Exception as e:
                print(f"Error refreshing lock: {e}")
                break

            time.sleep(LOCK_TIMEOUT_SECONDS / 2)

        print("Lock refresh thread stopped.")

    def on_close(self):
        """
        Handles application shutdown, cleans up the lock file, saves config,
        and checks if a process is running before exiting.
        """

        # --- Single Instance Cleanup START ---
        global IS_LOCK_CREATED
        if "IS_LOCK_CREATED" in globals() and IS_LOCK_CREATED:
            self.lock_refresh_active = False
            try:
                if self.lock_thread.is_alive():
                    self.lock_thread.join(0.5)
                os.remove(LOCK_FILE)
            except Exception as e:
                print(f"Could not remove lock file: {e}")
        # --- Single Instance Cleanup END ---

        self.destroy()

    def resource_path(self, relative_path):
        temp_dir = os.path.dirname(__file__)
        return os.path.join(temp_dir, relative_path)

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

        items = os.listdir(folder_path)
        folders = [i for i in items if os.path.isdir(os.path.join(folder_path, i))]
        total_folders = len(folders)
        renamed_count = 0
        skipped_count = 0
        failed_count = 0
        for item in folders:
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

                # Remove extra spaces
                new_name = re.sub(r"\s+", " ", new_name)

                # Replace & with And
                new_name = new_name.replace("&", "And")

                # Capitalize and convert spaces to hyphens
                words = new_name.split()

                fixed_words = []
                for w in words:
                    if any(char.isdigit() for char in w):
                        fixed_words.append(w)
                    else:
                        fixed_words.append(w.capitalize())

                new_name = " ".join(fixed_words)
                new_name = new_name.replace(" ", "-")

                def case_sensitive_exists(path):
                    directory, name = os.path.split(path)
                    return name in os.listdir(directory)

                if not new_name:
                    failed_count += 1

                elif new_name == item:
                    # Folder already has the correct name
                    skipped_count += 1

                else:
                    new_full_path = os.path.join(folder_path, new_name)
                    if case_sensitive_exists(new_full_path):
                        failed_count += 1
                    else:
                        try:
                            os.rename(full_path, new_full_path)
                            renamed_count += 1
                        except PermissionError:
                            messagebox.showerror(
                                "Access Denied",
                                "Cannot access or modify the selected folder.\n"
                                "Please check permissions or run the program as Administrator.",
                            )
                            return

        if total_folders == 0:
            messagebox.showinfo("Done", "No folders were found in the selected directory.\n" "Nothing to process.")

        elif renamed_count == total_folders:
            messagebox.showinfo(
                "Done", f"All folders were processed successfully.\n\n" f"Renamed folders: {renamed_count}"
            )

        elif skipped_count == total_folders:
            messagebox.showinfo(
                "Done",
                f"All folders already had correct names.\n\n"
                f"Checked folders: {skipped_count}\n"
                f"No changes were required.",
            )

        elif renamed_count == 0 and failed_count == total_folders:
            messagebox.showinfo("Done", f"No folders could be renamed.\n\n" f"Failed to rename: {failed_count}")

        elif failed_count == 0:
            messagebox.showinfo(
                "Done",
                f"Operation completed successfully.\n\n"
                f"Renamed folders: {renamed_count}\n"
                f"Already have correct names: {skipped_count}",
            )

        else:
            messagebox.showinfo(
                "Done",
                f"Operation completed successfully.\n\n"
                f"Renamed folders: {renamed_count}\n"
                f"Already have correct names: {skipped_count}\n"
                f"Failed to rename: {failed_count}",
            )

    def donate(self):
        """Opens a donation window with options to support the project."""
        top = ctk.CTkToplevel(self)
        top.title("Donate ❤")
        top.resizable(False, False)
        self.attributes("-disabled", True)

        def top_on_close():
            self.attributes("-disabled", False)
            top.destroy()
            self.lift()
            self.focus()

        top.protocol("WM_DELETE_WINDOW", top_on_close)
        top.withdraw()

        # Set icon safely for CTk
        if self.heart_icon:
            top.after(250, lambda: top.iconphoto(False, self.heart_icon))

        # Center the window
        width = 500
        height = 300
        x = (top.winfo_screenwidth() // 2) - (width // 2)
        y = (top.winfo_screenheight() // 2) - (height // 2)
        top.geometry(f"{width}x{height}+{x}+{y}")

        # Configure grid for Toplevel
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=0)

        # ==== Layout starts ====

        # Donate image (clickable)
        try:
            image_path = self.resource_path(os.path.join("assets", "donate.png"))
            img = Image.open(image_path)
            width_img, height_img = img.size
            donate_img = ctk.CTkImage(
                light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(width_img, height_img)
            )
            donate_button = ctk.CTkLabel(top, image=donate_img, text="", cursor="hand2")
            donate_button.grid(row=0, column=0, columnspan=2, pady=(30, 20))
        except Exception:
            donate_button = ctk.CTkLabel(top, text="Support the Developer!", font=("Segoe UI", 16, "bold"))
            donate_button.grid(row=0, column=0, columnspan=2, pady=(30, 20))

        def open_link(event=None):
            webbrowser.open_new("http://www.coffeete.ir/Titan")

        donate_button.bind("<Button-1>", open_link)

        # USDT Label
        usdt_label = ctk.CTkLabel(top, text="USDT (Tether) – TRC20 Wallet Address :", font=("Segoe UI", 14, "bold"))
        usdt_label.grid(row=1, column=0, columnspan=2, pady=(30, 5), sticky="w", padx=20)

        # Entry field (readonly)
        wallet_address = "TGoKk5zD3BMSGbmzHnD19m9YLpH5ZP8nQe"
        wallet_entry = ctk.CTkEntry(top, width=300)
        wallet_entry.insert(0, wallet_address)
        wallet_entry.configure(state="readonly")
        wallet_entry.grid(row=2, column=0, padx=(20, 10), pady=5, sticky="ew")

        # Copy button
        copy_btn = ctk.CTkButton(top, text="Copy", width=80)
        copy_btn.grid(row=2, column=1, padx=(0, 20), pady=5, sticky="w")

        tooltip = None

        def copy_wallet():
            nonlocal tooltip
            self.clipboard_clear()
            self.clipboard_append(wallet_address)
            self.update()

            # Remove old tooltip if exists
            if tooltip:
                tooltip.hidetip()
                tooltip = None

            tooltip = Hovertip(copy_btn, "Copied to clipboard!")
            tooltip.showtip()

            # Hide after 2 seconds
            def hide_tip():
                if tooltip:
                    tooltip.hidetip()

            top.after(2000, hide_tip)

        copy_btn.configure(command=copy_wallet)

        top.after(200, top.deiconify)


if __name__ == "__main__":
    app = BatchFolderRenamer()
    app.mainloop()
