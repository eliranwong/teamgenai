# TeamGen AI

TeamGen AI, developed by [Eliran Wong](https://github.com/eliranwong), automates the creation of AI agent teams to address user requests.

## Version 2.0

Version 2.0+ is completely re-written, built-on [AgentMake AI](https://github.com/eliranwong/agentmake) SDK.

# How does it work?

Upon receiving a user request, TeamGen AI generates a team of AI agents, each with a distinct role. They were then assigned in turns to work collaborately in
a group discussion. During each turn of the group discussion, TeamGen AI evaluates the progress and assigns the most suitable agent to contribute. Once all agents have provided their expertise and the request is fully addressed, TeamGen AI engages the final answer writer to deliver the response to the user.

# Agentic Workflow

<img width="832" alt="Image" src="https://github.com/user-attachments/assets/cf27cf97-ea7a-42bd-a050-3663064dc07d" />

# AI Backends and Configurations

ToolMate AI uses [AgentMake AI](https://github.com/eliranwong/agentmake) configurations. The default AI backend is Ollama, but you can easily edit the default backend and other configurations. To configure, run:

> ai -ec

# Installation

> pip install teamgenai

Setting up a virtual environment is recommended, e.g.

```
python3 -m venv tgai
source tgai/bin/activate
pip install --upgrade teamgenai
# setup
ai -m
```

Install extra package `genai` to support backend Vertex AI via `google-genai` library:

```
python3 -m venv tgai
source tgai/bin/activate
pip install --upgrade "teamgenai[genai]"
# setup
ai -m
```

# Run TeamGen AI

Run TeamGen AI with command `teamgenai` or `tgai`.

Remarks: `tgai` is an alias to `teamgenai`.

For CLI options run:

> tgai -h

To enter your request in editor mode:

> tgai

To run with a single command, e.g.

> tgai Write a Christmas song

Result of this example: https://github.com/eliranwong/teamgenai/blob/main/examples/example_01.md

> tgai Write a comprehensive introduction to the book of Daniel in the bible

Results of this example, comparing different AI backends: https://github.com/eliranwong/teamgenai/tree/main/examples/example_02

# Welcome Contributions

You are welcome to make contributions to this project by:

* joining the development collaboratively

* donations to show support and invest for the future

Support link: https://www.paypal.me/toolmate

Please kindly report of any issues at https://github.com/eliranwong/teamgenai/issues
