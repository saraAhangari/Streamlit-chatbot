# Bank Loan Advisor RAG

The Bank Loan Advisor RAG is a Streamlit application designed to assist users with inquiries related to obtaining loans from a bank. Leveraging the power of the Retrieval-Augmented Generation model, this application provides personalized advice by retrieving relevant information from a predefined data directory and generating responses to user queries. Whether you're looking for information on loan eligibility, interest rates, or document requirements, the Bank Loan Advisor is here to guide you through the maze of banking procedures with ease and clarity.
There's two python files in this reposiroty:
- streamlit_app.py : you need to set your own openai_key and data directory
- loan_adviser.py : you can set the necessary information in secrets.tomel and this python file and use the chatbot directly. 


## Features

- **Personalized Loan Advice**: Get answers tailored to your specific banking queries.
- **Retrieval-Augmented Generation**: Uses advanced NLP techniques for accurate and relevant responses.
- **User-Friendly Interface**: Simple and intuitive UI, making it easy for anyone to get started.
- **Configurable**: Set your OpenAI API key and data directory path directly through the application's sidebar.

## Prerequisites

Before running the Bank Loan Advisor RAG, ensure you have the following:

- Python 3.8 or higher
- Streamlit
- Access to OpenAI API
- A set of documents in a directory that the RAG model will use to retrieve information. This should be organized in a way that the model can navigate and extract relevant data for loan-related queries.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/saraAhangari/Streamlit-chatbot.git
cd Streamlit-chatbot
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage
To run the application, navigate to the project directory and execute the following command. Don;t forget to replace the "script_name" with the actual file name you want to run:

```bash
streamlit run script_name.py
```

After launching the application, if you're running streamlit_app.py follow these steps:

1. Input your **OpenAI API key** in the sidebar. This is required for the RAG model to generate responses.
2. Specify the **data directory path** where your loan-related documents are stored. The application will use these documents to retrieve information and assist users with their queries.
3. Use the chat interface to ask any questions related to obtaining a loan from a bank.
