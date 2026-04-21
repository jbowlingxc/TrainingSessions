# Workshop Creator Skill

This skill automates the creation of a training session folder and content based on a specific topic.

## Workflow

When triggered with a topic, the skill performs the following steps:

1. **Folder Creation**:
   - Create a new folder using `snake_case` naming convention corresponding to the topic (e.g., `terraform_basics`).

2. **Content Generation (`topic_name.md`)**:
   - Generate a `topic_name.md` file containing:
     - **Summary**: A concise explanation of the topic and its importance to IT Infrastructure Engineers.
     - **Audience**: Specifically targeted at IT Infrastructure Engineers with mixed automation experience.
     - **Learning Objectives**: A thorough breakdown of the specific concepts and techniques to be covered.
     - **References**: At least three links to authoritative, 3rd-party documentation.

3. **Demonstration Assets**:
   - Within the topic folder, create a `solution` subfolder.
   - Generate one or more scripts or files that demonstrate the lessons outlined in the `.md` file.
   - **Requirements for Assets**:
     - Provide real-world use cases.
     - Cover all topics mentioned in the `.md` file.
     - Include detailed comments explaining each component or line of code.

4. **Standardization**:
   - Ensure all naming conventions adhere to `snake_case`.
   - Ensure all files are organized logically within the topic folder.
