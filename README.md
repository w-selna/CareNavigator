# CareNavigator
A toy group project for an AI Agent to diagnose a disease, and find you a doctor to treat it in your area and medical network.

## Features
- Disease diagnosis
- Doctor search and matching
- Medical network integration

## Installation
This project is based on the Google ADK (Agent Development Kit).

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/w-selna/CareNavigator.git
   cd CareNavigator
   ```
2. Install Google ADK:
   ```bash
   pip install google-adk
   ```
3. (Optional) Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install other dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```
5. Configure your environment as needed for Google ADK (API keys, etc.).

Refer to the [Google ADK documentation](https://github.com/google/adk) for more details and advanced configuration.

## Usage
After setting up the repository and installing Google ADK, you can use the CareNavigator agents as follows:

1. **Activate your virtual environment** (if you created one):
   ```bash
   source venv/bin/activate
   ```

2. **Run the agents**
   - Each agent is implemented as a Python module in the `CareNav-app` directory (e.g., `diagnosis_agent`, `maps_agent`, `search_agent`, `root_agent`).
   - You can run or import these agents in your own Python scripts, or extend them as needed.

3. **Example: Running an agent**
   ```python
   from CareNav-app.diagnosis_agent import agent as diagnosis_agent
   ...
   ```

4. **Using Google ADK**
   - The agents leverage Google ADK for agent orchestration, LLM integration, and tool management.
   - Start the adk web procedure from the repo. ```adk web```
   - Navigate to http://127.0.0.1:8000/ where the agent UI is listening from.
   - Select root_agent from drpo down and prompt accordingly.
   - You can refer to the [Google ADK documentation](https://github.com/google/adk) for advanced usage, such as configuring agent workflows, adding new tools, or integrating with other services.

5. **Environment Variables**
   - Some features may require API keys or other environment variables. Set these in your shell or `.bashrc` as needed.

Feel free to explore and modify the agents to suit your needs!

## Contributing
This is a toy project for a class. It is not being monitored. Please do not feel like you need to contribute further to this work, just fork it and build on your own.

## License
N/A
