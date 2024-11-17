# RGB Generator - Open Source Software
# D:\USAF\color-research\remote01\RGBGeneratorWVignett1.py
# This software is distributed under an open source license. You are permitted to use, modify, and distribute it, provided that
# proper credit is given to the original author. If you use this software, please include a reference to the creator of Vlads Test Target.
#
# Author: Creator of Vlads Test Target
#
# Note: The alpha channel is handled using a Pygame surface with an alpha channel. The alpha value ranges from 0 (fully transparent) to 255 (fully opaque),
# allowing for precise control over the transparency of the displayed color. The implementation involves clearing the Pygame screen using `color_screen.fill((0, 0, 0))` to reset it, followed by blitting the updated surface with `color_screen.blit(surface, (0, 0))` to apply the desired transparency level.
#
# Specification for Version 20:
# Detailed Requirements:
# 1. **Application Components**:
#    - **Alpha Channel Handling**: The alpha channel is managed using a Pygame surface with an alpha channel, allowing for transparency values ranging from 0 (fully transparent) to 255 (fully opaque). This is implemented by clearing the Pygame screen using `color_screen.fill((0, 0, 0))` to reset it, followed by blitting the updated surface with `color_screen.blit(surface, (0, 0))` to apply the desired transparency level.

import pygame
import tkinter as tk
#from tkinter import ttk
import datetime
import os
import math

import numpy as np

# Function to update the color on the projector screen
def update_color():
    global color_screen
    r = red_slider.get()
    g = green_slider.get()
    b = blue_slider.get()
    a = alpha_slider.get()
    
    # Update entry boxes with slider values
    red_value.set(r)
    green_value.set(g)
    blue_value.set(b)
    alpha_value.set(a)
    
    # Update the color and alpha value for the projector screen
    color = (r, g, b, a)
    (current_width, current_height)=color_screen.get_size()
    normalized_distances = precompute_distances(current_width, current_height)
    vignette_factor = vignette_slider.get() / 50  # Slider value from -50 to 50
    
    if vignette_factor > 0:
        brightness_modifier= 1 - vignette_factor * normalized_distances ** 2
    else:
        brightness_modifier= 1 + vignette_factor * (1 - normalized_distances ** 2)
        
    r_array = np.clip(r * brightness_modifier, 0, 255).astype(np.uint8)
    g_array = np.clip(g * brightness_modifier, 0, 255).astype(np.uint8)
    b_array = np.clip(b * brightness_modifier, 0, 255).astype(np.uint8)
    rgb_array = np.dstack((r_array, g_array, b_array))
    surface = pygame.surfarray.make_surface(rgb_array)
    # we need to add reading alpha from slider
    surface.set_alpha(int(a ))

    color_screen.fill((0, 0, 0))  # Clear screen
    color_screen.blit(surface, (0, 0))
    pygame.display.flip()

mem_width=-1
mem_height=-1
ndistances=None
def precompute_distances(width,height):
    global ndistances,mem_width,mem_height
    if width == mem_width and height == mem_height:
        return ndistances
    #print (f"Degug Precompute_distances {height} x{width} (height x width) ")
    mem_width=width
    mem_height=height
    center_x = width / 2
    center_y = height / 2
    y_coords, x_coords = np.meshgrid(np.arange(height), np.arange(width))
    distances = np.sqrt((x_coords - center_x) ** 2 + (y_coords - center_y) ** 2)
    max_distance = np.sqrt(center_x ** 2 + center_y ** 2)
    ndistances=distances / max_distance
    return ndistances

# Function to update sliders based on entry box changes
def update_slider_from_entry(entry, slider):
    try:
        value = int(entry.get())
        if 0 <= value <= 255:
            slider.set(value)
            update_color()
    except ValueError:
        pass

# Function to set the display size
def set_display_size(event):
    global screen, color_screen
    size = display_size_var.get()
    width, height = map(int, size.split('x'))
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME, display=1)
    color_screen = screen
    update_color()

# Function to increment or decrement slider values using buttons
def update_slider_from_button(slider, value_var, increment):
    try:
        value = int(value_var.get()) + increment
        if 0 <= value <= 255:
            slider.set(value)
            value_var.set(value)
            update_color()
    except ValueError:
        pass

# Function to save the current RGB values, user input, and timestamp to a log file
def save_log():
    r = red_slider.get()
    g = green_slider.get()
    b = blue_slider.get()
    a = alpha_slider.get()
    v = vignette_slider.get()
    user_text = user_input.get()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"{timestamp} - RGB: ({r}, {g}, {b}, Alpha: {a}, Vignette: {v}) - Note: {user_text}\n"
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry)

# Function to exit the application
def exit_app():
    root.destroy()
    pygame.quit()

# Initialize Pygame
pygame.init()

# Get the list of displays
num_displays = pygame.display.get_num_displays()
if num_displays < 2:
    raise RuntimeError("Two monitors are required for this setup.")

# Set up display on the second screen (projector)
screen = pygame.display.set_mode((1280, 720), pygame.NOFRAME, display=1)  # Set initial resolution to HD (1280x720)

# Fill screen with initial color
color_screen = screen
color_screen.fill((0, 0, 0))  # Initially black
pygame.display.flip()

# Set up the GUI with Tkinter to control the color on the projector screen
root = tk.Tk()
root.title("Color Control")
root.geometry("600x800")  # Increase panel size

# Add title with byline
title_label = tk.Label(root, text="RGB Generator from Vlads Test Target", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Get the full path to the log file
log_file_path = os.path.abspath("color_log.txt")

# Set up dropdown for display sizes
display_size_var = tk.StringVar(root)
display_size_var.set("1280x720")  # Default value
display_sizes = [
    "640x480",  # VGA
    "800x600",  # SVGA
    "1024x768",  # XGA
    "1280x720",  # HD
    "1280x1024",  # SXGA
    "1600x900",  # HD+
    "1920x1080",  # Full HD
    "2560x1440",  # QHD
    "3840x2160"   # UHD
]
display_size_menu = tk.OptionMenu(root, display_size_var, *display_sizes, command=set_display_size)
display_size_menu.pack()

# Set up sliders and entry boxes for RGB and alpha
red_value = tk.StringVar(value='130')
red_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Red", length=400, command=lambda x: update_color())
red_slider.set(130)
red_slider.pack()

red_frame = tk.Frame(root)
red_frame.pack()
red_minus_button = tk.Button(red_frame, text="-", command=lambda: update_slider_from_button(red_slider, red_value, -1))
red_minus_button.grid(row=0, column=0)
red_entry = tk.Entry(red_frame, textvariable=red_value, width=5)
red_entry.grid(row=0, column=1)
red_plus_button = tk.Button(red_frame, text="+", command=lambda: update_slider_from_button(red_slider, red_value, 1))
red_plus_button.grid(row=0, column=2)
red_entry.bind("<KeyRelease>", lambda event: update_slider_from_entry(red_entry, red_slider))

green_value = tk.StringVar(value='40')
green_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Green", length=400, command=lambda x: update_color())
green_slider.set(40)
green_slider.pack()
green_frame = tk.Frame(root)
green_frame.pack()
green_minus_button = tk.Button(green_frame, text="-", command=lambda: update_slider_from_button(green_slider, green_value, -1))
green_minus_button.grid(row=0, column=0)
green_entry = tk.Entry(green_frame, textvariable=green_value, width=5)
green_entry.grid(row=0, column=1)
green_plus_button = tk.Button(green_frame, text="+", command=lambda: update_slider_from_button(green_slider, green_value, 1))
green_plus_button.grid(row=0, column=2)
green_entry.bind("<KeyRelease>", lambda event: update_slider_from_entry(green_entry, green_slider))

blue_value = tk.StringVar(value='170')
blue_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Blue", length=400, command=lambda x: update_color())
blue_slider.set(170)
blue_slider.pack()
blue_frame = tk.Frame(root)
blue_frame.pack()
blue_minus_button = tk.Button(blue_frame, text="-", command=lambda: update_slider_from_button(blue_slider, blue_value, -1))
blue_minus_button.grid(row=0, column=0)
blue_entry = tk.Entry(blue_frame, textvariable=blue_value, width=5)
blue_entry.grid(row=0, column=1)
blue_plus_button = tk.Button(blue_frame, text="+", command=lambda: update_slider_from_button(blue_slider, blue_value, 1))
blue_plus_button.grid(row=0, column=2)
blue_entry.bind("<KeyRelease>", lambda event: update_slider_from_entry(blue_entry, blue_slider))

alpha_value = tk.StringVar(value='255')
alpha_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Alpha", length=400, command=lambda x: update_color())
alpha_slider.set(255)
alpha_slider.pack()

alpha_frame = tk.Frame(root)
alpha_frame.pack()
alpha_minus_button = tk.Button(alpha_frame, text="-", command=lambda: update_slider_from_button(alpha_slider, alpha_value, -1))
alpha_minus_button.grid(row=0, column=0)
alpha_entry = tk.Entry(alpha_frame, textvariable=alpha_value, width=5)
alpha_entry.grid(row=0, column=1)
alpha_plus_button = tk.Button(alpha_frame, text="+", command=lambda: update_slider_from_button(alpha_slider, alpha_value, 1))
alpha_plus_button.grid(row=0, column=2)
alpha_entry.bind("<KeyRelease>", lambda event: update_slider_from_entry(alpha_entry, alpha_slider))
# new alpha




# Create vignette slider for vignetting control
vignette_value = tk.StringVar(value='0')
vignette_slider = tk.Scale(root, from_=-50, to=50, orient='horizontal', label='Vignette', length=400,command=lambda x: update_color())
vignette_slider.set(0)
vignette_slider.pack(pady=10)



# Add text input field for user notes
user_input_label = tk.Label(root, text="User Notes:")
user_input_label.pack()

user_input = tk.Entry(root, width=50)
user_input.pack()

# Show log file path (read-only)
log_path_label = tk.Entry(root, width=70)
log_path_label.insert(0, f"Log File Path: {log_file_path}")
log_path_label.config(state="readonly")
log_path_label.pack(pady=2)


# Add save button
save_button = tk.Button(root, text="Save to Log", command=save_log)
save_button.pack(pady=10)

# Add exit button
exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack(pady=20)

# Run the Tkinter main loop in a separate thread to allow the Pygame display to remain active
root.mainloop()
pygame.quit()