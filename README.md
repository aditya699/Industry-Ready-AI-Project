# RAG-based Chatbot

This project implements a Retrieval-Augmented Generation (RAG) chatbot using Gemini embeddings and Flask.

## Demo

Here are some screenshots of the chatbot in action:

![RAG Chatbot Demo 1](https://saibaba9758140479.blob.core.windows.net/testimages/ragcb1.PNG)

![RAG Chatbot Demo 2](https://saibaba9758140479.blob.core.windows.net/testimages/ragcb2.PNG)

## Project Structure

- `src/`: Source code for the RAG chatbot
- `templates/`: HTML templates for the web interface
- `.gitignore`: Specifies intentionally untracked files to ignore
- `LICENSE`: Project license file
- `README.md`: This file, providing project overview and instructions
- `app.py`: Main Flask application file
- `requirements.txt`: List of Python dependencies
- `setup.sh`: Setup script for the project
- `templates.py`: Handles Gemini embeddings

## Features

- Web-based chat interface
- RAG-powered responses using Gemini embeddings
- Flask backend for handling requests and integrating components

## Prerequisites

- Python 3.8+
- Flask
- Gemini API access (API key required)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/aditya699/rag-chatbot.git
   cd rag-chatbot
   ```

2. Run the setup script:
   ```
   bash setup.sh
   ```

   This script will likely set up your environment and install dependencies.

3. Set up your Gemini API key:
   - Create a `.env` file in the project root (it should be git-ignored)
   - Add your API key: `GEMINI_API_KEY=your_api_key_here`

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to the provided local address (typically `http://localhost:5000`)

3. Start chatting with the RAG-powered bot!

## Customization

- Modify files in the `templates/` directory to change the chat interface
- Adjust RAG parameters and Gemini embeddings in `templates.py`
- Update the main application logic in `app.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the license specified in the LICENSE file.