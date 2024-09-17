# Jobipy

## Project Overview

Jobipy is a web application designed to connect job seekers with employers. Users can browse through job postings, apply for jobs, and employers can post new job opportunities. This app aims to streamline the job search process and make it easier for both job seekers and employers to find suitable matches. JobiPY is developed using Javascript, JQuery, HTML, and SASS for the frontend, Python and Django for the backend, and PostgreSQL as the database.

## Distinctiveness and Complexity

### Distinctiveness

JobiPY serves a unique purpose: to bridge the gap between job seekers and employers. It is distinct from the previous projects like commerce, which are designed for buying and selling products, and from network, which focus on connecting individuals and sharing life updates. The core functionality of JobiPY revolves around job recruitment and application, making it a specialized tool in the job market ecosystem.

### Complexity

The complexity of this project surpasses that of the previous commerce and network projects due to several factors:

1. **Data Management**: The app handles diverse types of data, including user information, job preferences, and resumes (uploaded as PDF files, displayed on the frontend as JPG which is converted pdf file on the backend). Managing and securely storing this data requires robust backend architecture and database design.
   
2. **File Storage**: Implementing file storage for resumes PDF and JPG introduces additional complexity. Handling file uploads and ensuring their security and accessibility were not covered in the course, adding a layer of complexity.

3. **Real-Time Features**: The most complex feature of this application is its real-time messaging and notification system. Utilizing WebSockets for real-time communication presents challenges, particularly as this is the first time implementing such a feature. Real-time updates for messaging and notifications require careful handling of WebSocket connections and state management.

## File Descriptions

- **`manage.py`**: A command-line utility that lets you interact with this Django project. It provides commands for running the development server, managing migrations, and more.
- **`jobipy_app/`**: The app directory for managing job-related functionality.
  - **`models.py`**: Defines the data models for user profiles, user preferences, job postings, job applications, conversations, and messages.
  - **`views.py`**: Contains the logic for displaying HTML pages.
  - **`urls.py`**: Routes URLs to HTML pages and API.
  - **`consumers.py`**: Defines WebSocket consumers that handle real-time communication between the server and client, such as messaging and notifications.
  - **`routing.py`**: Used to define the WebSocket URL routing for Django Channels.
  - **`templates/jobipy/`**: HTML templates for rendering web pages.
     - **`layout.html`**: HTML file for the layout. Contains header and title.
     - **`index.html`**: HTML file for the homepage, this is the page that is shown if a user is not logged in.
     - **`register.html`**: HTML file for sign up page. Contains a sign up form.
     - **`login.html`**: HTML file for sign in page. Contains a log in form.
     - **`setup.html`**: HTML file for the setting up job preferences. Contains a preference form.
     - **`jobs.html`**: HTML file for available jobs to apply. Contains different containers for job postings and descriptions.
     - **`profile.html`**: HTML file for profile information. Contains container for profile information and an image for resume.
     - **`activities.html`**: HTML file for applied jobs. Contains different containers for job postings that the user applied to and descriptions.
     - **`posted.html`**: HTML file for jobs that is posted as employer. Contains different containers for job postings that the user posted as employer and descriptions.
     - **`post.html`**: HTML file for creating a job post. Contains a job post form.
     - **`message.html`**: HTML file for chat messages. Contains a container for messages.
  - **`static/jobipy/`**: Contains static files such as CSS, JavaScript, and images used throughout the project.
     - **`css/`**: Contains CSS files for styling html pages.
        - **`layout.css`**: Styles for layout.html.
        - **`index.css`**: Styles for index.html.
        - **`register.css`**: Styles for register.html.
        - **`login.css`**: Styles for login.html.
        - **`setup.css`**: Styles for setup.html.
        - **`jobs.css`**: Styles for layout.html.
        - **`profile.css`**: Styles for layout.html.
        - **`activities.css`**: Styles for layout.html.
        - **`posted.css`**: Styles for layout.html.
        - **`post.css`**: Styles for layout.html.
        - **`message.css`**: Styles for layout.html.
     - **`images/`**: Contains images used as icons on buttons.
     - **`scripts/`**: Contains Javascript files for making the html pages interactive.
        - **`index.js`**: Contains functions needed for index.html. Getting job postings by searching or filtering industry.
        - **`register.js`**: Contains functions needed for register.html. Creating new account.
        - **`login.js`**: Contains functions needed for login.html. Logging in the user.
        - **`setup.js`**: Contains functions needed for setup.html. Checking if the user has preference or not, if not, then create one.
        - **`jobs.js`**: Contains functions needed for jobs.html. Getting job postings based on user's preferences, Apply to any job post.
        - **`profile.js`**: Contains functions needed for profile.html. See the user's details as well as their resume, they can modify their preferences and replace resume here.
        - **`activities.js`**: Contains functions needed for activities.html. See the job posts that the user had applied to.
        - **`posted.js`**: Contains functions needed for posted.html. See the posted jobs as employer, they can also see the users who applied to a job post and they can send them a message.
        - **`post.js`**: Contains functions needed for post.html. Let the user create a new job post.
        - **`message.js`**: Contains functions needed for message.html. Let the user send a message to chat about the application.
        - **`overall.js`**: Contains functions needed for notifications like updated messages and application status changes. 
        - **`menu.js`**: Used to style the menus in header.
        - **`menuNoTitle.js`**: Used to style the menus but this script is used by pages that are not in menus like message and post.
        - **`menuAnimations.js`**: Used to trigger menu animations.
        - **`toIndex.js`**: Used to have the app name a function to either send the user to index if they are not logged in ro to jobs if they are logged in.
  - **`api/`**: Contains the logic for API endpoints.
     - **`api_index.py`**: Contains a function to send job post data such as job id, job title, company, pay and etc.
     - **`api_register.py`**: Contains a function that creates an account for user.
     - **`api_login.py`**: Contains a function that verifies user credentials giving them access to login.
     - **`api_setup.py`**: Contains functions to create a new preference and send preference data.
     - **`api_jobs.py`**: Contains functions to send job posting data, specific job posts based on search, and create an application to a job post.
     - **`api_profile.py`**: Contains a function to replace the current resume to a new one.
     - **`api_activities.py`**: Contains a function to send job posting data that the user applied to.
     - **`api_posted.py`**: Contains functions to send job posting data that the user has posted, viewing the resume of the users who applied, creating a group name for messages, creating a conversation, and setting the applications status.
     - **`api_post.py`**: Contains a function to create a new job post.
     - **`api_message.py`**: Contains functions to retrieve the conversation's group name and to send a message.
     - **`api_overall.py`**: Contains functions to send data about the user, for logging out, for sending notifications, for reading messages, and for viewing application status
- **`requirements.txt`**: Lists the Python packages required to run the application.

## How to Run the Application

1. **Clone the Repository**

   ```
   git clone https://github.com/Geode30/JobiPY.git
   cd JobiPY

2. **Create a virtual environment**

   ```
   python -m venv env
   env\Scripts\activate 

3. **Install dependencies**

   ```
   python install -r requirements.txt

4. **Apply Migrations**

   ```
   python manage.py migrate

2. **Start the server**

   ```
   python manage.py runserver
