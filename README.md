# Workshop Planner

Workshop Planner is a web application developed to facilitate the planning and management of workshops and events. It provides features for both organizers and participants, aiming to make the event planning process easier.

## Features
- **Event Management**: Create, display, and manage events with detailed information.
- **User Authentication**: Secure user registration, login, and logout functionalities.
- **Responsive Design**: Intuitive user interface with Bootstrap for a seamless experience across devices.
- **Search Functionality**: Search for events based on titles, descriptions, categories, and tags.
- **User Profiles**: Showcase user-specific information and activities.

## Installation Guide

1. Clone the repository: `git clone https://github.com/Emre-Oktay/workshopPlanner.git`

2. Navigate to the project directory: `cd workshopPlanner`

3. Create a virtual environment: `python -m venv venv`

4. Activate the virtual environment:

- On Windows: `venv\Scripts\activate`
- On macOS/Linux: `source venv/bin/activate`

5. Install dependencies: `pip install -r requirements.txt`

6. Apply migrations: `python manage.py migrate`

7. Run the development server: `python manage.py runserver`

Visit [http://localhost:8000](http://localhost:8000) in your web browser to access the Workshop Planner.
