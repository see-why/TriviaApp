# API Development and Documentation Final Project

## Trivia App

This is a complete web application that can be used to hold trivia and seeing who's the most knowledgeable of the bunch. The application:

1. Display questions - both all questions and by category.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

The codes are written using [PEP 8 style guide](https://peps.python.org/pep-0008/). 

### Backend

The [backend](./backend/README.md) directory contains a completed Flask and SQLAlchemy server. The work is primarily in `__init__.py` with defined endpoints and reference models.py for DB and SQLAlchemy setup.

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server.

Pay special attention to what data the frontend is expecting from each API response. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

> View the [Frontend README](./frontend/README.md) for more details.

### Arthur

👤 **Cyril Iyadi**

- GitHub: [@see-why](https://github.com/see-why)
- LinkedIn: [C.Iyadi](https://www.linkedin.com/in/cyril-iyadi/)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](../../issues/).

## Show your support

Give a ⭐️ if you like this project!

## Acknowledgments
- Caryn McCarthy [@cmccarthy15](https://github.com/cmccarthy15), for a great course content
## 📝 License
- This project is [MIT](./LICENSE) licensed.