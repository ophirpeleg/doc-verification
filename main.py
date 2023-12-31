import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def process_csv(input_file, output_file, required_columns, length_check_column, null_check_column):
    try:
        print("Loading CSV file:", input_file)
        # Load the CSV file
        df = pd.read_csv(input_file)
        print("CSV file loaded successfully.")

        # Check for missing columns
        print("Checking for required columns...")
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print("Missing columns found:", missing_columns)
            messagebox.showerror("Error", f"Missing columns: {missing_columns}")
            return
        print("Required columns are present.")

        # Length check
        print(f"Checking length of values in column: {length_check_column}")
        df['length_check'] = df[length_check_column].apply(lambda x: len(str(x)) > 80)

        # Null check
        print(f"Checking for null values in column: {null_check_column}")
        df['null_check'] = df[null_check_column].isnull()

        # Feedback column
        print("Creating feedback column...")
        def create_feedback(row):
            feedback = []
            if row['length_check']:
                feedback.append('Name Length is more then 80 chars')
            if row['null_check']:
                feedback.append('Null value found')
            return ', '.join(feedback)

        df['feedback'] = df.apply(create_feedback, axis=1)
        df.drop(['length_check', 'null_check'], axis=1, inplace=True)

        # Save to new CSV
        print("Saving processed data to:", output_file)
        df.to_csv(output_file, index=False)
        print("CSV file processed and saved successfully.")
        messagebox.showinfo("Success", "CSV file processed and saved successfully.")
    except Exception as e:
        print("Error:", str(e))
        messagebox.showerror("Error", str(e))

def open_file():
    print("Opening file dialog for CSV selection...")
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        print("CSV file selected:", file_path)
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            print("Save path chosen:", save_path)
            # Define your required columns, length check column, and null check column here
            required_columns = ['Row', 'Document Name']  # Update as per your requirements
            length_check_column = 'Document Name'  # Update as per your requirements
            null_check_column = 'Revision Number'  # Update as per your requirements
            process_csv(file_path, save_path, required_columns, length_check_column, null_check_column)
    else:
        print("File selection cancelled.")

root = tk.Tk()
root.title("CSV File Processor")

open_button = tk.Button(root, text="Open CSV File", command=open_file)
open_button.pack(pady=20)

print("Starting GUI application...")
root.mainloop()
