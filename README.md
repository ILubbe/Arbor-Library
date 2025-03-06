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