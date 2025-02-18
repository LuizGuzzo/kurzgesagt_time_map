# Kurz Event Time Map

**Kurz Event Time Map** is a Python script designed to help you visualize and map important events in your life on a lifespan timeline. This project was created for a personal project using the Lifespan Timeline Poster from [Kurzgesagt's Shop](https://shop-us.kurzgesagt.org/products/lifespan-timeline-poster). The idea is to place magnets on the poster that correspond to the dates of your life events, making your personal timeline both visually striking and meaningful.

## Overview

The script calculates your age at the time of each event based on your date of birth (hardcoded as **03/05/1997**, my anniversary) and positions markers on a timeline spanning 100 years (0 to 99). The timeline is displayed using Python’s Tkinter library with the following features:

- **Horizontal Lines:** Each year of life is represented by a horizontal line, with numbering on both the left and right sides.
- **Zigzag Connections:** The lines are connected in a zigzag fashion (even-numbered lines connect to the right edge, odd-numbered lines to the left).
- **Event Markers:** A red marker indicates where an event occurred, along with annotations above showing the distances (in "real" centimeters) from the left and right edges.
- **Scale Markers:** Vertical markers indicate physical scales of 30 cm, 15 cm, and 7.5 cm using different dash styles.
- **Zoom & Resize:** You can zoom in and out with your mouse scroll, and the timeline adapts to window resizing.
- **Dual Modes:**
  - *Interactive Mode:* Input a single event date via the console.
  - *File Mode:* Read multiple events from a text file (`events_data.txt`) formatted as `dd/mm/yyyy - Event Name`.

## Features

- **Interactive Timeline:** Visualize a 100-year timeline with yearly markers.
- **Zigzag Design:** Enjoy a creative zigzag connection between the years.
- **Accurate Event Placement:** Mark events precisely based on calculated age.
- **Scale Representation:** Vertical markers at 30 cm (major ticks), 15 cm (medium ticks), and 7.5 cm (minor ticks) help maintain a real-world scale.
- **Zoom Functionality:** Adjust the view using the mouse scroll for detailed inspection.
- **Easy Data Input:** Use either single-event console input or a batch file (`events_data.txt`) for multiple events.
- **Physical Display Integration:** This project was designed specifically for mapping events on a Kurzgesagt Lifespan Timeline Poster, where each marker corresponds to a real-life event position, and magnets are used to represent these events.

## Requirements

- Python 3.x  
- Tkinter (usually included with Python)

## Usage

### Interactive Mode (Single Event)

1. Run the script without any arguments:
```bash
python kurz_event_time_map.py
```
2. When prompted, enter the event date in the format:
```bash
dd/mm/yyyy
```
3. A window will open displaying your timeline with the event marker and distance annotations.

### File Mode (Multiple Events)

1. Create or edit the `events_data.txt` file in the same directory as the script. Each line should follow this format:
```bash
18/02/2025 - Event Name
20/03/2025 - Another Event
```
2. Run the script with the file name as an argument:
```bash
python kurz_event_time_map.py events_data.txt
```
3. The script will read and plot all events from the file, showing each event’s marker, the distances above it, and the event name below.

## Repository Structure

- **kurz_event_time_map.py**: The main Python script that generates the timeline.
- **events_data.txt**: An example text file containing event data for testing.

## Customization and Future Improvements

- Customize colors, line spacing, and marker styles.
- Add functionality to export the timeline as an image.
- Enhance the interface for easier event input and configuration.

## About

This project was inspired by the Lifespan Timeline Poster available at [Kurzgesagt's Shop](https://shop-us.kurzgesagt.org/products/lifespan-timeline-poster). The script is designed to help map significant life events using magnets on the poster, creating a visual representation of your life journey.

## Contributions

Contributions, suggestions, and improvements are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
