# AI-venger Paper Management 

This repository contains the backend code for the Paper Management Project, which is a web application that allows users to search, get recommendation and chat with research papers. The backend is built using Django, a Python web framework.

## Getting Started

### Prerequisites

- Python 3.x
- Django

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/NgToanRob/AI-venger-Paper-Management.git
2. Navigate to the project directory
    ```bash
   cd AI-venger-Paper-Management
3. Install the required dependencies using pip
   ```bash
   pip install -r requirements.txt
4. Set up the database by running migrations
   ```bash
   python manage.py migrate
5. Run the development server
   ```bash
   python manage.py runserver

## Usage

To use the Paper Search Project backend, follow these steps:

1. Access the admin interface at [http://localhost:8000/admin/](http://localhost:8000/admin/) to manage users, topics, and other data.
2. Utilize the following API endpoints to interact with the application:

    - **Search arXiv**: Use the `/home/api/search/` endpoint to search for research papers based on the user's query.

    - **Get Recommended Papers**: Access the `/home/api/recommended/` endpoint to retrieve recommended papers based on the user's interests.
    - **Chat with Papers**: Access the `/chatpaper/id` endpoint to chat with papers.

3. Integrate the backend with the frontend to create a user-friendly interface for paper search and recommendations.

## API Endpoints

- **Search arXiv**: Endpoint: `/home/api/search/`

    To search for research papers, make a GET request to this endpoint with the user's query.

    Example:
    ```
    GET /home/api/search/?query=deep%20learning
    ```

- **Get Recommended Papers**: Endpoint: `/home/api/recommended/`

    To get recommended papers, make a GET request to this endpoint with the user's interests.

    Example:
    ```
    GET /home/api/recommended/?interests=computer%20vision,neural%20networks
    ```
- **Chat with Papers**: Endpoint: `/chatpaper`

    To chat with papers, make a GET request to this endpoint with the paper id.

    Example:
    ```
    GET /chatpaper/?id=1234
    ```

Please note that you should replace placeholders like `http://localhost:8000` with the actual URL of your deployed backend. Ensure that you format the requests according to the API documentation for accurate results.
## Configuration

To configure the Paper Search Project backend according to your needs, consider the following steps:

- **Database Settings**: Customize your database settings in the `settings.py` file to match your preferred database setup.

- **Authentication**: Configure authentication settings to ensure secure access to the backend.

- **URL Routes**: Modify URL routes in your project's `urls.py` file to structure the API endpoints as desired.

- **App Configurations**: Adjust app-specific configurations in the `apps.py` file of each Django app in your project.

Feel free to explore and modify other settings in the project to align with your requirements.

## Contributing

We welcome contributions to the Paper Search Project backend!

## License
This project is licensed under the MIT License.