# LMStudio

MCP Settings file location on Mac: `~/.lmstudio/mcp.json`

Install `npq` for auditing packages prior to installation.

```bash
npm install -g npq
```

```json
{
  "mcpServers": {
    // https://github.com/weather-mcp/weather-mcp
    // npm view @dangahagan/weather-mcp versions
    // npq install @dangahagan/weather-mcp@1.6.1
    "weather": {
      "command": "npm",
      "args": [
        "exec",
        "@dangahagan/weather-mcp@1.6.1"
      ],
      "env": {
        "ENABLED_TOOLS": "full",
        "CACHE_MAX_SIZE": "2000",
        "LOG_LEVEL": "1"
      }
    },
    // https://github.com/modelcontextprotocol/servers/tree/main/src/everything
    // npm view @modelcontextprotocol/server-everything versions
    // npq install @modelcontextprotocol/server-everything@2026.1.26
    "everything": {
      "command": "npm",
      "args": [
        "exec",
        "@modelcontextprotocol/server-everything@2026.1.26"
      ]
    },
    // Work with Messages app on MacOs -- Requires full disk access...
    // https://mcpservers.org/servers/carterlasalle/mac_messages_mcp
    "messages": {
      "command": "uvx",
      "args": [
        "mac-messages-mcp"
      ]
    },
    // Using a local container for PowerShell Universal with MCP plugin enabled.
    // https://docs.powershelluniversal.com/platform/plugins/mcp-server
    "psu": {
      "url": "http://localhost:5001/api/v1/mcp"
    }
  }
}
```

# Snyk Agent Scanning

Must have `uv` package manager for Python installed. (https://docs.astral.sh/uv/)

```bash
uvx snyk-agent-scan@latest
```

Get an API key. It's free for personal use.
(https://snyk.io/blog/introducing-agent-security/)

Usage:
(https://github.com/snyk/agent-scan)

```bash
# Set the API key
export SNYK_TOKEN="your-api-key"
```

Perform a scan for LMStudio settings

```bash
uvx snyk-agent-scan@latest "~/.lmstudio/mcp.json"
```