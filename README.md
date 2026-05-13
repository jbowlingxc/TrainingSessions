# Technical Presentation Workshop Repository

This repository contains structured materials for technical training sessions, including presentation layouts, speaker scripts, and deep-dive reference documentation.

## 🚀 Generating New Presentations with OpenCode

You can use **OpenCode** to automate the creation of new presentation materials by referencing the existing template as context. This eliminates the need to manually copy templates.

### The Workflow

To generate a new presentation, provide OpenCode with a single instruction that includes:
1.  **Context**: Reference `templates/presentation_generator.md`.
2.  **Topic**: Define the subject matter and any specific requirements (e.g., "Include a demo of X").
3.  **Destination**: Specify the target folder within the `sessions/` directory.

### Example Command

You can prompt OpenCode as follows:

> "Using the instructions in `templates/presentation_generator.md`, generate a presentation about **Kubernetes Fundamentals**. Include a demo of `kubectl` commands. Save the resulting three files into `sessions/kubernetes/`."

### 📂 Expected File Output Structure

OpenCode will generate three files which should be organized as follows:
- `sessions/[topic]/[Topic]_Presentation.md`
- `sessions/[topic]/[Topic]_Presentation_Script.md`
- `sessions/[topic]/[Topic]_Reference_Doc.md`

## 📂 Repository Organization

- `templates/`: Contains master templates and LLM instruction sets.
- `sessions/`: The primary library of training content, organized by technology or topic (e.g., `sessions/mcp/`, `rag/`).
