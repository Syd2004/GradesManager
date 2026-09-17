import json

students = {}
grade_thresholds = [
  (90, "A"),
  (80, "B"),
  (65, "C"),
  (50, "D"),
  (0, "F")
]

# Save the students to the student.json file
def save_students():
  print("Saving students...")
  with open("students.json", "w") as f:
    json.dump(students, f)
  print("Students saved.")

# Load the students in students.json into the students dict
# Creates new file if students.json is not found
# If there's an error in students.json (we get a JSONDecodeError), the program creates a new empty file
def load_students():
  global students
  try:
    with open("students.json", "r") as f:
      students = json.load(f)
  except FileNotFoundError:
    print("Save file not found. Creating new file...")
    save_students()
    print("File created.")
  except json.JSONDecodeError:
    print("Save file corrupted. Creating new file...")
    save_students()
    print("File created.")

# Checks if the mark is categorized as a 'Pass' (50+) or 'Fail' (<50)
def check_pass(n):
  return "Pass" if n >= 50 else "Fail"

# Sorts the grade thresholds list and checks the mark to return the grade
def get_grade(n):
  sorted_thresholds = sorted(grade_thresholds, key = lambda g: g[0], reverse = True)
  return next(grade for (threshold, grade) in sorted_thresholds if n >= threshold)

# Used when an average is needed for a student in the students dict
def get_average(key):
  return sum(students[key]) / len(students[key])

# Checks whether a name is valid. Doesn't allow empty names. Only alphabet characters, spaces and hyphens allowed. Returns a bool
def validate_name(name):
  if name.strip() == "":
    print("Name cannot be empty.")
    return False
  
  invalid = []

  for c in name.lower():
    if c not in "abcdefghijklmnopqrstuvwxyz- ":
      invalid.append(c)
  if len(invalid) != 0:
    print(f"'{invalid[0]}' is not a valid character for a name. \nOnly alphabet characters, spaces and hyphens.")
    return False
  else:
    return True

# Displays all the students saved or a message for when there's no student record.
def view_students():
  if len(students) == 0:
    print("There aren't any students in the system at the moment. Try adding one.")
  else:
    for i in students.keys():
      avg = get_average(i)
      print(f"\n{i}")
      print(f"Average: {avg:.1f} ({get_grade(avg)})\n"
            f"Highest: {max(students[i]):.1f} ({get_grade(max(students[i]))})\n"
            f"Lowest: {min(students[i]):.1f} ({get_grade(min(students[i]))})\n"
            f"Status: {check_pass(avg)}\n")

# Searches for a student by name. The name can be in any case but it has to match how it was entered...
# i.e. if 2 names were given, for example 'Ashton Reid-Huxley', both names have to be entered in the search
# i.e. 'ashton reid-huxley' OR 'ASHTON REID-HUXLEY' OR 'Ashton Reid-Huxley'
# Even a mix of cases is allowed as long as you type the name in full
def search_student(name):
  key = name.title()
  if validate_name(name):
    if key not in students:
      return f"\nSorry, {key} is not in our list.\n"
    else:
      avg = get_average(key)
      return f"\n{show_student_details(key)}Average: {avg:.1f} ({get_grade(avg)})\nStatus: {check_pass(avg)}\n"
  else:
    return f"'{name.title()}' is not a valid name."

# Used to prompt the user to enter the marks of the student. Returns a list of the marks
def get_marks(): 
  marks = []

  for i in range(3):
    while True:
      try:
        mark = int(input(f"Enter mark {i+1} >_ "))
      except ValueError:
        print("Please enter a number.")
      else:
        if mark < 0 or mark > 100:
          print("Please enter a valid mark (0-100).")
        else:
          marks.append(mark)
          break

  return marks

# Used to prompt for a student's information (both name and marks)
def get_student_info():
  while True:
    name = input("Enter the student's name >_ ").lower()
    if validate_name(name):
      break

  if name.title() in students:
    print(f"{name.title()} is already in our records")
    return
  else:
    marks = get_marks()
    
    return name.title(), marks
    
# Used when adding a student to the records
def add_student():
  s = get_student_info()
  if s == None:
    print("Couldn't add student")
  else:
    students[s[0]] = s[1]
    print(search_student(s[0]))
    save_students()

# Returns the details of a student (Name and Marks)
def show_student_details(k):
  return f"{k}\nMark 1: {students[k][0]} ({get_grade(students[k][0])})\nMark 2: {students[k][1]} ({get_grade(students[k][1])})\nMark 3: {students[k][2]} ({get_grade(students[k][2])})\n"

# Deletes a student record. Confirms before deleting. Uses name to search and follows the convention established in searching
def delete_student(name):
  if validate_name(name):
    key = name.title()
    if key not in students:
      print(f"'{key}' doesn't exist in the records.\n")
    else:
      while True:
        delete_choice = input(
          f"{show_student_details(key)}"
          f"Are you sure you want to delete this student? (y/n) >_ "
        )
        if delete_choice.upper() not in "YN":
          print(f"'{delete_choice}' is not a valid choice. Please try again")
        elif delete_choice.upper() == "Y":
          students.pop(key)
          print(f"'{key}' has been deleted")
          save_students()
          return
        else:
          print(f"Exiting without deleting...")
          break
  else:
    print(f"'{name.title()}' is not a valid name.")

# Returns a dict (name, average for that student)
def get_averages():
  averages = {}
  for k in students:
    averages[k] = get_average(k)
  return averages

# Uses the get_averages() to return the average for all the students in the record
def get_class_average():
  return round(sum(get_averages().values()) / len(students), 1)

# Returns the student with the highest average (the first match if multiple have the same average score)
def get_highest_average():
  return next(p for p, q in get_averages().items() if q == max(get_averages().values())), round(max(get_averages().values()), 1)

# Returns the student with the lowest average (the first match if multiple have the same average score)
def get_lowest_average():
  return next(p for p, q in get_averages().items() if q == min(get_averages().values())), round(min(get_averages().values()), 1)

# Returns the number of students whose average score is above or equal the to "Pass" threshold (50)
def get_passing():
  passing = 0
  for i in students.keys():
    average = get_average(i)
    if check_pass(average) == "Pass":
      passing += 1
  return passing

# Displays the number of students, average for the 'whole class' (all students combined),
# student with the highest and also lowest average score, the number of students passing
# and those that are failing
def show_statistics():
  if len(students) == 0:
    print("There aren't any students to calculate from. Trying adding a few.")
  else:
    highest_average = get_highest_average()
    lowest_average = get_lowest_average()
    print(
      f"\nStudents: {len(students)}\n"
      f"Class Average: {get_class_average()}  ({get_grade(get_class_average())})\n"
      f"Highest Average: {highest_average[0]} ({highest_average[1]} -> {get_grade(highest_average[1])})\n"
      f"Lowest Average: {lowest_average[0]} ({lowest_average[1]} -> {get_grade(lowest_average[1])})\n"
      f"Students Passing: {get_passing()}\n"
      f"Students Failing: {len(students) - get_passing()}\n"
    )

# Used to edit a student's details. Confirms before editing
def edit_student(name):
  if validate_name(name):
    key = name.title()
    if key not in students:
      print(f"'{key}' doesn't exist in our records")
    else:
      while True:
        edit_choice = input(
          f"{show_student_details(key)}"
          f"Are you sure you want to edit this student? (y/n) >_ "
        )
        if edit_choice.upper() not in "YN":
          print(f"'{edit_choice}' is not a valid choice. Please try again")
        elif edit_choice.upper() == "Y":
          students[key] = get_marks()
          print(f"'{key}' has been updated")
          print(f"{show_student_details(key)}")
          save_students()
          return
        else:
          print(f"Exiting without edit...")
          break
  else:
    print(f"'{name.title()}' is not a valid name.")

# Displays the ranking of students baed on the average score in descending order.
# Those with the same score are ranked according to how the records were added.
def rank_students():
  if len(students) == 0:
    print("There aren't any students in the records. Try adding a few")
  else:
    sorted_students = sorted(get_averages().items(), key = lambda k: k[1], reverse = True)
    print()

    for j, (name, average) in enumerate(sorted_students, start=1):
      print(f"{j}. {name} --> {average:.1f} ({get_grade(average)})")

    print()

# Runs the entire program with a menu to choose from
def run_program():
  load_students()
  while True:
    print(
      "==============================\n"
      "\t Grade Manager\n"
      "==============================\n"
      "1. View all students\n"
      "2. Search for a student\n"
      "3. Add a student\n"
      "4. Delete student\n"
      "5. Edit Student\n"
      "6. Class Statistics\n"
      "7. Rank Students\n"
      "8. Save Students\n"
      "9. Exit"
    )

    try:
      choice = int(input("Enter a number from the menu >_ "))
    except ValueError:
      print("Please enter a valid number")
    else:
      if choice == 1:
        view_students()
      elif choice == 2:
        name_searched = input("Enter a student's name >_ ")
        print(search_student(name_searched))
      elif choice == 3:
        add_student()
      elif choice == 4:
        name_deleted = input("Enter a student's name >_ ")
        delete_student(name_deleted)
      elif choice == 5:
        name_edited = input("Enter a student's name >_ ")
        edit_student(name_edited)
      elif choice == 6:
        show_statistics()
      elif choice == 7:
        rank_students()
      elif choice == 8:
        save_students()
      elif choice == 9:
        while True:
          exit_choice = input(f"Are you sure you want to exit? (Y/N) >_ ")
          if exit_choice.upper() not in "YN":
            print(f"'{exit_choice}' is not a valid choice. Please try again")
          elif exit_choice.upper() == "Y":
            save_students()
            print("Goodbye")
            exit()
          else:
            break
      else:
        print("Please enter a valid number")

run_program()
