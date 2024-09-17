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
     - **`layout.html`**: Layout HTML file including header and title.
     - **`index.html`**: Homepage HTML file shown to users who are not logged in.
     - **`register.html`**: Sign-up page HTML file with a registration form.
     - **`login.html`**: Sign-in page HTML file with a login form.
     - **`setup.html`**: HTML file for setting up job preferences with a preference form.
     - **`jobs.html`**: HTML file listing available jobs with containers for job postings and descriptions.
     - **`profile.html`**: HTML file displaying profile information, including a resume image.
     - **`activities.html`**: HTML file showing applied jobs, with containers for job postings the user has applied to.
     - **`posted.html`**: HTML file for jobs posted by the user as an employer, including containers for job postings and descriptions.
     - **`post.html`**: HTML file for creating a new job post with a job post form.
     - **`message.html`**: HTML file for chat messages with a message container.
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
        - **`index.js`**: Functions for `index.html`, such as job posting searches and filtering.
        - **`register.js`**: Functions for `register.html`, including account creation.
        - **`login.js`**: Functions for `login.html`, handling user login.
        - **`setup.js`**: Functions for `setup.html`, checking and creating user preferences.
        - **`jobs.js`**: Functions for `jobs.html`, retrieving job postings based on user preferences and applying for jobs.
        - **`profile.js`**: Functions for `profile.html`, viewing and updating user details and resume.
        - **`activities.js`**: Functions for `activities.html`, displaying jobs the user has applied to.
        - **`posted.js`**: Functions for `posted.html`, managing job posts as an employer, viewing applicants, and messaging them.
        - **`post.js`**: Functions for `post.html`, allowing the creation of new job posts.
        - **`message.js`**: Functions for `message.html`, enabling chat messages about applications.
        - **`overall.js`**: Functions for notifications, including message updates and application status changes.
        - **`menu.js`**: Styles the header menus.
        - **`menuNoTitle.js`**: Styles menus for pages not in the main navigation, like `message` and `post`.
        - **`menuAnimations.js`**: Triggers animations for menus.
        - **`toIndex.js`**: Determines if a user should be directed to the index page or the jobs page based on login status.
  - **`api/`**: Contains the logic for API endpoints.
     - **`api_index.py`**: Functions to provide job post data including job ID, title, company, pay, etc.
     - **`api_register.py`**: Functions to create a new user account.
     - **`api_login.py`**: Functions to verify user credentials for login access.
     - **`api_setup.py`**: Functions to create and manage user preferences.
     - **`api_jobs.py`**: Functions to handle job posting data, search for specific jobs, and apply for jobs.
     - **`api_profile.py`**: Functions to update the user’s resume.
     - **`api_activities.py`**: Functions to retrieve job postings that the user has applied for.
     - **`api_posted.py`**: Functions to manage job postings by the user, view applicant resumes, create message groups, and manage application statuses.
     - **`api_post.py`**: Functions to create a new job post.
     - **`api_message.py`**: Functions to retrieve group names for conversations and send messages.
     - **`api_overall.py`**: Functions for user data, logging out, sending notifications, reading messages, and checking application statuses.
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
