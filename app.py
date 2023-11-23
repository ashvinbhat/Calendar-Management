import streamlit as st
import mysql.connector
from mysql.connector import Error
import datetime
import pandas as pd

# Function to connect to the MySQL database
# Database connection
def create_connection():
    return mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="your_database"
    )

# Function to create a connection to the MySQL database
def signup_user(username, password, email, phone_number):
   try:
      connection = create_connection()
      cursor = connection.cursor()

      # Insert user details into the USER table
      insert_user_query = "INSERT INTO USER (USER_NAME, PASSWORD, EMAIL) VALUES (%s, %s, %s)"
      cursor.execute(insert_user_query, (username, password, email))
      user_id = cursor.lastrowid

      # Insert phone number into the USER_PHONE table
      insert_phone_query = "INSERT INTO USER_PHONE (USER_ID, PHONE_NUMBER) VALUES (%s, %s)"
      cursor.execute(insert_phone_query, (user_id, phone_number))

      connection.commit()
      st.success("Signup successful! User added to the database.")
   except mysql.connector.Error as e:
      st.error(f"Error: {e.msg}")
   finally:
      if connection.is_connected():
         cursor.close()
         connection.close()


# Function to authenticate user
def authenticate_user(username, password):
   try:
      connection = create_connection()
      cursor = connection.cursor()

      # Check if user exists and credentials are correct
      check_user_query = "SELECT * FROM USER WHERE USER_NAME = %s AND PASSWORD = %s"
      cursor.execute(check_user_query, (username, password))
      user = cursor.fetchone()

      if user:
         st.success("Authentication successful! User logged in.")
      else:
         st.error("Authentication failed. Invalid username or password.")

   except mysql.connector.Error as e:
      st.error(f"Error: {e.msg}")
   finally:
      if connection.is_connected():
         cursor.close()
         connection.close()

# Function to add a new calendar to the database
def add_calendar(calendar_name, user_id):
   try:
      connection = create_connection()
      cursor = connection.cursor()

      # Insert the new calendar into the CALENDAR table
      insert_calendar_query = "INSERT INTO CALENDAR (CALENDAR_NAME, USER_ID) VALUES (%s, %s)"
      cursor.execute(insert_calendar_query, (calendar_name, user_id))

      connection.commit()
      st.success("New calendar added to the database.")
   except mysql.connector.Error as e:
      st.error(f"Error: {e.msg}")
   finally:
      if connection.is_connected():
         cursor.close()
         connection.close()


# Function to fetch user's calendars from the database
def fetch_calendars(user_id):
   calendars = []
   try:
      connection = create_connection()
      cursor = connection.cursor()

      # Fetch user's calendars from the CALENDAR table
      fetch_calendars_query = "SELECT CALENDAR_NAME FROM CALENDAR WHERE USER_ID = %s"
      cursor.execute(fetch_calendars_query, (user_id,))
      result = cursor.fetchall()

      for row in result:
         calendars.append(row[0])

   except mysql.connector.Error as e:
      st.error(f"Error: {e.msg}")
   finally:
      if connection.is_connected():
         cursor.close()
         connection.close()
   
   return calendars

# Function to get the calendar ID based on the selected calendar name
def get_calendar_id(calendar_name, user_id):
   try:
      connection = create_connection()
      cursor = connection.cursor()

      # Fetch the calendar ID for the selected calendar name and user ID
      get_calendar_id_query = "SELECT CALENDAR_ID FROM CALENDAR WHERE CALENDAR_NAME = %s AND USER_ID = %s"
      cursor.execute(get_calendar_id_query, (calendar_name, user_id))
      result = cursor.fetchone()

      if result:
         return result[0]

   except mysql.connector.Error as e:
      st.error(f"Error: {e.msg}")
   finally:
      if connection.is_connected():
         cursor.close()
         connection.close()


# Function to add an event to the database
def add_event(event_title, event_description, start_time, end_time, calendar_id, state, city, zipcode):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        insert_event_query = """
            INSERT INTO EVENTS 
            (EVENT_TITLE, EVENT_DESCRIPTION, START_TIME, END_TIME, CALENDAR_ID, STATE_, CITY, ZIPCODE) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
         # Unpack date and time tuples to construct datetime values
        start_datetime = datetime.datetime.combine(start_time[0], start_time[1])
        end_datetime = datetime.datetime.combine(end_time[0], end_time[1])

        # Pass the parameters as a tuple to the cursor.execute method
        cursor.execute(insert_event_query, (event_title, event_description, start_datetime, end_datetime, calendar_id, state, city, zipcode))

        connection.commit()
        st.success("New event added to the database.")
    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to add a task to the database
def add_task(task_title, task_description, due_time, calendar_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        insert_task_query = """
            INSERT INTO TASK 
            (TASK_TITLE, TASK_DESCRIPTION, DUE_TIME, CALENDAR_ID) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_task_query, (task_title, task_description, due_time, calendar_id))

        connection.commit()
        st.success("New task added to the database.")
    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to add a note to the database
def add_note(note_description, date_created, calendar_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        insert_note_query = """
            INSERT INTO NOTES 
            (NOTE_DESCRIPTION, DATE_CREATED, CALENDAR_ID) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_note_query, (note_description, date_created, calendar_id))

        connection.commit()
        st.success("New note added to the database.")
    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to fetch events for a particular calendar and date
def fetch_events(calendar_id, selected_date):
    events = []
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Fetch events from the EVENTS table for the selected calendar and date
        fetch_events_query = "SELECT EVENT_TITLE, EVENT_DESCRIPTION, START_TIME, END_TIME FROM EVENTS WHERE CALENDAR_ID = %s AND DATE(START_TIME) = %s"
        cursor.execute(fetch_events_query, (calendar_id, selected_date))
        result = cursor.fetchall()

        for row in result:
            events.append({
                "title": row[0],
                "description": row[1],
                "start_time": row[2],
                "end_time": row[3]
            })

    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return events


# Function to update task status using the stored procedure
def update_task_status(task_id, new_status):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Call the stored procedure
        cursor.callproc("UpdateTaskStatus", (task_id, new_status))
        connection.commit()
        st.success("Task status updated successfully.")

    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



# Function to fetch tasks for a particular calendar
def fetch_tasks(calendar_id, selected_date):
    tasks = []
    try:
        connection = create_connection()
        cursor = connection.cursor()

        fetch_tasks_query = "SELECT TASK_ID, TASK_TITLE, TASK_DESCRIPTION, DUE_TIME, STATUS_ FROM TASK WHERE CALENDAR_ID = %s AND DATE(DUE_TIME) = %s"
        cursor.execute(fetch_tasks_query, (calendar_id, selected_date))
        result = cursor.fetchall()

        for row in result:
            tasks.append({
               "id": row[0],
               "title": row[1],
               "description": row[2],
               "deadline": row[3],
               "status": row[4]
            })

    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return tasks

# Function to fetch tasks for a particular calendar
def fetch_collaborated_tasks(user_id):
    collaborated_tasks = []
    try:
        connection = create_connection()
        cursor = connection.cursor()

        fetch_collaborated_tasks_query = """
            SELECT t.TASK_ID, t.TASK_TITLE, t.TASK_DESCRIPTION, t.DUE_TIME, t.STATUS_, c.USER_ID1, c.USER_ID2
            FROM TASK t, COLLABORATION c
            WHERE t.TASK_ID IN (
                SELECT c.TASK_ID
                FROM COLLABORATION c
                WHERE c.USER_ID1 = %s OR c.USER_ID2 = %s
            )
        """
        cursor.execute(fetch_collaborated_tasks_query, (user_id, user_id))
        result = cursor.fetchall()

        for row in result:
            collaborated_tasks.append({
               "id": row[0],
               "title": row[1],
               "description": row[2],
               "deadline": row[3],
               "status": row[4],
               "user_id1": row[5],
               "user_id2": row[6]
            })

    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return collaborated_tasks



# Function to fetch notes for a particular date
def fetch_notes(calendar_id, selected_date):
    notes = []
    try:
        connection = create_connection()
        cursor = connection.cursor()

        fetch_notes_query = "SELECT NOTE_DESCRIPTION, DATE_CREATED FROM NOTES WHERE CALENDAR_ID = %s AND DATE(DATE_CREATED) = %s"
        cursor.execute(fetch_notes_query, (calendar_id, selected_date))
        result = cursor.fetchall()

        for row in result:
            notes.append({
                "description": row[0],
                "date_created": row[1]
            })

    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return notes


# Function to add collaboration between a user and a task
def add_collaboration(user_id1, user_id2, task_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Insert collaboration details into the COLLABORATION table
        insert_collaboration_query = "INSERT INTO COLLABORATION (USER_ID1, USER_ID2, TASK_ID) VALUES (%s, %s, %s)"
        cursor.execute(insert_collaboration_query, (user_id1, user_id2, task_id))

        connection.commit()
        st.success("Collaboration added successfully!")
    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to execute custom SQL queries
def execute_custom_query(sql_query):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Execute the custom SQL query
        cursor.execute(sql_query)
        result = cursor.fetchall()

        if result:
            # Display the output in a DataFrame
            df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
            st.write(df)
        else:
            st.write("No data available for the query.")

    except mysql.connector.Error as e:
        st.error(f"Error: {e.msg}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Streamlit UI
def main():
   st.title("Calendar management system")

   # Login and Signup Section
   st.session_state.user_id = st.session_state.get("user_id", None)
   st.session_state.user_type = st.session_state.get("user_type", None)

   menu = ["Login", "Signup", "Calendar", "Add Event", "Add Task", "Add Note", "Update Task Status", "Custom Query", "Add Collaboration", "View Collaborated Tasks"]
   choice = st.sidebar.selectbox("Menu", menu)

   if choice == "Login":
      st.subheader("Login")
      username = st.text_input("Username")
      password = st.text_input("Password", type="password")
      if st.button("Login"):
         authenticate_user(username, password)
         st.session_state.user_id = 1
         st.session_state.user_type = "user"

   elif choice == "Signup":
      st.subheader("Signup")
      username = st.text_input("Username")
      password = st.text_input("Password", type="password")
      email = st.text_input("Email")
      phone_number = st.text_input("Phone Number")
      if st.button("Signup"):
         signup_user(username, password, email, phone_number)

   elif choice == "Calendar" and st.session_state.user_id:
      # Calendar Section
      selected_date = st.sidebar.date_input("Select a date", datetime.date.today())

      # Create a sidebar for adding calendars
      st.sidebar.title("Calendars")
      calendars = fetch_calendars(st.session_state.user_id)
      selected_calendar = st.sidebar.selectbox("Select a calendar", calendars)
      st.session_state.selected_calendar = selected_calendar
      st.session_state.selected_date = selected_date

      # Add a button to create a new calendar in the database
      new_calendar = st.sidebar.text_input("Enter the name of the new calendar")
      if st.sidebar.button("Add new calendar"):
         if new_calendar:
               added = add_calendar(new_calendar, st.session_state.user_id)
               if added:
                  calendars = fetch_calendars(st.session_state.user_id)
                  selected_calendar = new_calendar
                  st.session_state.calendar_id = get_calendar_id(selected_calendar, st.session_state.user_id)  # Update calendar_id after adding a new calendar
                  st.session_state.selected_calendar = selected_calendar  # Update selected_calendar after adding a new calendar

      # Display the selected date and calendar
      st.title(f"Selected Date: {selected_date}")
      st.title(f"Selected Calendar: {selected_calendar}")


      # Sidebar buttons for events, tasks, and notes
      st.sidebar.subheader("View:")
      show_events = st.sidebar.button("Events")
      show_tasks = st.sidebar.button("Tasks")
      show_notes = st.sidebar.button("Notes")

       # Display events, tasks, or notes based on button click
      if show_events:
         st.header("Events")
         # Fetch and display events
         calendar_id = get_calendar_id(selected_calendar, st.session_state.user_id)
         events = fetch_events(calendar_id, selected_date)
         for event in events:
               st.write(f"Title: {event['title']}, Description: {event['description']}, Start Time: {event['start_time']}, End Time: {event['end_time']}")

      elif show_tasks:
         st.header("Tasks")
         # Fetch and display tasks
         calendar_id = get_calendar_id(selected_calendar, st.session_state.user_id)
         tasks = fetch_tasks(calendar_id, selected_date)
         for task in tasks:
               st.write(f"ID: {task['id']}, Title: {task['title']}, Description: {task['description']}, Deadline: {task['deadline']}, Status: {task['status']}")

      elif show_notes:
         st.header("Notes")
         # Fetch and display notes
         calendar_id = get_calendar_id(selected_calendar, st.session_state.user_id)
         notes = fetch_notes(calendar_id, selected_date)
         for note in notes:
               st.write(f"Description: {note['description']}, Date Created: {note['date_created']}")



   elif choice == "Add Event" and st.session_state.user_id:
      st.title("Add Event")
      event_title = st.text_input("Event Title")
      event_description = st.text_input("Event Description")
      start_time = st.date_input("Start Date"), st.time_input("Start Time")
      end_time = st.date_input("End Date"), st.time_input("End Time")
      state = st.text_input("State")
      city = st.text_input("City")
      zipcode = st.text_input("Zipcode")

      if st.button("Submit Event"):
         calendar_id = get_calendar_id(st.session_state.selected_calendar, st.session_state.user_id)
         add_event(event_title, event_description, start_time, end_time, calendar_id, state, city, zipcode)
         st.success("Event added successfully!")

   elif choice == "Add Task" and st.session_state.user_id:
      st.title("Add Task")
      task_title = st.text_input("Task Title")
      task_description = st.text_input("Task Description")
      deadline = st.date_input("Deadline")

      if st.button("Submit Task"):
         calendar_id = get_calendar_id(st.session_state.selected_calendar, st.session_state.user_id)
         add_task(task_title, task_description, deadline, calendar_id)
         st.success("Task added successfully!")

   elif choice == "Add Note" and st.session_state.user_id:
      st.title("Add Note")
      note_description = st.text_area("Note Description")
      date_created = st.session_state.selected_date

      if st.button("Submit Note"):
         calendar_id = get_calendar_id(st.session_state.selected_calendar, st.session_state.user_id)
         add_note(note_description, date_created, calendar_id)
         st.success("Note added successfully!")

   elif choice == "Update Task Status" and st.session_state.user_id:
      st.title("Update Task Status")
      task_id = st.text_input("Task ID")
      new_status = st.selectbox("New Status", ["Completed", "INCOMPLETE"])

      if st.button("Update Task Status"):
         update_task_status(task_id, new_status)
   
   elif choice == "Custom Query" and st.session_state.user_id:
      st.title("Custom Query")
      sql_query = st.text_area("Enter your query here")
      if st.button("Execute Query"):
         execute_custom_query(sql_query)

   elif choice == "Add Collaboration" and st.session_state.user_id:
      st.title("Add Collaboration")
      user_id1 = st.text_input("User ID1")
      user_id2 = st.text_input("User ID2")
      task_id = st.text_input("Task ID")

      if st.button("Add Collaboration"):
         add_collaboration(user_id1, user_id2, task_id)
         st.success("Collaboration added successfully!")

   elif choice == "View Collaborated Tasks" and st.session_state.user_id:
      st.title("View Collaborated Tasks")
      collaborated_tasks = fetch_collaborated_tasks(st.session_state.user_id)
      for task in collaborated_tasks:
         st.write(f"ID: {task['id']}, Title: {task['title']}, Description: {task['description']}, Deadline: {task['deadline']}, Status: {task['status']}\n Collaborated with: USER1: {task['user_id1']},  USER2: {task['user_id2']}")


if __name__ == "__main__":
    main()