# Expense Tracker

An **Expense Tracker** application that allows users to track income and expenses, visualize financial data, and manage records. This application features a graphical user interface (GUI) built with `ttkbootstrap` and uses `SQLite` for database storage. Additional libraries are utilized for data import/export and visualization.

## Features

- **Add and manage income/expense entries**: Track various categories of income and expenses with dynamic fields for ease of use.
- **Data Storage**: Store entries in a local SQLite database for easy data retrieval and analysis.
- **Data Visualization**: Generate graphical representations of your expenses and income.
- **Export Options**: Export your data to CSV or Excel files for external use.
- **Notifications and Dialogs**: Utilize toast notifications and message dialogs for enhanced user experience.

## Requirements

- Python 3.x
- Libraries: Install the following Python libraries, which can be installed via `pip`.

  ```bash
  pip install ttkbootstrap sqlite3 csv openpyxl matplotlib
  ```

## Installation

1. Clone this repository or download the code.
2. Ensure all the required libraries are installed.
3. Run the `code.py` file to launch the application.

   ```bash
   python code.py
   ```

## Usage

1. **Launch the Application**: Upon launching, the main GUI will load, displaying options for entering income and expenses.
2. **Manage Entries**: Use dynamic fields to input categories, amounts, and dates for each transaction.
3. **View and Analyze Data**: Visualize income vs. expenses over time.
4. **Export Data**: Export records in CSV or Excel format for external analysis.

## Database Structure

The application stores data in a local SQLite database located in the user's Documents folder. This setup allows for persistent storage across sessions.
