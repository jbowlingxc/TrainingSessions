---
name: workshop-creator
description: Automates the creation of a training session folder and content based on a specific topic.
---

# Workshop Creator Skill

This skill automates the creation of a training session folder and content based on a specific topic.

## Workflow

Create a list of subtopics related to the topic in the prompt provided and include any specific subtopics referenced in the prompt.

All documentation has an intended audience of IT infrastructure engineers with wide ranges of experience.

Verify the list of topics with the user before generating any files.

All file and folder names must be lowercase and use snake casing.

Determine a topic name no more than three words long. Create a folder with this name.

Create a markdown file in the new folder named DOCUMENT.md that contains:
- An introduction to the topic
- A breakdown of each subtopic that includes an explanation of what it is and how to apply it, if applicable. Use code blocks to show examples and be thoroughly descriptive.
- Conclude the document with a list of authoritative external references related to the topic and subtopics.

Create a folder named solutions within the topic folder. Generate examples of the various subtopics in this folder.
- these are most commonly scripts but can be other types of practical examples of the topic in action.
- Use detailed comments to explain each action or command in the example.
- Multiple subtopics should be covered together whenever possible to demonstrate how they work together.
- Each subtopic must appear at least once in these examples.