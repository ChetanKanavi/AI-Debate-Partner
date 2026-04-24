# 🗣️ AI Debate Partner

An intelligent, interactive debate application built with Python and Streamlit, powered by the Google Gemini API. 

This application acts as a sophisticated sparring partner to help you test your arguments, identify logical fallacies, and strengthen your understanding of any topic.

## ✨ Features

*   **Dual Personas:**
    *   **The Opponent:** A ruthless debater that will challenge your assertions, demand evidence, and find logical flaws in your arguments.
    *   **The Coach:** A supportive mentor that points out weaknesses in your reasoning not to defeat you, but to help you build a stronger, more bulletproof argument.
*   **Dynamic Knowledge Assessment:** As you chat, the AI silently assesses your depth of knowledge and logical strength. It uses this "Hidden Profile" to tailor its responses, ensuring it challenges a beginner on fundamentals while attacking the nuance of an expert's argument.
*   **Rate-Limit Resilient:** Includes built-in exponential backoff to gracefully handle API limits.

## 🛠️ Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/)
*   **AI Engine:** Google Gemini API (`gemini-2.5-flash` model for high-speed, robust reasoning)
*   **Language:** Python 3.10+

## 🚀 Getting Started

Follow these steps to run the application locally on your machine.

### Prerequisites
*   Python 3.10 or higher installed.
*   A Google Gemini API key (You can get one for free at [Google AI Studio](https://aistudio.google.com/)).

### Installation

1. **Clone the repository (or download the files):**
   ```bash
   git clone https://github.com/your-username/ai-debate-partner.git
   cd ai-debate-partner
   ```
   *(Note: Replace `your-username` with your actual GitHub username once uploaded)*

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   * **On Windows:**
     ```powershell
     .\venv\Scripts\activate
     ```
   * **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your environment variables:**
   * Create a file named `.env` in the root directory (you can copy the `.env.example` file).
   * Add your Gemini API key to the file:
     ```env
     GEMINI_API_KEY=your_actual_api_key_here
     ```

### Running the App

Once everything is installed and your API key is set, run the following command from the root folder:

```bash
streamlit run app.py
```

A new tab will automatically open in your default web browser containing the application.

## 💡 Usage

1. Open the sidebar on the left side of the screen.
2. Enter the **Debate Topic** you wish to discuss.
3. Select your desired **Persona** (Opponent or Coach).
4. Click **Apply & Reset Debate** to start a fresh session.
5. Enter your opening argument in the chat box at the bottom and begin the debate! You can expand the "Your Hidden Profile" section in the sidebar to see how the AI is currently evaluating your skill level.
