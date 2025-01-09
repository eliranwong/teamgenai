# TeamGen AI

TeamGen AI, developed by [Eliran Wong](https://github.com/eliranwong), automates the creation of AI agent teams to address user requests.

# How does it work?

Upon receiving a user request, TeamGen AI generates a team of AI agents, each with a distinct role. They were then assigned in turns to work collaborately in
a group discussion. During each turn of the group discussion, TeamGen AI evaluates the progress and assigns the most suitable agent to contribute. Once all agents have provided their expertise and the request is fully addressed, TeamGen AI engages the final answer writer to deliver the response to the user.

# Supported AI Backends

The following AI Backends are supported and tested:

`anthropic`, `azure`, `genai`, `googleai`, `groq`, `llamacppserver`, `mistral`, `ollama`, `openai`, `xai`

Compare at: https://github.com/eliranwong/teamgenai/tree/main/examples/example_02

# Latest Features

Read https://github.com/eliranwong/teamgenai/blob/main/latest.md

# Requirements

To run TeamGen AI, you need to install and setup [ToolMate AI](https://github.com/eliranwong/toolmate) (version 0.6.34 or later) FIRST!

To install:

> pip install --upgrade toolmate

To install on Android Termux:

> pip install --upgrade toolmate_lite

To setup ToolMate AI:

> tmsetup -m

Select AI a backend and a model. Enter API keys if the selected backend requires.

Note: We are using `toolmate` as a library to quicken the initial development of this project. We may consider removing this requirement as this project grow.

# Installation

> pip install teamgenai

We recommend creating a virtual environment first, e.g.

```
python3 -m venv tgai
source tgai/bin/activate
pip install --upgrade toolmate teamgenai
# setup ToolMate AI
tmsetup -m
```

Install `toolmate_lite` instead of `toolmate` on Android Termux, e.g.

```
python3 -m venv tgai
source tgai/bin/activate
pip install --upgrade toolmate_lite teamgenai
# setup ToolMate AI
tmsetup -m
```

# Run TeamGen AI

Run TeamGen AI with command: `tgai` 

For CLI options run:

> tgai -h

To enter your request in interactive mode:

> tgai

To run with a single command, e.g.

> tgai Write a Christmas song

Result of this example: https://github.com/eliranwong/teamgenai/blob/main/examples/example_01.md

> tgai Write a comprehensive introduction to the book of Daniel in the bible

Results of this example, comparing different AI backends: https://github.com/eliranwong/teamgenai/tree/main/examples/example_02

# Development Road Map

1. Creat an initial version that support group discussion between AI agents (Done! version 0.0.2)
2. Support backup and reuse of generated agent configurations (Done! version 0.0.2)
3. Test all the [AI backends supported by ToolMate AI](https://github.com/eliranwong/toolmate#ai-backends-and-models) ([Done!](https://github.com/eliranwong/teamgenai/tree/main/examples/example_02))
4. Support specifying different AI backends or models for running agent creation, assignment and responses
5. Support customisation of core system messages that run TeamGen AI (Done! version 0.0.3)
6. Support code generation and task execution
7. Integrate `ToolMate AI` tools and plugins
8. May remove dependency on `ToolMate AI`
9. More ...

Welcome further suggestions!

# Welcome Contributions

You are welcome to make contributions to this project by:

* joining the development collaboratively

* donations to show support and invest for the future

Support link: https://www.paypal.me/toolmate

Please kindly report of any issues at https://github.com/eliranwong/teamgenai/issues