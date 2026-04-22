# AGENTS.md

## Repo structure

- **Empty workspace** — used as a root for generating training sessions via the `workshop-creator` skill.
- No source code, build config, or tests exist here.

## Workshop creator skill

Located at `.opencode/skills/workshop-creator/SKILL.md`. Key conventions:

- Topic folder name: max 3 words, lowercase snake_case.
- All file/folder names: lowercase snake_case.
- Audience: IT infrastructure engineers with wide experience range.
- Verify subtopic list with the user **before** generating files.
- Output: `{topic}/DOCUMENT.md` + `{topic}/solutions/` with commented scripts covering all subtopics together when possible.
