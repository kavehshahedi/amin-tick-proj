# TicketAssist

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.27+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

TicketAssist is a comprehensive ticket management and support platform powered by LLMs, designed for telecom and 5G network operations teams. It combines AI-driven chatbot assistance with advanced ticket tracking and visualization capabilities.

## Features

### 🔐 Authentication System
- Secure login with username/password authentication
- Session management for persistent user experience
- Role-based access control (admin/user)

### 💬 AI-Powered Chatbot
- Integrated LLM support via Ollama
- Context-aware responses for technical questions
- Support for various LLM models including Llama3
- Customizable parameters (temperature, top_p, etc.)
- Persistent chat history
- User feedback collection mechanism

### 📱 5G Ticket Management
- Comprehensive ticket visualization dashboard
- Advanced filtering and sorting capabilities
- Real-time ticket status tracking
- Priority-based ticket highlighting
- Detailed ticket information with solutions
- Support for multiple 5G network components and projects
- Export functionality (CSV, JSON, Excel)

### 🎨 User Experience
- Responsive design
- Dark/light mode toggle
- Customizable views
- Interactive card-based UI
- Tooltips and helpful indicators

## Installation

### Prerequisites
- Python 3.9 or higher
- [Ollama](https://ollama.ai/) (for LLM support)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ticketassist.git
cd ticketassist
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Ollama (if using the chatbot feature):
```bash
# Install Ollama from https://ollama.ai/
ollama pull llama3.1:8b
```

5. Create required directories:
```bash
mkdir -p data/.streamlit
```

## Usage

### Running the Application

Start the Streamlit application:
```bash
streamlit run main_page.py
```

### Authentication

Default credentials:
- Username: `admin`
- Password: `admin`

### Navigation

The application consists of three main components:
1. **Main Dashboard** - Overview and welcome page
2. **Chatbot** - AI-powered assistance for troubleshooting
3. **Ticket Management** - Visualization and management of 5G tickets

## Project Structure

```
TicketAssist/
├── .gitignore
├── main_page.py             # Main entry point with authentication
├── requirements.txt         # Project dependencies
├── pages/
│   ├── 1_chat_bot_page.py   # Chatbot interface
│   └── 2_ticket_page.py     # 5G ticket management system
└── utils/
    ├── auth.py              # Authentication utilities
    ├── chat.py              # Chat functionality and LLM service
    ├── styles.py            # CSS and JS styling utilities
    └── ticket.py            # Ticket data models and utilities
```

## Technologies

- **Frontend**: Streamlit, HTML, CSS, JavaScript
- **Backend**: Python
- **AI/ML**: Ollama, Llama3 LLM
- **Data Processing**: Pandas, NumPy
- **Data Storage**: Shelve (for chat history)
- **Typing**: Python type hints, Pydantic

## Configuration

For custom configuration, create a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#1e88e5"
backgroundColor = "#f5f5f5"
secondaryBackgroundColor = "#ffffff"
textColor = "#262730"
font = "sans serif"
```

## Development

### Type Checking

The project uses type hints throughout. You can check types with:

```bash
mypy .
```

### Code Formatting

Format code using:

```bash
black .
isort .
```

## Use Cases

TicketAssist is designed for:

1. **Network Operations Centers (NOCs)** - Track and manage 5G network issues
2. **Technical Support Teams** - Leverage AI for faster troubleshooting
3. **Network Engineers** - Document and share solutions for common issues
4. **Product Managers** - Track issue priorities and resolutions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the web framework
- [Ollama](https://ollama.ai/) for LLM integration capabilities
- All open-source libraries used in this project

---

Created with ❤️ for telecom operations teams