# JobiPY

## Project Overview

The Job Portal App is a web application designed to connect job seekers with employers. Users can browse through job postings, apply for jobs, and employers can post new job opportunities. This app aims to streamline the job search process and make it easier for both job seekers and employers to find suitable matches. JobiPY is developed using Javascript, JQuery, HTML, and SASS for the frontend, Python and Django for the backend, and PostgreSQL as the database.

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

- **`JobiPY/`**: The main Django project directory.
  - **`settings.py`**: Contains the settings and configuration for the Django project.
  - **`urls.py`**: Defines the URL routing for the project.
  - **`asgi.py`**: Configured with ASGI to support WebSocket functionality, as opposed to WSGI.

- **`jobipy_app/`**: The app directory for managing job-related functionality.
  - **`models.py`**: Defines the data models for user profiles, user preferences, job postings, job applications, conversations, and messages.
  - **`views.py`**: Contains the logic for displaying HTML pages.
  - **`urls.py`**: Routes URLs to HTML pages and API.
  - **`consumers.py`**: Defines WebSocket consumers that handle real-time communication between the server and client, such as messaging and notifications.
  - **`routing.py`**: Used to define the WebSocket URL routing for Django Channels.
  - **`templates/jobipy/`**: HTML templates for rendering web pages.
     - **`layout.html`**: HTML file for the layout. Contains header and title.
     - **`index.html`**: HTML file for the homepage, this is the page that is shown if a user is not logged in.
     - **`register.html`**: HTML file for sign up page.
     - **`login.html`**: HTML file for sign in page.
     - **`setup.html`**: HTML file for the setting up job preferences.
     - **`jobs.html`**: HTML file for available jobs to apply.
     - **`profile.html`**: HTML file for profile information.
     - **`activities.html`**: HTML file for applied jobs.
     - **`posted.html`**: HTML file for jobs that is posted as employer.
     - **`post.html`**: HTML file for creating a job post.
     - **`message.html`**: HTML file for chat messages.
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
       **`images/`**: Contains images used as icons on buttons.
       **`scripts/`**: Contains Javascript files for making the html pages interactive.
        - **`index.js`**: Styles for layout.html.
        - **`register.js`**: Styles for register.html.
        - **`login.js`**: Styles for login.html.
        - **`setup.js`**: Styles for setup.html.
        - **`jobs.js`**: Styles for layout.html.
        - **`profile.js`**: Styles for layout.html.
        - **`activities.js`**: Styles for layout.html.
        - **`posted.js`**: Styles for layout.html.
        - **`post.js`**: Styles for layout.html.
        - **`message.js`**: Styles for layout.html.
        - **`overall.js`**: Styles for index.html.
        - **`menu.js`**: Styles for index.html.
        - **`menuNoTitle.js`**: Styles for index.html.
        - **`toIndex.js`**: Styles for index.html.
  - **`api/`**: Contains the logic for API endpoints.
     - **`api_index.py`**: Styles for layout.html.
     - **`api_register.py`**: Styles for index.html.
     - **`api_login.py`**: Styles for register.html.
     - **`api_setup.py`**: Styles for login.html.
     - **`api_jobs.py`**: Styles for setup.html.
     - **`api_profile.py`**: Styles for layout.html.
     - **`api_activities.py`**: Styles for layout.html.
     - **`api_posted.py`**: Styles for layout.html.
     - **`api_post.py`**: Styles for layout.html.
     - **`api_message.py`**: Styles for layout.html.
     - **`api_overall.py`**: Styles for layout.html.

- **`requirements.txt`**: Lists the Python packages required to run the application.

## How to Run the Application

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/job-portal-app.git
   cd job-portal-app
