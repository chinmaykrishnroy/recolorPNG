import os
from tkinter import Tk, Label, Button, filedialog, messagebox, StringVar, colorchooser
from tkinter.ttk import Progressbar
from PIL import Image
import webcolors

# Function to recolor PNG files in the input directory and save them in the output directory
def recolor_png(input_dir, output_dir, target_color):
    os.makedirs(output_dir, exist_ok=True)  # Create output folder if it doesn't exist

    # Convert RGB to hex for filename use
    hex_color = ''.join(f'{val:02x}' for val in target_color)

    png_files = [f for f in os.listdir(input_dir) if f.endswith(".png")]

    # Total number of files to process
    total_files = len(png_files)

    # Update the progress bar max value
    progress_bar["maximum"] = total_files

    for i, filename in enumerate(png_files):
        img_path = os.path.join(input_dir, filename)
        with Image.open(img_path).convert("RGBA") as img:
            recolored_img = Image.new("RGBA", img.size)

            for y in range(img.height):
                for x in range(img.width):
                    r, g, b, a = img.getpixel((x, y))
                    if a > 0:  # Only recolor non-transparent pixels
                        recolored_img.putpixel((x, y), (*target_color, a))
                    else:
                        recolored_img.putpixel((x, y), (r, g, b, a))

            # Create the new filename with the hex color code appended
            base_name, _ = os.path.splitext(filename)
            new_filename = f"{base_name}-{hex_color}.png"
            recolored_img.save(os.path.join(output_dir, new_filename))

        # Update progress bar
        progress_bar["value"] = i + 1
        root.update_idletasks()

    messagebox.showinfo("Success", f"Recolored images saved to {output_dir}")

# Function to open file dialog for input folder selection
def select_input_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        input_folder.set(folder_selected)

# Function to open file dialog for output folder selection
def select_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder.set(folder_selected)

# Function to start the conversion process
def start_conversion():
    input_dir = input_folder.get()
    output_dir = output_folder.get()

    if not input_dir:
        messagebox.showerror("Error", "Please select an input folder.")
        return

    # Default output folder to 'output' subfolder in the input directory if not selected
    if not output_dir:
        output_dir = os.path.join(input_dir, "output")

    # Target color (for example: white)
    target_color = webcolors.hex_to_rgb(color_hex.get())

    # Recolor PNG images
    recolor_png(input_dir, output_dir, target_color)

# Function to open the color picker and update the label's background and text color
def pick_color():
    color_code = colorchooser.askcolor(title="Choose Color")[1]
    if color_code:
        color_hex.set(color_code)
        update_color_label()

# Function to update the color label's background, border, and text color
def update_color_label():
    # Get RGB from the selected hex code
    target_color = webcolors.hex_to_rgb(color_hex.get())

    # Calculate the negative color (invert RGB values)
    negative_color = '#{:02x}{:02x}{:02x}'.format(255 - target_color[0], 255 - target_color[1], 255 - target_color[2])

    # Update label styles
    color_label.config(bg=color_hex.get(), fg=negative_color, bd=2, relief="solid")

# Create the main window
root = Tk()
root.title("PNG Recolor Tool")

# Variable to hold folder paths and color
input_folder = StringVar()
output_folder = StringVar()
color_hex = StringVar(value="#ffffff")  # Default to whitr

# Input folder selection
Label(root, text="Select Input Folder:").grid(row=0, column=0, padx=10, pady=5)
Button(root, text="Browse", command=select_input_folder).grid(row=0, column=2, padx=10, pady=5)
Label(root, textvariable=input_folder, wraplength=300).grid(row=0, column=1, padx=10, pady=5)

# Output folder selection
Label(root, text="Output Folder (optional):").grid(row=1, column=0, padx=10, pady=5)
Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=5)
Label(root, textvariable=output_folder, wraplength=300).grid(row=1, column=1, padx=10, pady=5)

# Color picker and label
Label(root, text="Target Color (Hex):").grid(row=2, column=0, padx=10, pady=5)
color_label = Label(root, textvariable=color_hex, width=20, relief="solid", bd=2)
color_label.grid(row=2, column=1, padx=10, pady=5)
Button(root, text="Pick Color", command=pick_color).grid(row=2, column=2, padx=10, pady=5)

# Convert button
Button(root, text="Convert", command=start_conversion).grid(row=3, column=1, padx=10, pady=20)

# Progress bar
progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Run the application
root.mainloop()
