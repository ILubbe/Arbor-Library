# Arbor Library Web Application

## Summary
This Web Application was built for the fictional "Arbor Library".

It consists of 5 components:

- Frontend container, a UI built with Angular, and served with Nginx for user interaction.
- Backend Container: Built with the Flask Python Framework, responsible for core business logic.
- Database Container: Utilizes MariaDB to store data that is important to the Library's operation.
- Search Engine Container: Utilizes ElasticSearch to provide a word search for end users in the UI.
- Cache Container: Utilizes Redis to store authorization/authentication tokens

## 📖 Documentation

- **[User Guide](docs/userguide.md)** – Learn how to use the application.
- **[Design Document](docs/design.md)** – Understand the technical design and architecture.

## Local Deployment and Important Maintenance Notes
- Clone the repository at https://gitlab.com/wgu-gitlab-environment/student-repos/ilubbe2/d424-software-engineering-capstone.git
- Install Docker Engine and Compose.

### Local Deployment
- First change directory to ./deploy/local

- To build the frontend and backend container images:
    - docker compose build

- To deploy the full application stack:
    - docker compose up -d

- To stop the application stack:
    - docker compose down

- Reach the UI on _http://localhost:8080_

- A variable within deploy/local/compose.yml for the backend service named **SEED_BOOK_COUNT** controls the number of books pulled from https://openlibrary.org when an empty database is detected at boot.
    - Please Note:
        - **_This is sample data_**
        - The larger the count, the longer the backend container takes to begin accepting API requests.

### Important Maintence Notes
- The Default Admin's credentials are as follows. **Please Change The Password!**
    - Email: _defaultadmin@arbor-library.click_
    - Password: _admin_

_Version 1.0.3_