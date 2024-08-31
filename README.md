# Bank Loan Advisor RAG

The Bank Loan Advisor RAG is a Streamlit application designed to assist users with loan-related queries by leveraging a Retrieval-Augmented Generation model. The application retrieves relevant information from a predefined data directory and generates responses to user inquiries, covering topics like loan eligibility, interest rates, and required documentation.

## Features

- **Personalized Loan Advice**: Tailored answers for banking queries.
- **Retrieval-Augmented Generation**: Utilizes advanced NLP techniques.
- **User-Friendly Interface**: Easy setup and usage.
- **Configurable**: Set your OpenAI API key and data path via the sidebar.

## Prerequisites

- Python 3.8 or higher
- Streamlit
- OpenAI API access
- A directory of documents for the RAG model

  You can install all the required packages with this command:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

Clone the repository:

```bash
git clone https://github.com/saraAhangari/Streamlit-chatbot.git
cd Streamlit-chatbot
```

## Steps to Run the Application

1. **Set Up OpenAI API Key**: Add your OpenAI API key in the `secrets.toml` file located in the `.streamlit` folder.
2. **Set Up the Database**: Run the Docker compose file in the `Data` folder to configure the database.
   ```bash
   docker-compose -f Data/docker-compose.yml up
   ```
3. **Run the Application**: Navigate to the `src` directory and run the `main.py` file Streamlit app:

   ```bash
   streamlit run src/main.py
   ```

