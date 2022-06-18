# Art Explorer

## Art Explorer is my Springboard Capstone 1 project

### Objectives

- Build a database-driven website
- Utilize a publically available API
- Incorporate front-end and back-end technologies to demonstrate the skills learned in the program to-date
- Create something cool!

### Here is a link to the API documentation for this project

"https://metmuseum.github.io/"

### Here is the link to the deployed app. Check it out. I hope you like it. Feedback is appreciated.

"https://artexplorer.herokuapp.com/"

### Art Explorer is an app for art lovers to use to explore The Metropolitan Museum of Art Collection

### User Flow

- Register for an account
- Login to your account
- Search for works of art by any search term
- Select a work of art to view an image and information about the art, title and artist, etc.
- Add a work of art to your personal art collection
- View a full-screen image of the art
- Add your notes or comments about the art if you'd like
- Share your collection with other users of the app
- View the collections shared by other art lovers
- Remove art from your collection if you want

### Notes

- It is necessary to create an account to use the app but only a username, first name, and last name are required, no API key is needed
- No password reset feature is included. A user can change their password but forgotten passwords must be reset by a db admin

### Tech Stack Used

- Python
- Flask
- SQLAlchemy
- WTForms
- PostgresSQL
- Bootstrap 5
- Bcrypt for passwords
- HTML/CSS/JavaScript for the front-end
- Heroku with Gunicorn for deployment

see the requirement.txt file for details of versions needed for venv

### For testing

#### run python -m unittest test_app.py

### ERD and DB Schema

<!-- markdownlint-disable -->
<img src="art_explorer erd.png">
<img src="art_explorer schema.png">
<!-- markdownlint-restore -->

### In The Future

- Tools to filter, sort, and categorize your collection as is grows larger
- Filters for seaching by department, etc.
- Get additional information from the museum website that is not available via the API
- More museums to explore!
