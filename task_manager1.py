'''
This Python script, is a comprehensive task management system designed for both administrators and users. 
It enables user registration with secure password verification, task assignment with detailed specifications, 
and personal task viewing for efficient management. 
Administrators have exclusive access to generate detailed reports and view system-wide statistics, 
enhancing oversight and productivity. This high-level overview serves as a guide for navigating the application's functionalities, 
ensuring a user-friendly experience for task administration and tracking

'''
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Declare the global variable at the top of your script
curr_user = None
# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

task_list = []  # Initialize an empty list to hold task dictionaries
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

    # Parse each task string into a dictionary and add to task_list
    for t_str in task_data:
        task_components = t_str.split(";")
        curr_t = {
            'username': task_components[0],
            'title': task_components[1],
            'description': task_components[2],
            'assigned_date': datetime.strptime(task_components[3], DATETIME_STRING_FORMAT),
            'due_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
            'completed': task_components[5] == "Yes"
        }
        task_list.append(curr_t)


#====Login Section====
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password\n")  # Ensure newline character for proper reading

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().strip().split("\n")

# Convert to a dictionary
username_password = {}
for user_info in user_data:
    user_info_split = user_info.split(';')
    if len(user_info_split) >= 2:  # Check if user info contains username and password
        username = user_info_split[0]
        password = user_info_split[1]
        username_password[username] = password
    else:
        print(f"Ignoring invalid user data: {user_info}")

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user_input = input("Username: ")
    curr_pass = input("Password: ")

    if curr_user_input not in username_password:
        print("User does not exist")
        continue
    elif username_password[curr_user_input] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True
        curr_user = curr_user_input  # Set the global variable upon successful login


def safe_write(file_path, content):
    """Appends content to a file, ensuring it starts on a new line if the file is not empty."""
    with open(file_path, 'a+') as file:
        file.seek(0)  # Move file pointer to the beginning
        if file.read(1):  # Check if the file is not empty
            content = '\n' + content  # Prepend a newline if the file is not empty

        file.write(content + '\n')  # Always append a newline to content


def reg_user():
    """Registers a new user with password verification."""
    username = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()
    password_verify = input("Re-enter your password for verification: ").strip()

    if not username:
        print("Username cannot be empty.")
        return
    if not password or password != password_verify:
        print("Passwords do not match or are empty.")
        return

    with open('user.txt', 'r') as users_file:
        existing_users = [user.split(';')[0].strip() for user in users_file.readlines()]

    if username in existing_users:
        print("Username already exists.")
    else:
        try:
            safe_write('user.txt', f"{username};{password}")
            print("User registered successfully.")
        except IOError as e:
            print(f"An error occurred while accessing 'user.txt': {e}")


def add_task():
    """Adds a new task directly to the tasks.txt file."""
    task_title = input("Enter task title: ").strip()
    task_description = input("Enter task description: ").strip()
    assigned_to = input("Enter the username of the person this task is assigned to: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(due_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    current_date = datetime.now().strftime('%Y-%m-%d')
    completed = "No"

    # Use safe_write to append the new task
    safe_write("tasks.txt", f"{assigned_to};{task_title};{task_description};{current_date};{due_date};{completed}")

    print("Task added successfully.")


def view_all():
    """Displays all tasks."""
    try:
        with open('tasks.txt', 'r') as tasks_file:
            tasks = tasks_file.readlines()

        if not tasks:
            print("There are no tasks to display.")
            return

        print("All tasks:\n")
        for index, task in enumerate(tasks, start=1):
            task_details = task.strip().split(';')
            if len(task_details) == 6:  # Ensure that the task entry has all necessary fields
                assigned_date = datetime.strptime(task_details[3], "%Y-%m-%d").strftime("%d-%m-%Y")
                due_date = datetime.strptime(task_details[4], "%Y-%m-%d").strftime("%d-%m-%Y")

                print(f"Task {index}:\nAssigned to: {task_details[0]}\nTitle: {task_details[1]}\n"
                      f"Description: {task_details[2]}\nDate Assigned: {assigned_date}\n"
                      f"Due Date: {due_date}\nCompleted: {task_details[5]}\n")
                print("--------------------------------------------------")
            else:
                print(f"Issue with task format at line {index}: {task}")
    except IOError:
        print("Could not read 'tasks.txt'. Please ensure the file exists and is accessible.")


def mark_task_as_complete(task_index, tasks):
    """Marks a task as complete."""
    task_details = tasks[task_index].strip().split(';')
    if task_details[5] != 'Yes':
        task_details[5] = 'Yes'
        tasks[task_index] = ';'.join(task_details) + '\n'


def edit_task(task_index, tasks):
    """Edits a task."""
    task_details = tasks[task_index].strip().split(';')
    if task_details[5] == 'Yes':
        print("This task has already been completed and cannot be edited.")
        return

    print("Edit task:\n1. Assignee username\n2. Due date")
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice == '1':
        new_username = input("Enter new username: ").strip()
        task_details[0] = new_username
    elif choice == '2':
        new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
        task_details[4] = new_due_date

    tasks[task_index] = ';'.join(task_details) + '\n'
    print("Task updated successfully.")


def view_mine():
    global curr_user
    try:
        with open('tasks.txt', 'r') as tasks_file:
            tasks = tasks_file.readlines()

        user_tasks = [task for task in tasks if task.split(';')[0] == curr_user]
        if not user_tasks:
            print(f"No tasks found for user {curr_user}.")
            return

        print(f"Tasks assigned to {curr_user}:")
        for i, task in enumerate(user_tasks, start=1):
            parts = task.strip().split(';')
            print(f"{i}. Title: {parts[1]}\n   Description: {parts[2]}\n"
                  f"   Date Assigned: {parts[3]}\n   Due Date: {parts[4]}\n"
                  f"   Completed: {parts[5]}\n")

        task_choice = int(input("Select a task number to edit or mark as "
                                "complete, or '-1' to return to the main menu: "))
        if task_choice == -1:
            return

        if 1 <= task_choice <= len(user_tasks):
            task_index = tasks.index(user_tasks[task_choice - 1])
            print("Do you want to:\n1. Mark this task as complete\n2. Edit this task")
            user_choice = input("Enter your choice (1 or 2): ")
            if user_choice == '1':
                mark_task_as_complete(task_index, tasks)
            elif user_choice == '2':
                edit_task(task_index, tasks)

        # Instead of writing only user_tasks, write back all tasks
        with open('tasks.txt', 'w') as file:
            file.writelines(tasks)

    except IOError:
        print("Could not read 'tasks.txt'. Please ensure the file exists and is accessible.")


def display_statistics():
    global curr_user
    if curr_user != 'admin':
        print("Access denied: This feature is available to admin only.")
        return

    # Proceed with displaying statistics
    with open('user.txt', 'r') as users_file:
        users = users_file.readlines()
    num_users = len(users)

    with open('tasks.txt', 'r') as tasks_file:
        tasks = tasks_file.readlines()
    num_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if "Yes" in task.split(';')[5])
    incomplete_tasks = num_tasks - completed_tasks
    overdue_tasks = sum(1 for task in tasks if "No" in task.split(';')[5] and datetime.strptime(task.split(';')[4], "%Y-%m-%d") < datetime.now())

    # Display calculated statistics
    print("-----------------------------------")
    print(f"Number of users: {num_users}")
    print(f"Total tasks: {num_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Incomplete tasks: {incomplete_tasks}")
    print(f"Overdue tasks: {overdue_tasks}")
    print(f"Percentage incomplete: {(incomplete_tasks / num_tasks * 100) if num_tasks else 0:.2f}%")
    print(f"Percentage overdue: {(overdue_tasks / num_tasks * 100) if num_tasks else 0:.2f}%")
    print("-----------------------------------")


def main():
    global curr_user
    # Add user interface here
    user_interface()


def user_interface():
    while True:
        print("\nMAIN MENU")
        print("1. View all tasks")
        print("2. Add a new task")
        print("3. Register a new user")
        print("4. View my tasks")
        print("5. Display statistics")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_all()
        elif choice == '2':
            add_task()
        elif choice == '3':
            reg_user()
        elif choice == '4':
            view_mine()
        elif choice == '5':
            display_statistics()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
