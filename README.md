# 🐾 ADK Pet Mate AI

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

### Command-Line Parameters

The application supports the following command-line options:

- **`-d, --debug`**: Enable debug output
- **`-v, --verbose`**: Enable verbose output (displays current model when enabled)
- **`-l, --log-level`**: Set logging level (choices: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Default: `ERROR`
- **`-m, --model`**: Select the AI model to use. Available options:
  - `gemini-2.5-flash-lite` (default)
  - `gemini-2.5-flash`
  - `gemini-2.0-flash-lite`
  - `gemini-2.0-flash`

**Example usage**:
```bash
python pet_mate/main.py --verbose --log-level INFO --model gemini-2.5-flash
```

### Running Jupyter Notebooks

```bash
jupyter lab --no-browser
```

Then open the `notebooks/dima.ipynb` notebook in your browser.

## 📁 Project Structure

```
adk-pets/
├── pet_mate/              # Main application package
│   ├── main.py           # Application entry point
│   ├── settings.py       # Configuration and CLI parameters
│   ├── agents/           # AI agent implementations
│   │   └── care_advisor/ # Pet care advice agent
│   └── flows/            # Application flow management
├── evaluation/           # Agent evaluation and testing
```

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
