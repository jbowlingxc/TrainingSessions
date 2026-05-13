# AGENTS.md

## 🚀 Presentation Generation Workflow

Use OpenCode to generate new technical presentations by referencing the master template and specifying a destination.

1.  **Reference Template**: Always use `templates/presentation_generator.md` as context.
2.  **Instruction Format**: Provide:
    *   **Topic**: Subject matter and specific requirements (e.g., "Include a demo of X").
    *   **Destination**: Target folder within the `sessions/` directory (e.g., `sessions/my-new-topic/`).

## 📂 Output Structure

OpenCode must generate exactly three files in the destination folder:

1.  `[Topic]_Presentation.md` (**Layout**):
    *   Contains structural guide, slides, and demo breaks.
    *   Uses `---` separators between sections.
2.  `[Topic]_Presentation_Script.md` (**Narrative**):
    *   Word-for-word script for the presenter.
    *   **MUST match** the layout file's sections and slides exactly.
    *   **CRITICAL**: Every 'Image' description from File 1 must be explicitly referenced or described in this text.
    *   Includes technical readiness checklist and stage directions (e.g., `(Switch to shared screen)`).
3.  `[Topic]_Reference_Doc.md` (**Wiki.JS Documentation**):
    *   Comprehensive deep-dive resource for Wiki.JS.
    *   **CRITICAL**: Insert a single HTML `<br>` tag on its own line **before every header section** (except the first).
    *   Use Wiki.JS callout syntax: `> text\n{.is-info}` (or `.is-success`, `.is-warning`, `.is-danger`).

## 🛠️ Key Constraints

*   **Pacing**: Total presentation time should be ~1 hour.
*   **Demos**: Allocate approximately **30 minutes** of the total time for demonstrations.
*   **Tone**: Professional, engaging, and authoritative.
*   **Clarity**: Expand all acronyms; use analogies where appropriate.
