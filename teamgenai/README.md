# TeamGen AI

TeamGen AI automates the creation of AI agent teams to address user requests.

Upon receiving a user request, TeamGen AI generates tailor-made teams of AI agents that collaborate to resolve the request.

# Developer

[Eliran Wong](https://github.com/eliranwong)

# Latest Features

Read https://github.com/eliranwong/teamgenai/latest.md

# Requirements

To run TeamGen AI, you need to install and setup [ToolMate AI](https://github.com/eliranwong/toolmate) (version 0.6.30 or later) FIRST!

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

Command: `tgai` 

For CLI options run:

> tgai -h

To enter your request in interactive mode:

> tgai

To run with a single command, e.g.

> tgai Write a Christmas song

Result of this example: https://github.com/eliranwong/teamgenai/example_01.md

> tgai Write a comprehensive introduction to the book of Daniel in the bible

Result of this example: https://github.com/eliranwong/teamgenai/example_02.md

# Development Road Map

1. Creat an initial version that support group discussion between AI agents (Done! version 0.0.2)
2. Support backup and reuse of generated agent configurations (Done! version 0.0.2)
3. Test all the [AI backends supported by ToolMate AI](https://github.com/eliranwong/toolmate#ai-backends-and-models) (Partially done! Tested backends: `openai`, `github`, `azure`)
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