# 🛡️ Snyk Agent Scan: Securely Auditing MCP Servers & Skills

When working with the Model Context Protocol (MCP), you are essentially granting LLM agents the ability to execute code and access system resources via tools. This introduces significant security risks, including prompt injection, tool poisoning, and malware execution.

The [Snyk Agent Scan](https://github.com/snyk/agent-scan) tool is designed to audit these components in a low-risk manner, allowing you to inspect MCP configurations and dependencies before fully integrating them into your production or development workflow.

<br>

## ⚠️ The Security Mandate: "Scan Before You Run"

The most critical rule of MCP security is: **Never run an untrusted MCP server without verification.** 

Standard execution starts the `stdio` process, which can trigger malicious payloads. Snyk Agent Scan allows you to perform a security audit by inspecting the configuration and dependencies *before* granting full system access.

<br>

## 🔍 Core Use Cases for Lab Environments

### 1. Auditing MCP Configuration Files (`mcp_settings.json`)
Before adding a new server to your Claude Desktop, Cursor, or Windsurf configuration, use Agent Scan to verify the `command` and `args` parameters.

**How to scan:**
```bash
# Replace with the path to your specific config file
export SNYK_TOKEN=your-api-token-here
uvx snyk-agent-scan@latest scan path/to/mcp_settings.json
```

**What it checks:**
*   **Command Integrity:** Ensures the executable being called is expected.
*   **Argument Analysis:** Inspects arguments for suspicious patterns or hidden flags.
*   **Tool Poisoning:** Analyzes tool definitions for instructions that could be hijacked via prompt injection.

<br>

### 2. Securely Scanning NPM & Pip Packages
Many MCP servers rely on `npm` (Node.js) or `pip` (Python) packages. Running `npm install` or `pip install` directly on untrusted code can execute malicious post-install scripts. Agent Scan provides a way to inspect these components.

**For NPM-based Servers:**
Inspect the `package.json` and its dependency tree for known vulnerabilities without downloading and executing the package contents.
```bash
# Use Snyk's ability to audit node dependencies via the agent scan workflow
uvx snyk-agent-string@latest scan path/to/npm_mcp_server/
```

**For Pip-based Servers:**
Audit Python-based MCP servers by scanning their `requirements.txt` or `pyproject.toml`.
```bash
# Scan the python environment configuration
uvx snyk-agent-scan@latest scan path/to/python_mcp_server/
```

<br>

### 3. Auditing Agent Skills (Markdown/Prompt Files)
Agent "Skills" are often just text files containing instructions. These are highly susceptible to **Indirect Prompt Injection**.

**How to scan:**
```bash
# Scan a specific skill file for malicious prompt patterns
uvx snyk-agent-scan@latest scan ~/path/to/my_skill.md
```

<br>

## 🛠️ Implementation Strategy: The "Sandbox Workflow"

To achieve the goal of **minimal risk and setup** in a lab environment, follow this three-step workflow:

| Step | Action | Tool/Environment | Goal |
| :--- | :--- | :--- | :--- |
| **1. Isolation** | Spin up a disposable Docker container or VM. | Docker / Vagrant | Ensure no host system access if a leak occurs. |
| **2. Audit** | Run `snyk-agent-scan` against the downloaded MCP repo/config. | Snyk Agent Scan | Identify Prompt Injection, Tool Poisoning, or Malicious Payloads. |
| **3. Integration** | Only move the verified configuration to your primary dev machine. | Manual / Scripted | Minimize the attack surface of your local workstation. |

<br>

## 💡 Pro-Tips for IT Professionals

> [!TIP]
> **Use `--no-skills` if you only care about MCP servers.** If you are specifically testing a new tool and not looking at prompt-based skills, use this flag to speed up the scan and reduce noise.

> [!WARNING]
> **Never use `--dangerously-run-mcp-servers` in your main environment.** This flag bypass's the interactive consent prompt and automatically executes the commands defined in the config. Use it **only** inside your isolated sandbox during the audit phase.

<br>

## 📖 Glossary of Terms (Security Focus)
* **Prompt Injection:** Malicious instructions hidden in data that hijack the LLM's logic.
* **Tool Poisoning:** Modifying an MCP tool's description to trick the agent into performing unauthorized actions.
* **Toxic Flows:** A sequence of tool calls designed to cause harm or extract secrets.
* **Agent Skill:** A specialized set of instructions (often in Markdown) that teaches an agent a new capability.
