# Presentation Script: Mastering Git with VSCode and GitLab

## Technical Readiness Checklist
- [ ] Verify screen sharing permissions are active in Microsoft Teams.
- [ ] Verify audio/video connection is stable; mute all non-presenters.
- [ ] Ensure VSCode is open with a test Git repository initialized.
- [ ] Ensure GitLab access is active and the web interface is loaded.
- [ ] Confirm that a terminal (zsh/bash) is ready for quick command execution.

---

## Section 1: Setup & Foundations (10 mins)

### Slide 1: Introduction & Configuration
**(Digital/Teams cue: "(Check audio/video connection)")**

"Hello everyone, and welcome to our session on Mastering Git with VSCode and GitLab. Before we start writing code, we need to talk about identity. Have you ever looked at a commit history and wondered why someone's name is just 'user123'? It usually comes down to configuration. We use `git config` to set our `user.name` and `current.email`. This ensures that every contribution is properly attributed in GitLab, which is vital for accountability in team environments."

**(Digital/Teams cue: "(Reference the diagram showing local repo, staging, and working directory)")**

"As you can see in this diagram, Git isn't just one place; it's a movement of data. You have your Working Directory where you edit files, the Staging Area where you prepare changes, and the Local Repository where those changes are permanently recorded as commits. Understanding this flow is the key to avoiding mistakes."

"We also need to talk about security. As shown in this screenshot of a `.gitignore` file, we use this file to tell Git: 'Hey, don't track these files.' This is your first line of defense against accidentally leaking API keys or committing massive `node_modules` folders that would bloat our repository."

---

### Slide 2: The Repository Environment
**(Digital/Teams cue: "(Pause for chat questions)")**

"The core workflow follows a very specific path. You work on a file, you stage it, you commit it locally, and finally, you push it to the remote server—in our case, GitLab. It's like preparing a package: the working directory is your packing station, staging is putting items in the box, and pushing is actually handing that box to the courier."

---

## Section 					2: Local Development & Branching (15 mins)

### Slide 3: Mastering the Local Commit
"Now, let's talk about quality. We strive for 'Atomic Commits.' Think of an atomic commit like a single, clear sentence in an essay. It should do one thing and one thing only. If you fix a bug and add a feature in one commit, it becomes much harder to revert that fix later without losing the feature."

**(Digital/Teams cue: "(Reference the VSCode side-by-side diff screenshot)")**

"To achieve this, we leverage the incredible tools inside VSCode. Before you even click 'Stage,' use the side-by-side diff tool. It allows you to inspect every single character change. This prevents the classic mistake of accidentally committing a `console.log` or a piece of debug code."

"And what if you're in the middle of something, but a high-priority bug comes in? You don't have to commit half-finished work. Use `git stash`. It effectively 'shelves' your current changes, giving you a clean slate to switch branches, and then you can 'pop' them back later when you're ready."

### Slide  $\rightarrow$ 4: Branching Strategies
"Branching is where the magic happens. The `main` branch is our source of truth—it should always be stable and deployable. But we don't work directly on it. We create branches."

**(Digital/Teams cue: "(Reference the branching timeline diagram)")**

"As you can see in this timeline, features diverge from the main line, progress independently, and eventually merge back. Depending on your team, you might use GitFlow, which is quite structured with development and release branches, or GitLab Flow, which is much simpler and focuses on environment-based branches. There is no 'right' way, only the way that works for your team's velocity."

---

#### **[DEMO BREAK 1: Local Workflow in VSCode] (10 mins)**

"**(Switch to shared screen for demo)** Let's jump into a live environment. I'm going to show you how we go from an empty file to a staged and committed change, all without leaving the VSCode interface."

"**Goal**: Demonstrate a complete local cycle: Create $\rightarrow$ Diff $\rightarrow$ Stage $\rightarrow$ Atomic Commit $\rightarrow$ Stash/Pop."

"**Step-by-Step Instructions**:
1. I'll start by creating `feature.txt`. 
2. Notice how the Source Control icon shows a 'U' for untracked.
3. Let's click it to see the diff. See how clean it is?
4. Now, I'll stage it using this plus sign.
5. Time for an atomic commit. I'll type 'feat: add initial feature file'.
6. Now, watch this: I'll add some messy code, then run `git stash` in the terminal. 
7. Look! My working directory is clean again, even though I didn't commit that mess.
8. Finally, I'll bring it back with `git stash pop`."

"**Narration Notes**: Emphasize how much visibility the VSCode UI provides compared to just using the command line alone. Point out the 'Staged Changes' section specifically."

---

## Section 3: Synchronization & Advanced Git Actions (15 mins)

### Slide 5: Moving Data Between Local and Remote
"Once your work is committed locally, it's still only on your machine. To share it, we need to move data between your local repo and GitLab. You'll often hear the terms 'Fetch' and 'Pull.' A `fetch` is like checking your mailbox to see if there's mail, but not opening it yet. A `pull` is like fetching the mail AND immediately opening it and putting it on your desk. Use `fetch` when you want to see what others have done without risking a merge conflict right away."

**(Digital/Teams cue: "(Reference the infographic of data flow)")**

"As shown here, the flow goes from Local to Remote via 'Push' and 'Publish.' This is how we populate GitLab with our hard work."

### Slide 6: Advanced Operations in VSCode
"For more advanced users, we have `rebase` and `prune`. Rebase is a way to rewrite your history. Instead of having a messy web of merge commits, rebase allows you to move your changes to the tip of the main branch, creating a beautiful, linear history."

**(Digital/Teams cue: "(Reference the comparison diagram of messy vs. clean history)")**

"Compare these two diagrams. The left one is what happens with standard merges—it's a spiderweb. The right one is the result of rebasing—a single, easy-to-read line. It makes debugging much easier."

"We also use `prune` to keep our local environment clean by removing references to branches that have already been deleted on GitLab. And finally, understanding Fast-Forward vs. Three-Way merges helps you understand how Git decides whether to just move a pointer or create a new merge commit."

---

## Section 4: GitLab Collaboration & CI/CD (15 mins)

### Slide 7: The Merge Request (MR) Lifecycle
"The Merge Request is the heart of GitLab collaboration. It's where code review happens. To make reviews efficient, we use Description Templates. This ensures every developer provides the same vital information, like testing steps or impact analysis."

**(Digital and Teams cue: "(Reference the screenshot of a well-formatted MR)")**

"And here is a pro-tip: if you link your MR to an issue by writing `Closes #123` in the description, GitLab will automatically close that issue once the MR is merged. It's seamless automation."

### Slide 8: Conflict Resolution & Safety
"We've all been there: you try to merge and—BAM—conflict. VSCode makes this much less scary with its built-in Merge Editor."

**(Digital/Teams cue: "(Reference the VSCode Merge Editor screenshot)")**

"As you can see in this screenshot, you are presented with clear choices: 'Accept Current,' 'Accept Incoming,' or even a manual resolution. It takes the guesswork out of the process."

"If a merge goes wrong and breaks production, don't panic. You can use the 'Revert' feature in GitLab to safely roll back the changes and restore stability."

### Slide 9: Automation with Pipelines
"Finally, let's talk about the safety net: GitLab Pipelines. Every time you push code, a pipeline can trigger. This automates our testing, linting, and even deployment."

**(Digital/Teams cue: "(Reference the GitLab Pipeline graph)")**

"As shown in this graph, we have distinct stages: Build, Test, and Deploy. If any stage fails, the pipeline stops, preventing broken code from reaching production. We can even use Git Hooks locally to run these same checks before you even attempt a push."

---

#### **[DEMO BREAK 2: The Collaboration Loop] (10 mins)**

"**(Switch to shared screen for demo)** Now, let's put everything together in one big collaborative loop. This is what a typical day looks like."

"**Goal**: Demonstrate a collaborative cycle: Branch $\rightarrow$ Introduce Conflict $\rightarrow$ Resolve in VSCode $\rightarrow$ Push $\rightarrow$ Create MR with Template $\rightarrow$ Trigger Pipeline."

"**Step-by-Step Instructions**:
1. I'll create a new branch called `feature-conflict`.
2. I'll modify a line in `file.txt` on this branch.
3. Now, I'll switch to `main` and change that *same* line differently.
4. I'll try to merge the feature branch into main using VSCode.
5. Watch as VSCode prompts me with the Merge Editor conflict! I'll resolve it now.
6. Once resolved, I'll push this to GitLab.
7. Now, I'll go to the GitLab web interface and create a Merge Request. 
8. Notice how the description template is already there for me to fill out.
9. Finally, let's watch the magic happen as the Pipeline starts running automatically."

"**Narration Notes**: This is the most important part of the presentation. Show the 'stress' of the conflict and the 'relief' of the resolution. The connection between the local VSCode action and the remote GitLab pipeline is the 'Aha!' moment."
