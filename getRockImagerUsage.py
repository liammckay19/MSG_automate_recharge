import pandas as pd
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename

class UserException(Exception):
    pass

def main():
    # Read from RockImager's usage log file
    while True:
        try:
            filename = askopenfilename(initialdir = 'C:/Users/ljiang/Google Drive/UCSF_XTAL/MSG_recharge_automation/rockImagerLogs',
                title = "Select rockImagerUsage file (.csv or .tsv only)")
            path = filename #change to file name

            if not(filename): # empty file name occurs when user tries to close input window
                raise SystemExit()
            elif filename.endswith('.tsv'):
                df = pd.read_csv(path, delimiter="\t")
                break
            elif filename.endswith('.txt'):
                df = pd.read_csv(path, delimiter="\t")
                break
            elif filename.endswith('.csv'):
                df = pd.read_csv(path, delimiter=",")
                break
            else:
                raise UserException
        except UserException as e:    
            print('\nWrong file type selected (ONLY .csv or .tsv files)')

    # MAIN SCRIPT BELOW
    print("\nRunning script on:\n" + filename +"\n")


    # Remove "groups" not in recharge system (administrators, etc.)
    df = df[df['Group'] != 'Administrators']
    # Look at 'Duration' column and extract numerical data inplace
    durStr = 'Dur (min)'
    df.rename(columns={'Duration':durStr}, inplace=True)
    df[durStr] = df[durStr].str.replace(r'[^0-9.]','', regex=True).astype('float')

    # Look at 'Time' column and convert to datetime type
    df.index = pd.to_datetime(df.pop('Time')) # Change index to datetime index

    # Group by PIs and aggregate total duration
    groupedByPI = df.groupby('Group')
    usageByPI = groupedByPI.sum()[durStr] #in minutes
    usageSum = usageByPI.sum()
    # print(100*usageByPI/usageSum) #percent usage 

    # Create pie chart of usage (min) by PI group -- too crowded, need to reformat...
    # labels = usageByPI.index
    # usageByPI.plot.pie(figsize=(6, 6), labels=labels, autopct='%1.0f%%')
    # plt.show()
    usageByMonthByPI = df.groupby([pd.Grouper(freq="M"),'Group']).sum()
    usageByYearByPI = df.groupby([df.index.year,'Group']).sum()
    # usageByMonthByPI.xs('Minor', level = 1)

    return df