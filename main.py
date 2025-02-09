import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CSVConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Converter")
        self.root.geometry("450x150")

        # Label to show selected file
        self.file_label = tk.Label(root, text="No file selected", font=("Arial", 12))
        self.file_label.pack(pady=10)

        # Browse button
        self.browse_button = ttk.Button(root, text="Browse", command=self.open_file)
        self.browse_button.pack(pady=10)

        # Convert button
        self.convert_button = ttk.Button(root, text="Convert", command=self.convert_csv, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        self.input_file = ""

    def open_file(self):
        file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file:
            self.input_file = file
            self.file_label.config(text=f"{file}")
            self.convert_button.config(state=tk.NORMAL)

    def convert_csv(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return

        output_file = self.input_file.replace(".csv", "_converted.csv")
        
        df = pd.read_csv(self.input_file)
        
        required_columns = ["EmpNo", "ALOutstanding", "SKBalance"]
        if not all(col in df.columns for col in required_columns):
            messagebox.showerror("Error", "Missing required columns in CSV file.")
            return

        # Process the data
        col1_data = df["EmpNo"]
        col2_data = df["ALOutstanding"]
        col2_append_data = df["SKBalance"]

        col1_combined = pd.concat([col1_data, col1_data], ignore_index=True)
        col2_combined = pd.concat([col2_data, col2_append_data], ignore_index=True)
        ann_sick_labels = ["ANN"] * len(col2_data) + ["SICK"] * len(col2_append_data)

        new_df = pd.DataFrame({0: col1_combined, 1: col2_combined, 2: ann_sick_labels})
        new_df.to_csv(output_file, index=False, header=False)

        messagebox.showinfo("Success", f"Converted file saved as {output_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVConverterApp(root)
    root.mainloop()
