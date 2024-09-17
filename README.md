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
  - **`templates/`**: HTML templates for rendering job-related pages.
  - **`static/`**: Contains static files such as CSS, JavaScript, and images used throughout the project.
  - **`api/`**: Contains the logic for API endpoints.

- **`requirements.txt`**: Lists the Python packages required to run the application. (To be created based on your project's dependencies.)

## How to Run the Application

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/job-portal-app.git
   cd job-portal-app
