# 🐾 ADK Pet Care Assistant

> An intelligent pet care guidance system built with Google ADK, providing personalized advice and care recommendations for your beloved pets.

## ✨ Features

- **Intelligent Pet Care Advice**: AI-powered guidance for pet health and wellbeing
- **Multi-Agent Architecture**: Specialized agents for different aspects of pet care
- **Interactive Flow System**: Seamless conversation flow for better user experience
- **Google ADK Integration**: Powered by advanced language models

## 🛠️ Technologies

- **Python 3.12+**
- **Google ADK 1.18.0** - AI Development Kit
- **Google GenAI 1.49.0** - Generative AI capabilities
- **Asyncio** - Asynchronous programming support

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd adk-pets
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   
   Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   
   Add your Google API key to the `.env` file:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   
   > 📝 **Note**: Get your API key from the [Google ADK documentation](https://google.github.io/adk-docs/get-started/python/#set-your-api-key)

4. **Verify installation**:
   ```bash
   python --version  # Should be 3.12+
   ```

## 🚀 Usage

### Running the Main Application

```bash
python pet_mate/main.py
```

### Running Jupyter Notebooks

```bash
jupyter lab --no-browser
```

Then open the `notebooks/dima.ipynb` notebook in your browser.

## 📁 Project Structure

```
adk-pets/
├── 📄 README.md                    # Project documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 main.py                      # Root application entry point
│
├── 🐾 pet_mate/                    # Main application package
│   ├── 📄 main.py                  # Application entry point
│   ├── 📄 logger.py                # Logging utilities
│   │
│   ├── 🤖 agents/                  # AI agent implementations
│   │   ├── 📄 common.py            # Shared agent utilities
│   │   ├── 💡 care_advisor/        # Pet care advice agent
│   │   ├── 📋 guidance_reviewer/   # Guidance validation agent
│   │   ├── 🔍 guidence_researcher/ # Research and fact-checking
│   │   └── 📝 guidance writer/     # Guidance providing advice
|   |   └── 📝 instruction_provider/# Instruction generation
│   │
│   └── 🔄 flows/                   # Application flow management
│       └── 📄 guidance.py
        └── 📄 flow.py 
│
├── 📓 notebooks/                   # Jupyter notebooks for experimentation
│   └── 📄 dima.ipynb              # Development notebook
│
└── 🛠️ utils/                       # Utility functions
    └── 📄 adk_utils.py
    └── 📄 sqlite_memory.py         # memory service
```

### Key Components

- **`pet_mate/main.py`**: Main application entry point with state management and flow orchestration
- **`pet_mate/agents/`**: Modular AI agents for different pet care aspects
- **`pet_mate/flows/`**: Conversation flow management and user interaction logic
- **`utils/adk_utils.py`**: Google ADK utilities and configuration helpers
- **`notebooks/`**: Development and testing notebooks

## 🧪 Testing

### Web UI Testing

The easiest way to test the agents is through the ADK Web UI:

```bash
# Start the web interface
./start_web.sh

# Or manually:
adk web evaluation/agents --port 8002
```

Then open http://localhost:8002 in your browser to:
- Chat with agents interactively
- Run predefined test cases
- View evaluation results
- Create new test scenarios

### Test Cases Included

- **Guidance Writer Agent**: 4 test cases covering dog limping, cat feeding, appetite loss, and behavioral changes
- **Guidance Reviewer Agent**: 6 test cases for evaluating advice quality, safety, and completeness

## 👥 Authors

- **Shery Khanlar** 
- **Mohnish Harisinganey**
- **Nilesh Jariwala**
- **Dmytro Nahornyi**
