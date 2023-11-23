# Calendar Management System

This is a Calendar Management System built using Streamlit for the frontend and MySQL for the backend database.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation and Usage](#installation-and-usage)
- [Database Structure](#database-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Calendar Management System is designed to assist users in managing their calendars, events, tasks, and notes. It provides a user-friendly interface to add, view, and update events, tasks, and notes associated with different calendars.

## Features

- User authentication (Signup/Login)
- Create, view, and select calendars
- Add events with descriptions, start/end times, and locations
- Add tasks with titles, descriptions, and deadlines
- Add notes with descriptions and creation dates
- Collaborate on tasks with other users
- Custom SQL query execution
- Update task status using a stored procedure

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/calendar-management-system.git
   ```

2. Install the required Python packages:

   ```bash
   pip install streamlit
   pip install mysql-connector-python
   ```

3. Set up your MySQL database and configure the connection in the code.

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

5. Use the web interface to sign up or log in and start managing your calendar, events, tasks, and notes.

## Database Structure

The database structure includes the following tables:

- USER: Stores user information
- CALENDAR: Stores calendar details
- EVENTS: Stores event-related information
- TASK: Stores task-related information
- NOTES: Stores note-related information
- COLLABORATION: Stores information about collaborations between users and tasks

## Contributing

Contributions are welcome! If you want to contribute to this project, follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
