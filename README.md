# Arbor Library Web Application

## Summary
This Web Application was built for a fictional library "Arbor Library". It consists of 5 components:

- A frontend container, a UI built with Angular, and served with Nginx.
- A backend container, built with the Flask Python Framework, responsible for core business logic.
- A database container, which utilizes MariaDB, to store User, Book, Reservation, Checkout, and Genre tables.
- A search engine container, which utilizes ElasticSearch to provide a word search to users in the UI.
- A cache container, which utilizes Redis to store revoked JSON web tokens once a user logs out or refreshes their page.

## 📖 Documentation

- **[User Guide](docs/userguide.md)** – Learn how to use the application.
- **[Design Document](docs/design.md)** – Understand the technical design and architecture.