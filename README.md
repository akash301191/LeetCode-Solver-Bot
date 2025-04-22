# LeetCode Solver Bot

LeetCode Solver Bot is a smart Streamlit application that reads LeetCode problem screenshots and generates clean, optimized code solutions along with step-by-step explanations. Powered by [Agno](https://github.com/agno-agi/agno) and OpenAI's GPT-4o, this bot enhances your coding workflow by turning visual prompts into precise, well-explained solutions.

## Folder Structure

```
LeetCode-Solver-Bot/
├── leetcode-solver-bot.py
├── README.md
└── requirements.txt
```

- **leetcode-solver-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Screenshot-Based Input**  
  Upload a screenshot of any LeetCode problem to get started—no manual copy-pasting needed.

- **Solution Preferences**  
  Choose your desired programming language, solution style (e.g., beginner-friendly, step-by-step), and explanation depth.

- **AI-Powered Problem Solving**  
  The LeetCode Solver agent uses GPT-4o to read the screenshot, understand the problem, and generate a complete solution.

- **Structured Markdown Output**  
  The solution is presented in a consistent format with clear headers:
  - 💻 **Solution**
  - 📘 **Explanation**
  - Optional: complexity analysis and learning links

- **Download Option**  
  Save the solution and explanation as a `.md` file for future use.

- **Streamlined UI**  
  Built with Streamlit to ensure a clean, responsive, and intuitive experience for developers.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/LeetCode-Solver-Bot.git
   cd LeetCode-Solver-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run leetcode-solver-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI API key in the sidebar.
   - Upload a screenshot of a LeetCode question.
   - Choose your solution and explanation preferences.
   - Click **🚀 Generate Solution**.
   - View or download the formatted solution and explanation.

3. **Download Option**  
   Use the **📥 Download Solution** button to save the generated content as a Markdown file.

---

## Code Overview

- **`render_solution_preferences()`**:  
  Collects user input, including the uploaded image, language preference, and explanation depth.

- **`generate_solution()`**:  
  - Uses Agno’s `Agent` abstraction to run the LeetCode Solver agent.
  - Reads the screenshot and generates both code and explanation.
  - Formats the output using consistent Markdown sections.

- **`render_sidebar()`**:  
  Captures and stores the OpenAI API key securely using Streamlit session state.

- **`main()`**:  
  Manages the layout, user interaction, and full app flow from upload to output.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Please ensure your changes are well-documented, modular, and aligned with the app’s purpose.