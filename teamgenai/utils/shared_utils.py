from toolmate import config, writeTextFile, getCurrentDateTime
from pathlib import Path
import os

def saveRecord(userRequest, agents, agents_description):
    timestamp = getCurrentDateTime()
    storagePath = os.path.join(config.localStorage, "teamgenai", timestamp)
    Path(storagePath).mkdir(parents=True, exist_ok=True)
    print()
    print("# User Request Resolved")
    agents_description_file = os.path.join(storagePath, "agents_configurations.py")
    print(f"Saving agents' configurations in '{agents_description_file}' ...")
    writeTextFile(agents_description_file, str(agents))
    agents_discussion_file = os.path.join(storagePath, "agents_discussion.py")
    print(f"Saving agents discussion in '{agents_discussion_file}' ...")
    writeTextFile(agents_discussion_file, str(config.currentMessages))
    plain_record_file = os.path.join(storagePath, "plain_record.md")
    plain_record = f"""# Datetime

{timestamp}

# AI Backend

{config.llmInterface}

# User Request

{userRequest}

# Agents Generated

{agents_description}

# Agents Discussion
"""
    for i in config.currentMessages:
        role = i.get("role", "")
        content = i.get("content", "")
        if content:
            plain_record += f"""
```{role}
{content}
```
"""
    print(f"Saving plain record in '{plain_record_file}' ...")
    writeTextFile(plain_record_file, plain_record)
    print("Done!")
    try:
        os.system(f'''{config.open} "{plain_record_file}"''')
    except:
        pass