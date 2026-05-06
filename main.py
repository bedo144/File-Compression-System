import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import matplotlib.pyplot as plt

# =====================================================
# Multimedia Compression Toolkit (Final Version)
# File/Text Input + Compression + Graph + Save File
# =====================================================

# -----------------------------
# Compression Simulations (Educational)
# -----------------------------

def lzw(data): return max(1, len(data)//2)

def arithmetic(data): return max(1, int(len(data)*0.6))

def huffman(data): return max(1, int(len(data)*0.5))

def shannon_fano(data): return max(1, int(len(data)*0.55))

def rle(data): return max(1, int(len(data)*0.4))

# -----------------------------
# GUI Application
# -----------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Multimedia Compression Toolkit")
        self.root.geometry("900x650")
        self.root.configure(bg="#0f172a")

        self.file_path = None
        self.data = ""
        self.compressed_data = ""

        self.mode = tk.StringVar(value="file")

        # HEADER
        tk.Label(root, text="Multimedia Compression Toolkit",
                 bg="#0f172a", fg="white",
                 font=("Arial", 18, "bold")).pack(pady=10)

        # MODE SELECTION
        mode_frame = tk.Frame(root, bg="#0f172a")
        mode_frame.pack(pady=10)

        tk.Radiobutton(mode_frame, text="File",
                       variable=self.mode, value="file",
                       command=self.switch_mode,
                       bg="#0f172a", fg="white",
                       selectcolor="#1e293b").pack(side="left", padx=10)

        tk.Radiobutton(mode_frame, text="Text",
                       variable=self.mode, value="text",
                       command=self.switch_mode,
                       bg="#0f172a", fg="white",
                       selectcolor="#1e293b").pack(side="left", padx=10)

        # FILE FRAME
        self.file_frame = tk.Frame(root, bg="#111827")

        self.upload_btn = tk.Button(self.file_frame,
                                    text="Upload File",
                                    bg="#3b82f6", fg="white",
                                    command=self.upload)
        self.upload_btn.pack(side="left", padx=10)

        self.file_label = tk.Label(self.file_frame,
                                    text="No file selected",
                                    bg="#111827", fg="gray")
        self.file_label.pack(side="left")

        # TEXT FRAME
        self.text_frame = tk.Frame(root, bg="#111827")

        self.text_area = tk.Text(self.text_frame, height=6, width=80)
        self.text_area.pack(padx=10, pady=10)

        # ALGORITHM SELECT
        self.combo = ttk.Combobox(root,
            values=["LZW","Arithmetic","Huffman","Shannon-Fano","RLE"],
            width=40)
        self.combo.set("Choose compression method")
        self.combo.pack(pady=10)

        # RUN BUTTON
        tk.Button(root, text="Run Compression",
                  bg="#10b981", fg="white",
                  font=("Arial", 12, "bold"),
                  command=self.run).pack(pady=10)

        # SAVE BUTTON
        tk.Button(root, text="Save Compressed File",
                  bg="#f59e0b", fg="black",
                  command=self.save_file).pack(pady=5)

        # GRAPH BUTTON
        tk.Button(root, text="Show Compression Graph",
                  bg="#8b5cf6", fg="white",
                  command=self.show_graph).pack(pady=5)

        # RESULT
        self.result = tk.Label(root,
                               text="Results will appear here",
                               bg="#0f172a", fg="#fbbf24",
                               font=("Arial", 12, "bold"))
        self.result.pack(pady=15)

        self.switch_mode()

    # -----------------------------
    def switch_mode(self):
        if self.mode.get() == "file":
            self.text_frame.pack_forget()
            self.file_frame.pack(pady=10)
        else:
            self.file_frame.pack_forget()
            self.text_frame.pack(pady=10)

    # -----------------------------
    def upload(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
                self.data = f.read()
            self.file_label.config(text=os.path.basename(self.file_path))

    # -----------------------------
    def run(self):
        if self.mode.get() == "file":
            if not self.file_path:
                messagebox.showerror("Error", "Upload file first")
                return
        else:
            self.data = self.text_area.get("1.0", tk.END).strip()
            if not self.data:
                messagebox.showerror("Error", "Enter text first")
                return

        size = len(self.data)
        method = self.combo.get()

        if method == "LZW": new_size = lzw(self.data)
        elif method == "Arithmetic": new_size = arithmetic(self.data)
        elif method == "Huffman": new_size = huffman(self.data)
        elif method == "Shannon-Fano": new_size = shannon_fano(self.data)
        elif method == "RLE": new_size = rle(self.data)
        else:
            messagebox.showerror("Error", "Select method")
            return

        ratio = size / new_size if new_size else 0

        # store compressed result (simulated)
        self.compressed_data = f"Compressed Data Simulation\nOriginal Size: {size}\nCompressed Size: {new_size}\nRatio: {ratio:.2f}"

        self.result.config(text=f"Original: {size} | Compressed: {new_size} | Ratio: {ratio:.2f}")

    # -----------------------------
    def save_file(self):
        if not self.compressed_data:
            messagebox.showerror("Error", "Run compression first")
            return

        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files","*.txt")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.compressed_data)
            messagebox.showinfo("Saved", "Compressed file saved successfully")

    # -----------------------------
    def show_graph(self):
        if not hasattr(self, "compressed_data"):
            messagebox.showerror("Error", "Run compression first")
            return

        original = int(self.compressed_data.split("Original Size: ")[1].split("\n")[0])
        compressed = int(self.compressed_data.split("Compressed Size: ")[1].split("\n")[0])

        plt.bar(["Original", "Compressed"], [original, compressed])
        plt.title("Compression Ratio")
        plt.ylabel("Size")
        plt.show()

# -----------------------------
root = tk.Tk()
App(root)
root.mainloop()
