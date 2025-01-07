from toolmate import config, readTextFile
from toolmate.utils.call_llm import CallLLM
from toolmate.utils.streaming_word_wrapper import StreamingWordWrapper
from teamgenai import packageFolder
from teamgenai.utils.shared_utils import saveRecord
import os, re, argparse
try:
    import readline
except:
    pass

def main():
    parser = argparse.ArgumentParser(description = """TeamGen AI CLI options.""")
    parser.add_argument("default", nargs="*", default=None, help="user request")
    parser.add_argument("-a", "--agents", action="store", dest="agents", help="the file path of a previously saved copy of agents' configurations")
    args = parser.parse_args()

    print("# Running TeamGen AI ...")
    print(f"# AI Backend\n{config.llmInterface}\n")

    # streaming parameter
    openai = True if config.llmInterface in ("openai", "letmedoit", "github", "azure", "googleai", "xai", "groq", "mistral", "llamacppserver") else False

    # user request
    userRequest = " ".join(args.default) if args.default else ""
    if userRequest := userRequest.strip():
        print(f"# User request\n{userRequest}\n")
    else:
        userRequest = input("Enter your request: ")
    config.currentMessages = [{"role": "system", "content": ""}, {"role": "user", "content": userRequest}]

    # agent configurations
    if args.agents and os.path.isfile(args.agents):
        agents = eval(readTextFile(args.agents))
    else: # generate a team of AI agents
        custom_system_create_agents_file = os.path.join(config.localStorage, "teamgenai", "system", "core", "create_agents.txt")
        system_create_agents_file = custom_system_create_agents_file if os.path.isfile(custom_system_create_agents_file) else os.path.join(packageFolder, "system", "core", "create_agents.txt")
        config.tempChatSystemMessage = readTextFile(system_create_agents_file)
        create_agents_response = CallLLM.getSingleChatResponse(None, messages=config.currentMessages, keepSystemMessage=False) # use system: create_agents
        agents = [i.rstrip() for i in create_agents_response.split("```") if re.search("^agent [0-9]", i)]

    # agent description
    agents_description = "```" + "```\n\n```".join(agents) + "```"
    print("# Agents Generated")
    print(agents_description, "\n")

    # Agent assignment
    custom_system_assign_agents_file = os.path.join(config.localStorage, "teamgenai", "system", "core", "assign_agents.txt")
    system_assign_agents_file = custom_system_assign_agents_file if os.path.isfile(custom_system_assign_agents_file) else os.path.join(packageFolder, "system", "core", "assign_agents.txt")
    assign_agents = readTextFile(system_assign_agents_file).format(userRequest, agents_description)
    agent = 1

    while len(agents) >= agent > 0:
        config.tempChatSystemMessage = assign_agents
        assign_agents_response = CallLLM.getSingleChatResponse(None, messages=config.currentMessages, keepSystemMessage=False) # use system: assign_agents

        print("# Assignment")
        print(assign_agents_response, "\n")

        p = r"The best agent to work next is agent ([0-9]+?)[^0-9]"
        if found := re.search(p, assign_agents_response):
            agent = int(found.group(1))
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
            
            print(f"# Calling Agent {agent} ...")
            print(config.tempChatSystemMessage, "\n")

            if len(config.currentMessages) == 2: # at the beginning
                config.currentMessages.append({
                    "role": "assistant",
                    "content": "# Progress\nA team of AI agents has been created to resolve your requests. Pending assignments of the AI agents to work on your request...",
                })
            config.currentMessages.append({
                "role": "user",
                "content": f"# Assignment\n{agent_role} It is your turn to contribute.",
            })
            completion = CallLLM.regularCall(config.currentMessages)
            StreamingWordWrapper().streamOutputs(None, completion, openai=openai)
        else:
            print("Group discussion terminated unexpectedly.")
            agent = 0

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