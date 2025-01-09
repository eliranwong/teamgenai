from toolmate import config, readTextFile, writeTextFile
from toolmate.eTextEdit import launch
from toolmate.utils.call_llm import CallLLM
from toolmate.utils.streaming_word_wrapper import StreamingWordWrapper
from teamgenai import packageFolder
from teamgenai.utils.shared_utils import saveRecord
import os, re, argparse, sys

def main():
    parser = argparse.ArgumentParser(description = """TeamGen AI CLI options.""")
    parser.add_argument("default", nargs="*", default=None, help="user request")
    parser.add_argument("-a", "--agents", action="store", dest="agents", help="the file path of a previously saved copy of agents' configurations")
    parser.add_argument('-ed', '--editor', action='store_true', dest='editor', help=f"""edit instruction with text editor; configured editor: {config.customTextEditor if config.customTextEditor else "etextedit"}""")
    parser.add_argument('-edcmd', '--editorcommand', action='store', dest='editorcommand', help="specify editor command; edit instruction with this editor command instead of configured editor")
    args = parser.parse_args()

    print("# Running TeamGen AI ...")
    print(f"# AI Backend\n{config.llmInterface}\n")

    # streaming parameter
    openai = True if config.llmInterface in ("openai", "letmedoit", "github", "azure", "googleai", "xai", "groq", "mistral", "llamacppserver") else False

    # user request
    stdin_text = sys.stdin.read() if not sys.stdin.isatty() else ""
    userRequest = " ".join(args.default) if args.default else ""
    userRequest = userRequest.strip()
    if stdin_text:
        userRequest += f" {stdin_text}"
    # edit request with text editor
    if not userRequest or args.editor or args.editorcommand:
        if config.customTextEditor or args.editorcommand:
            tempTextFile = os.path.join(config.toolMateAIFolder, "temp", "edit_request")
            writeTextFile(tempTextFile, userRequest)
            customTextEditor = args.editorcommand if args.editorcommand else config.customTextEditor
            os.system(f"{customTextEditor} {tempTextFile}")
            userRequest = readTextFile(tempTextFile)
        else:
            userRequest = launch(input_text=userRequest, filename=None, exitWithoutSaving=True, customTitle="Edit instruction below; exit when you finish")
    # display user request
    print(f"# User request\n{userRequest}\n")
    # set initial message chain
    config.currentMessages = [{"role": "system", "content": ""}, {"role": "user", "content": userRequest}]

    # agent configurations
    if args.agents and os.path.isfile(args.agents):
        agents = eval(readTextFile(args.agents))
    else: # generate a team of AI agents
        custom_system_create_agents_file = os.path.join(config.localStorage, "teamgenai", "system", "core", "create_agents.txt")
        system_create_agents_file = custom_system_create_agents_file if os.path.isfile(custom_system_create_agents_file) else os.path.join(packageFolder, "system", "core", "create_agents.txt")
        config.tempChatSystemMessage = readTextFile(system_create_agents_file) # use system: create_agents
        create_agents_response = CallLLM.getSingleChatResponse(None, messages=config.currentMessages, keepSystemMessage=False)
        create_agents_response = re.sub("```\n[Aa]gent", "```agent", create_agents_response)
        create_agents_response = re.sub("^[#]+? [Aa]gent", "```agent", create_agents_response, flags=re.M)
        agents = [i.rstrip() for i in create_agents_response.split("```") if re.search("^agent [0-9]", i)]
    if not agents:
        if config.developer:
            print(f"Agents not found in:\n\n{create_agents_response}")
        else:
            print("Agents not found!")
        exit(1)
    notCalled = [i for i in range(1, len(agents)+1)] # a list of agents that haven't been called
    config.currentMessages.append({
        "role": "assistant",
        "content": "# Progress\nA team of AI agents has been created to resolve your requests, and they are waiting for your call to contribute in turn.",
    })

    # agent description
    agents_description = "```" + "\n```\n\n```".join(agents) + "\n```"
    print("# Agents Generated")
    print(agents_description, "\n")

    # Agent assignment
    custom_system_assign_agents_file = os.path.join(config.localStorage, "teamgenai", "system", "core", "assign_agents.txt")
    system_assign_agents_file = custom_system_assign_agents_file if os.path.isfile(custom_system_assign_agents_file) else os.path.join(packageFolder, "system", "core", "assign_agents.txt")
    assign_agents = readTextFile(system_assign_agents_file).format(userRequest, agents_description)
    agent = 1

    while len(agents) >= agent > 0:
        config.tempChatSystemMessage = assign_agents # use system: assign_agents
        assign_agents_response = CallLLM.getSingleChatResponse(None, messages=config.currentMessages+[{"role": "user", "content": "Who is the best agent to contribute next?"}], keepSystemMessage=False)
        if assign_agents_response is None:
            assign_agents_response = ""

        print("# Assignment")
        print(assign_agents_response, "\n")

        p = r"The best agent to contribute next is agent ([0-9]+?)[^0-9]"
        if found := re.search(p, assign_agents_response):
            agent = int(found.group(1))
            if agent > len(agents):
                agent = 0
            elif agent in notCalled:
                notCalled.remove(agent)
        elif notCalled:
            agent = notCalled.pop(0)
        else:
            agent = 0
        if agent == 0 and notCalled:
            agent = notCalled.pop(0)
        if agent == 0:
            break

        config.tempChatSystemMessage = re.sub("^agent [0-9]+?\n", "", agents[agent - 1]).replace("##", "#") + f"""# User request
{userRequest}
# Instruction
1. Examine carefully what has been done or dicussed so far toward resolving the user request and think about what is the best to do next.
2. On top of what has been done or discussed, contribute your expertise to work toward resolving the user request."""
        try:
            agent_role = re.search("""# Role(.+?)# Job description""", config.tempChatSystemMessage, re.DOTALL).group(1).strip()
        except:
            agent_role = f"Agent {agent}"
        agent_role = re.sub("^You are (a|an|the) (.*?)[.]*$", r"\2", agent_role)
        
        print(f"# Calling Agent {agent} ...")
        print(config.tempChatSystemMessage, "\n")

        config.currentMessages.append({
            "role": "user",
            "content": f'''# Change Speaker\nThe best agent to contribute next is agent {agent}.\n{agent_role}, It is your turn to contribute.''',
        })
        completion = CallLLM.regularCall(config.currentMessages)
        StreamingWordWrapper().streamOutputs(None, completion, openai=openai)

    # Conclusion
    config.currentMessages.append({
        "role": "user",
        "content": f"""# Instruction
Please provide me with the final answer to my original request based on the work that has been completed.

# Original Request
{userRequest}""",
    })
    custom_system_write_final_answer_file = os.path.join(config.localStorage, "teamgenai", "system", "core", "write_final_answer.txt")
    system_write_final_answer_file = custom_system_write_final_answer_file if os.path.isfile(custom_system_write_final_answer_file) else os.path.join(packageFolder, "system", "core", "write_final_answer.txt")
    config.tempChatSystemMessage = readTextFile(system_write_final_answer_file)
    completion = CallLLM.regularCall(config.currentMessages)
    StreamingWordWrapper().streamOutputs(None, completion, openai=openai)

    # backup before closing
    saveRecord(userRequest, agents, agents_description)
    print("Closing ...")

if __name__ == '__main__':
    main()