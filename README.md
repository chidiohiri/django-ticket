# Django Ticket

This project is a comprehensive Customer Support Ticketing System built with Django. It facilitates efficient support management by enabling customers to create, track, and manage tickets while integrating a secure wallet payment system for support services. Support engineers and admins can assign, resolve, and manage tickets, ensuring smooth communication and service delivery.

### Getting Started

These instructions will guide you through setting up Django Ticket on your local machine for development and testing purposes. This guide assumes you are working on a Windows environment. Mac and Linux users can adapt the commands accordingly.

### Prerequisites

Below are the dependencies for the project. For quicker installation, please refer to the [requirements.txt](requirements.txt) file.
- [Python](https://www.python.org/downloads/) - The programming language used to build the backend of the application.
- [Django](https://www.djangoproject.com/download/) - The web framework that powers the server-side logic, database models, and URL routing.
- [Visual Studio Code](https://code.visualstudio.com/) -  A lightweight, flexible code editor recommended for writing and managing the project code.
- [Django Widget Tweaks](https://pypi.org/project/django-widget-tweaks/) - A Django template tag library used to customize form fields directly in templates.
- [Django Filter](https://pypi.org/project/django-filter/) - Adds filtering capabilities to Django views, making it easy to implement search and filter functionality.
- [Requests](https://pypi.org/project/requests/) - A simple and elegant HTTP library for Python, used to send HTTP/1.1 requests with methods like GET and POST. It simplifies interacting with external APIs.

### Installing

Create and initialize a virtual environment (optional)

    pip install virtualenv
    virtualenv ticket_env
    cd ticket_env
    Scripts\activate

Clone the Repository

    clone https://github.com/chidiohiri/django-ticket.git
    cd django-ticket

Move the project into the virtual environment, then install dependencies. The project dependencies can found in [requirements.txt](requirements.txt)

    pip install -r requirements.txt

Migrate all tables to the Sqlite3 DB

    python manage.py makemigrations
    python manage.py migrate

Create/Login to Paystack account, and get secret and public key, then add it to the settings.py file (see file ending)

    PAYSTACK_SECRET_KEY = ''
    PAYSTACK_PUBLIC_KEY = ''

Create a super user. This account will be used to access the admin dashboard and verify objects.

    python manage.py createsuperuser

Run server on your terminal (cmd or powershell). Open your browser and navigate to http://127.0.0.1:8000/ to access the application.

    python manage.py runserver

### Core Features

- Ticket Creation with Wallet Deduction: Customers can only create tickets if their wallet balance covers the ticket cost. The system automatically deducts the specified amount from the wallet and logs the ticket.

- Role-Based Access Control: Access to features is restricted based on user roles. Customers can manage their own tickets, support engineers handle assigned tickets, and admins manage assignments and critical alerts.

- Ticket Filtering and Pagination: Custom filters and paginated views help users efficiently find and manage tickets relevant to them, improving usability for both customers and engineers.

- Critical Priority Alerts: If a ticket is marked as "Critical", an email is immediately sent to the admin for urgent attention, ensuring high-priority issues are not missed.

- Ticket Notes and Updates: Support engineers can add internal notes. Customers can edit their tickets if they are still pending. Resolved or pending tickets have restricted edit actions to preserve integrity.

- File Attachments: Customers can upload relevant files (screenshots, documents, etc.) to a ticket. Attachments are linked to the ticket and visible in the ticket detail view.

- Email Notifications: Automated emails are sent during key events such as ticket creation, resolution, and feedback—keeping users and admins informed throughout the process.

- Feedback and Rating System: Customers can submit feedback after ticket resolution. A 1-star rating automatically triggers an alert to the admin for review.

- Ticket Lifecycle Management: Tickets transition through statuses—Pending, Active, and Resolved. Resolved tickets can be reopened by customers for continued support if needed.

- Search Functionality: A simple keyword search allows users to look up tickets by title. Results are filtered based on user permissions and roles.

- Feedback Messaging: Clear user feedback via Django’s messaging framework helps guide and inform users through each action.

### Deployment

For production deployment, you will need to configure your application with a production-grade database (such as PostgreSQL), static file handling, and secure hosting. You may refer to the official [Django Documentation](https://docs.djangoproject.com/en/5.1/howto/deployment/) on deployment

### Authors

  - **Chidi Ohiri** - *For updates, networking, or feedback, feel free to connect:* -
    [Linkedin](https://www.linkedin.com/in/chidiebere-ohiri/)

### License

This project is licensed under the [MIT LICENSE](LICENSE.md), which permits reuse, modification, and distribution with proper attribution.

### Acknowledgments

  - Guido van Rossum, the creator of Python
  - The Django core team and community for building and maintaining such a robust framework
  - Developers and open-source contributors whose work inspired or supported the development of this project

