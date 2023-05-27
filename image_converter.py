from PIL import Image
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF library for PDF conversion
from tqdm import tqdm

def convert_image_format(input_path, output_path, output_format):
    if output_format == 'pdf':
        img = fitz.open(input_path)
        pdf_path = output_path.split('.')[0] + '.pdf'
        img.save(pdf_path)
        img.close()
    else:
        image = Image.open(input_path)
        rgb_image = image.convert('RGB')
        output_path = output_path.split('.')[0] + '.' + output_format
        rgb_image.save(output_path, format=output_format)

def open_input_file():
    file_path = filedialog.askopenfilename(filetypes=[('Image files', '*.heic;*.pdf;*.png;*.jpg;*.jpeg;*.gif')])
    entry_input_path.delete(0, tk.END)
    entry_input_path.insert(tk.END, file_path)

def open_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg;*.jpeg'), ('PDF', '*.pdf')])
    entry_output_path.delete(0, tk.END)
    entry_output_path.insert(tk.END, file_path)

def convert_image():
    input_path = entry_input_path.get()
    output_path = entry_output_path.get()
    output_format = dropdown_format.get()

    if input_path and output_path:
        if output_format != 'pdf':
            progress_bar = tqdm(total=100, unit='%', desc="Converting", ncols=60)
            convert_image_format(input_path, output_path, output_format)
            for i in range(100):
                progress_bar.update(1)
                progress_bar.set_postfix({'Progress': f'{i}%'})
                progress_bar.refresh()
            progress_bar.close()
            lbl_status.config(text="Image converted successfully!", fg="green")
            window.after(3000, reset_window_color)
        else:
            convert_image_format(input_path, output_path, output_format)
            lbl_status.config(text="Image converted successfully!", fg="green")
            window.after(3000, reset_window_color)
    else:
        lbl_status.config(text="Please select input and output paths.", fg="red")
        window.after(3000, reset_window_color)

def reset_window_color():
    window.configure(bg="SystemButtonFace")
    lbl_status.config(text="")

# GUI Setup
window = tk.Tk()
window.title("Image Converter")

lbl_input_path = tk.Label(window, text="Input Image Path:")
lbl_input_path.pack()

entry_input_path = tk.Entry(window, width=50)
entry_input_path.pack()

btn_open_input = tk.Button(window, text="Open", command=open_input_file)
btn_open_input.pack()

lbl_output_path = tk.Label(window, text="Output Image Path:")
lbl_output_path.pack()

entry_output_path = tk.Entry(window, width=50)
entry_output_path.pack()

btn_open_output = tk.Button(window, text="Save As", command=open_output_file)
btn_open_output.pack()

lbl_format = tk.Label(window, text="Output Format:")
lbl_format.pack()

dropdown_format = tk.StringVar(window)
dropdown_format.set("png")  # Default value

option_menu = tk.OptionMenu(window, dropdown_format, "png", "jpg", "jpeg", "pdf")
option_menu.pack()

btn_convert = tk.Button(window, text="Convert", command=convert_image)
btn_convert.pack()

lbl_status = tk.Label(window, text="")
lbl_status.pack()

window.mainloop()
