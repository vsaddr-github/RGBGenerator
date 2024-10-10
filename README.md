# RGB Generator

Creates RGB output on second screen or video projector

## Overview
The RGB Generator is an application designed to control RGB color outputs using a dual monitor setup. The primary screen is used to adjust settings, while the secondary screen, typically connected to a projector, displays the selected color. The application is built using Pygame and Tkinter for controlling colors and GUI interaction respectively.

## Features
- **Dual Monitor Setup**: Control color on a secondary screen while adjusting settings on the primary screen.
- **Real-time RGB and Alpha Control**: Adjust Red, Green, Blue, and Alpha (transparency) values via sliders, manual buttons, or direct input fields.
- **User Notes and Logging**: Save RGB values, Alpha, and user notes along with timestamps to a log file.
- **Custom Screen Resolution**: Change the resolution of the display on the secondary screen.

## License
This software is open source and distributed under an open source license. You are permitted to use, modify, and distribute the application, provided that proper credit is given to the original author. The software must include a reference to the creator of Vlads Test Target.

## Installation Guide for Windows

### Step 1: Install Python
1. Go to the [Python Downloads page](https://www.python.org/downloads/).
2. Download the latest stable version of Python for Windows.
3. Run the downloaded installer.
   - Make sure to select **"Add Python to PATH"** during the installation process.

### Step 2: Install Required Packages
After installing Python, you need to install the necessary libraries. Open a Command Prompt and run the following commands:

```bash
pip install pygame
pip install tkinter
```

> Note: `tkinter` is usually included with Python by default, but this command ensures it is available.

### Step 3: Download the RGB Generator Application
1. Obtain the script file (`RGB_Generator.py`) provided by the author.
2. Save it in a location that you can easily access.

### Step 4: Connect Your Monitors
Ensure that you have two monitors connected to your system. The second monitor should ideally be a projector for best results.

### Step 5: Run the Application
1. Open a Command Prompt.
2. Navigate to the directory where you saved the `RGB_Generator.py` file.
3. Run the following command to start the application:

```bash
python RGB_Generator.py
```

## User Guide

### Control Panel
- The main control panel will open on your primary monitor, providing sliders and buttons to control the RGB values and transparency of the color on your second monitor.
- **Adjusting Colors**: Use the sliders to adjust the **Red**, **Green**, **Blue**, and **Alpha** values.
- **Manual Controls**: You can also use the `+` and `-` buttons next to each color field for fine adjustments.
- **Entry Fields**: If precise values are required, manually enter them in the respective fields.

### Screen Size Adjustment
- Use the dropdown menu to change the screen resolution for the projector display.

### Saving Configurations
- Use the **Save to Log** button to save the current RGB, Alpha, and any notes you've added. This is helpful for documenting color settings.

### Exit
- Use the **Exit** button on the control panel to cleanly close both the GUI and the projector display.

## Contributing
Feel free to fork this repository and make any changes or improvements to the RGB Generator. Pull requests are always welcome.

## Contact
If you have any questions or encounter any issues, please contact the creator of Vlads Test Target.

## License
This project is licensed under the open source license - see the LICENSE file for details.

---

This README file provides the essential information to get started with the RGB Generator, including setup, running the application, and usage guidelines. Let me know if there are any additional details you would like to include!
