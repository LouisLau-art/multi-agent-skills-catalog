import json
import os

settings_path = os.path.expanduser("~/.claude/settings.json")
skills_dir = os.path.expanduser("~/.claude/skills")

try:
    with open(settings_path, "r") as f:
        settings = json.load(f)
except FileNotFoundError:
    settings = {}

if "hooks" not in settings:
    settings["hooks"] = {}

hooks = {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": f"bash {skills_dir}/self-improving-agent/hooks/pre-tool.sh \"$TOOL_NAME\" \"$TOOL_INPUT\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": f"bash {skills_dir}/self-improving-agent/hooks/post-bash.sh \"$TOOL_OUTPUT\" \"$EXIT_CODE\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": f"bash {skills_dir}/self-improving-agent/hooks/session-end.sh"
          }
        ]
      }
    ]
}

settings["hooks"].update(hooks)

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)

print("Updated ~/.claude/settings.json")
