# Python Environment

Prepare an environment using `uv`

```bash
cd ./MCP-PowerPoint
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Execute the script

```bash
uv --directory "/Users/jesse/Documents/VSCode Projects/TrainingSessions/MCP-PowerPoint" run powerpoint_mcp_server_stable.py
```

OpenCode MCP configuration

```json
"mcp": {
    "powerpoint": {
      "type": "local",
      "command": ["uv","--directory","/Users/jesse/Documents/VSCode Projects/TrainingSessions/MCP-PowerPoint","run","powerpoint_mcp_server_stable.py"],
      "enabled": true
    }
  }
```