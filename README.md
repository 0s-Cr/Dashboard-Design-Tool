# Dashboard Design Tool
This project was designed to develop and test a custom dashboard for York Formula Student.

## Requirements
Python 3.10.11
- Tkinter
- Thread
- Math
- os
- ast

Python-can 4.3.1

## Instructions
To run the program run the dash_designer.py file.\
Creating a new file will open a new empty development window. \
Click on a shape in the left had sidebar to add it to the main area.\
Holding Lshift and dragging a shape will resize it.\
Pressing Lcontrol and clicking will open a shape config window.\
Save the file (files save as .txt) and click Simulate in the file menu.\
Use controls on the left hand side to interract with the dashboard created.

## Known Issues
- Saving sometimes doesn't detect updated shape values from config window unless shape is dragged
- Threads from the simulation window don't terminate properly in some occasions
