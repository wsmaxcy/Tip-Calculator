# Tip Calculator - Hourly and Points

## Overview
This program is a tip calculator that allows you to split tips among hourly workers or workers with assigned points. There are two versions of the program: `Tip-Calc-Hourly.py` and `Tip-Calc-Points.py`. The program is built using the custom `customtkinter` library for graphical user interface and also uses the `googleapiclient` library for exporting data to Google Sheets.

## Features
- Enter the name of the person who will be splitting the tips.
- Enter the total tips received.
- Add and remove workers who will receive tips.
- For `Tip-Calc-Hourly.py`, enter the number of hours and minutes worked by each worker to calculate their tipout.
- For `Tip-Calc-Points.py`, assign points to each worker to determine their tipout proportion.
- Calculate the tipout for each worker and view the tip percentage.
- Export the tip information to a Google Sheet.

## Instructions
1. Clone or download the project to your local machine.
2. Install the required libraries using the following commands in the Tip-Calculator folder:

`pip intsall -r requirements.txt`

3. Obtain a Google Sheets API service account credentials file and replace the path to the `creds.json` file in the program.
4. Replace the `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` with your actual Google Sheet ID in the `add_rows_to_sheet` function.
5. Run either `Tip-Calc-Hourly.py` or `Tip-Calc-Points.py` to launch the respective tip calculator.

## How to Use
### Tip-Calc-Hourly.py
1. Enter the name of the person who will be splitting the tips.
2. Enter the total tips received.
3. Click on the "Add Worker" button to add a worker who will receive tips.
4. For each worker, enter their name, hours, and minutes worked.
5. Click on the "Calculate Tipout" button to calculate the tipout for each worker based on their working hours.
6. Click on the "Export" button to export the tip information to a Google Sheet.
7. The program will display a message box confirming the export. Click "Okay" to close the program.

### Tip-Calc-Points.py
1. Enter the name of the person who will be splitting the tips.
2. Enter the total tips received.
3. Click on the "Add Worker" button to add a worker who will receive tips.
4. For each worker, enter their name, position, and points assigned.
5. Click on the "Calculate Tipout" button to calculate the tipout for each worker based on their assigned points.
6. Click on the "Export" button to export the tip information to a Google Sheet.
7. The program will display a message box confirming the export. Click "Okay" to close the program.

## Note
- If any required field is left empty, an error message will be displayed, and the operation will be aborted.
- Make sure to fill in all the necessary information before clicking the "Calculate Tipout" and "Export" buttons.
- The `customtkinter` library is used to create a customized appearance for the GUI. You can modify the appearance by changing the theme and color settings in the code.

Feel free to use and customize this tip calculator according to your needs! Happy tipping!
