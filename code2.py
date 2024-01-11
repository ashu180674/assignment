import sys
import pandas as pd
from datetime import timedelta

def analyze_timecard(file_path):

    original_stdout = sys.stdout
    with open('output.txt', 'w') as f:
        sys.stdout = f
        df = pd.read_csv(file_path, parse_dates=['Time', 'Time Out'])
        df['Timecard Hours (as Time)'] = pd.to_timedelta(df['Timecard Hours (as Time)'] + ':00')

        #Employees who have worked for 7 consecutive days
        consecutive_days = 7
        consecutive_days_filter = df.groupby(['Employee Name', df['Time'].dt.date])['Time'].transform(lambda x: x.diff().dt.days == 1)
        employees_7_consecutive_days = df[consecutive_days_filter & ~consecutive_days_filter.isna()].groupby('Employee Name').filter(lambda x: len(x) >= consecutive_days)

        #Employees with less than 10 hours between shifts but greater than 1 hour
        time_between_shifts_filter = ((df['Time'] - df['Time Out'].shift(1)) < timedelta(hours=10)) & ((df['Time'] - df['Time Out'].shift(1)) > timedelta(hours=1))
        employees_less_than_10_hours = df[time_between_shifts_filter]

        #Employees who have worked for more than 14 hours in a single shift
        more_than_14_hours_filter = df['Timecard Hours (as Time)'] > timedelta(hours=14)
        employees_more_than_14_hours = df[more_than_14_hours_filter]

        # results
        print("Employees who have worked for 7 consecutive days:")
        print(employees_7_consecutive_days[['Employee Name', 'Position ID']].drop_duplicates())

        print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
        print(employees_less_than_10_hours[['Employee Name', 'Position ID']].drop_duplicates())

        print("\nEmployees who have worked for more than 14 hours in a single shift:")
        print(employees_more_than_14_hours[['Employee Name', 'Position ID']].drop_duplicates())


    sys.stdout = original_stdout
if __name__ == "__main__":
    file_path = "/home/ashu/Downloads/Assignment_Timecard.csv"
    analyze_timecard(file_path)
