import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
from ics import Calendar, Event

print("Welcome to the Test Planner Generator \nMade by Aryan")
current_datetime2 = datetime.now()
current_datetime = current_datetime2.strftime("%Y-%m-%d %H:%M:%S")
print("Current date and time:", current_datetime, "\n----------------------------------------------------------\n")

def getExamDate():
    exam_date_str = input("Enter the exam date (Please use DD-MM, DD-MM-YYYY, or YYYY-MM-DD.): ")
    try:
        if len(exam_date_str) == 5:  # Format DD-MM
            exam_date = datetime.strptime(exam_date_str, "%d-%m")
            # Set the year to the current year
            exam_date = exam_date.replace(year=datetime.now().year)
        elif len(exam_date_str) == 10 and exam_date_str[2] == '-':  # Format DD-MM-YYYY
            exam_date = datetime.strptime(exam_date_str, "%d-%m-%Y")
        elif len(exam_date_str) == 10 and exam_date_str[4] == '-':  # Format YYYY-MM-DD
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
        else:
            raise ValueError("Invalid format")
        
        #print("Exam date:", exam_date)

    except ValueError:
        print("Invalid date format! Please use DD-MM, DD-MM-YYYY, or YYYY-MM-DD.")
    return exam_date

def getOtherDate():
    exam_date_strr = input("Enter the starting date (Please use DD-MM, DD-MM-YYYY, or YYYY-MM-DD.): ")
    try:
        if len(exam_date_strr) == 5:  # Format DD-MM
            other_date = datetime.strptime(exam_date_strr, "%d-%m")
            # Set the year to the current year
            other_date = other_date.replace(year=datetime.now().year)
        elif len(exam_date_strr) == 10 and exam_date_strr[2] == '-':  # Format DD-MM-YYYY
            other_date = datetime.strptime(exam_date_strr, "%d-%m-%Y")
        elif len(exam_date_strr) == 10 and exam_date_strr[4] == '-':  # Format YYYY-MM-DD
            other_date = datetime.strptime(exam_date_strr, "%Y-%m-%d")
        else:
            raise ValueError("Invalid format")
        
        #print("Exam date:", exam_date)

    except ValueError:
        print("Invalid date format! Please use DD-MM, DD-MM-YYYY, or YYYY-MM-DD.")
    return other_date

def difference():    
    exam_date = getExamDate()
    differenceExamTodayDate = exam_date - current_datetime2  
        #print(differenceExamTodayDate, type(differenceExamTodayDate.days))
    return differenceExamTodayDate, exam_date    

differenceExam_today_forcalc, exam_date = difference()

#print(differenceExam_today_forcalc.days)

while differenceExam_today_forcalc.days < 0:
    print("That's in the past!\n")
    differenceExam_today_forcalc, exam_date = difference()

print("Today's date is: ", current_datetime, "\nTest Date is ", exam_date.strftime("%Y-%m-%d"), "\nYou have", differenceExam_today_forcalc.days, "days to study until the test\n" )

response = input("Is this correct Y/N: ")

if response.lower() != "y":
    mayb_other_date = input("Do you want another date as starting date? (Y/N): ")
    if mayb_other_date.lower() == 'y':
        current_datetime2 = getOtherDate()
        current_datetime = current_datetime2.strftime("%Y-%m-%d %H:%M:%S")
        differenceExam_today_forcalc = exam_date - current_datetime2 
        print("Today's date is: ", current_datetime, "\nTest Date is ", exam_date.strftime("%Y-%m-%d"), "\nYou have", differenceExam_today_forcalc.days, "days to study until the test\n" )       #TODO: better solution now you can have negraitviwe differenceexam today forcalc and you cant y/n twice 
    else:    
        quit()

print("\nWonderful! Now please provide the Subject(code), what you want to divide the deadlines in, and the amount of divisions\nE.g. If you want to study FoCs, have 1 deadline for each of the 8 Lectures, write: FoCs, Lectures, 8")
print("\nAnother example: You need to have to study week 5, 6, 7, 8 of EssoCS, write (EssoCS, Week, 4), you'll get the option later to make the events in calendar start from week 5 instead of 1.")

user_input_subj_div_no = input("Enter Subject(code), division type, and number of divisions (e.g., FoCs, Lecture, 8): ")

try:
    subj, divtype, num_div_study = [plan.strip() for plan in user_input_subj_div_no.split(',')]
    num_div_study = int(num_div_study)
    print("\nSubject:", subj)
    print("Divide by:", divtype)
    print("In", num_div_study, "sessions\n\n")
except ValueError:
     print("Invalid format! Please enter in the format: Subject, Division Type, Number of Divisions.")

while True:
    try:
        begin_study_from = int(input(f"From which {divtype} would you like to begin? (If it's from the start, enter 1): "))
        break  # Exit the loop if the input is a valid integer
    except ValueError:
        print("Invalid input! Please enter a number.")


space_within_deadlines = differenceExam_today_forcalc.days // num_div_study

print("You have", space_within_deadlines, "days within each deadline")

optional_metadata_user_req = "Would you like to provide your email-address or a custom description? Y/N: "

user_extra_metadata_ask_flag = input(optional_metadata_user_req)

if user_extra_metadata_ask_flag.lower() == 'y':
    user_email = input("Provide Email-Address: ")
    custom_desc = input("Provide custom description for all events: \n")
else:
    user_email = ""
    custom_desc = ""     

                                                                                                    #TODO: add per event descriptions

current_event_date = current_datetime2

planned_days = [] 

for i in range(num_div_study):
    event_name = f"{subj} {divtype} {i + begin_study_from}"
    current_event_date += timedelta(days=space_within_deadlines)

    event = {
        "name": event_name,
        "date": current_event_date
    }

    planned_days.append(event) # each planned_day contains disctionary with event detail


calander = Calendar()

for i, event in enumerate(planned_days): #the enumerate gives tuples with index,event_dictionary, elke tuple nomeen we event, and the for-loop iterate over elke event met i
    calendar_event = Event()

    calendar_event.name = event["name"]
    calendar_event.begin = event["date"]
    calendar_event.duration = timedelta(hours=1)

    calendar_event.uid = f"{event['date'].strftime('%Y%m%dT%H%M%SZ')}-{i}-{user_email}"  # Unique identifier
    calendar_event.description = f"Study {event['name']}\n\n{custom_desc}"

    calander.events.add(calendar_event)

string_all_events_check = "\n"

print("Here are the event deadlines + dates: ")

for i, event in enumerate(planned_days):
    string_all_events_check += f"{event['name']}: {event['date'].strftime('%Y-%m-%d')}\n"

print(string_all_events_check)

quitflag = 0    

response2 = input("Would you like to save this to an .ics file Y/N: ")
if response2.lower() != "y":
    quit()
else: 
            # Initialize tkinter (needed to use file dialog)
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Open a "Save As" dialog box
    file_path = filedialog.asksaveasfilename(defaultextension=".ics", 
                                            filetypes=[("iCalendar files", "*.ics")], 
                                            title="Save the Calendar File")

    # Check if a file path was selected
    if file_path:
        # Write the calendar to the chosen file path
        with open(file_path, "w") as f:
            f.writelines(calander)
        print(f"Calendar saved to {file_path}")
        quitflag = 1
    else:
        print("Save operation was canceled.")
        result3 = input("Would you like to try again? Y/N: ")
        if result3.lower() != "y":
            quitflag = 1
         




def saveICS():
            # Initialize tkinter (needed to use file dialog)
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Open a "Save As" dialog box
    file_path = filedialog.asksaveasfilename(defaultextension=".ics", 
                                            filetypes=[("iCalendar files", "*.ics")], 
                                            title="Save the Calendar File")

    # Check if a file path was selected
    if file_path:
        # Write the calendar to the chosen file path
        with open(file_path, "w") as f:
            f.writelines(calander)
        print(f"Calendar saved to {file_path}")
        quitflag = 1
    else:
        print("Save operation was canceled.")
        result3 = input("Would you like to try again? Y/N: ")
        if result3.lower() != "y":
            quitflag = 1  

  
while quitflag != 1:
    saveICS()
          

if quitflag == 1:
    quit()