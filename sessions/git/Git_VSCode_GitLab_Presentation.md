### **Presentation: Mastering Git with VSCode and GitLab**

---

#### **Section 1: Setup & Foundations (10 mins)**

**Slide 1: Introduction & Configuration**
- **Content**:
    - Git Identity: Setting `user.name` and `user.email` for proper attribution.
    - Authentication: Understanding SSH vs. HTTPS for secure communication with GitLab.
    - Core Terminologies: Repository, Staging Area, Commit, Branch, and HEAD.
- **Image**: A diagram showing the relationship between a local repository, the staging area, and the working directory.
- **Speaker Notes**: Welcome everyone. Before we dive into code, we must ensure our identity is correctly configured so every contribution is properly attributed in GitLab.

**Slide 2: The Repository Environment**
- **Content**:
    - The `.gitignore` file: Preventing sensitive secrets (API keys) and large build artifacts from being tracked.
    - The Git Workflow: Working Directory $\rightarrow$ Stashing/Staging $\rightarrow$ Local Commit $\rightarrow$ Remote Push.
- **Image**: A screenshot of a `.gitignore` file in VSCode highlighting ignored patterns like `*.env` or `node_modules/`.
- **Speaker Notes**: Never commit secrets! The `.gitignore` is your first line of defense for repository hygiene.

---

#### **Section 2: Local Development & Branching (15 mins)**

**Slide 3: Mastering the Local Commit**
- **Content**:
    - Atomic Commits: Making small, single-purpose commits to simplify debugging and reverts.
    - VSCode Diff Tool: Using the side-by-side view to inspect changes before staging.
    - Git Stash: Temporarily "shelving" uncommitted work to switch branches quickly without losing progress.
- **Image**: A screenshot of the VSCode Source Control view showing a side-by-side diff comparison between two file versions.
- **Speaker Notes**: Good commits are like good sentences; they should convey one clear idea. Use the built-in VSCode diff tool to double-check your work before you commit.

**Slide 4: Branching Strategies**
- **Content**:
    - The Main Branch: The source of truth for production-ready code.
    - Understanding Divergence: What happens when local and remote branches drift apart.
    - Strategies: GitFlow (feature/develop/release) vs. GitLab Flow (simpler, branch-per-environment).
- **Image**: A visual timeline showing a main branch diverging into multiple feature branches and eventually merging back.
- **Speaker Notes**: Branching is how we work in parallel without stepping on each other's toes.

---

#### **[DEMO BREAK 1: Local Workflow in VSCode] (10 mins)**

**Goal**: Demonstrate a complete local cycle: Create $\rightarrow$ Diff $\rightarrow$ Stage $\rightarrow$ Atomic Commit $\rightarrow$ Stash/Pop.

**Step-by-Step Instructions**:
1. Open a new repository in VSCode.
2. Create a new file `feature.txt` with some content.
3. Use the Source Control view to inspect the diff of the new file.
4. Stage the file using the `+` icon.
5. Commit the change with an atomic message: "feat: add initial feature file".
6. Modify the file again, then use `git stash` via the command palette.
7. Switch to a different branch (or simulate a context switch).
8. Use `git stash pop` to bring the changes back.

**Code/Config Blocks**:
```bash
git checkout -b feature-branch
git stash
git checkout main
git stash pop
```

**Narration Notes**: Show how easy it is to see exactly what changed in VSCode before clicking commit. Emphas and then show the "magic" of stashing when a sudden task arrives.

---

#### **Section 3: Synchronization & Advanced Git Actions (15 mins)**

**Slide 5: Moving Data Between Local and Remote**
- **Content**:
    - Fetch vs. Pull: `git fetch` downloads metadata; `git pull` downloads and attempts to merge.
    - Push & Publish: Sending your local commits to the GitLab remote repository.
- **Image**: An infographic showing data flowing from a Local Repository to a Remote (GitLab) icon.
- **Speaker Notes**: Always fetch before you pull to see what others have done without forcing a merge on yourself immediately.

**Slide 6: Advanced Operations in VSCode**
- **Content**:
    - Rebase: Rewriting history for a cleaner, linear commit log.
    - Prune: Cleaning up local references to branches that no longer exist on remote.
    - Fast-Forward vs. Three-Way Merges: Understanding how Git handles branch integration.
- **Image**: A comparison diagram showing a "messy" merge history (spiderweb) vs. a "clean" rebased history (linear).
- **Speaker Notes**: Rebase is powerful but use it with caution on shared branches. It keeps our history readable.

---

#### **Section 4: GitLab Collaboration & CI/CD (15 mins)**

**Slide 7: The Merge Request (MR) Lifecycle**
- **Content**:
    - Creating MRs: The gateway to code review.
    - Description Templates: Using templates to ensure all necessary info (testing, impact) is provided.
    - Linking Issues: Using `Closes #123` to automate GitLab issue transitions.
- **Image**: A screenshot of a well-formatted GitLab Merge Request page with a description template in use.

- **Speaker Notes**: An MR is more than just code; it's documentation for your reviewers.

**Slide 8: Conflict Resolution & Safety**
- **Content**:
    - Identifying Conflicts: When two people change the same line.
    - Resolving in VSCode: Using the Merge Editor to pick incoming or current changes.
    - Reverting MRs: How to safely undo a merge that broke production.
- **Image**: A screenshot of the VSCode Merge Editor showing "Accept Current" and "Accept Incoming" buttons.
- **Speaker Notes**: Don't panic when you see conflict markers. VSCode makes resolving them much safer than manual text editing.

**Slide 9: Automation with Pipelines**
- **Content**:
    - GitLab Pipelines: Automated testing and deployment triggered by commits.
    - Triggers: How MRs or tags can kick off specific CI/CD workflows.
    - Git Hooks: Using pre-commit hooks to run linters locally before the push.
- **Image**: A GitLab Pipeline graph showing stages like `build`, `test`, and `deploy` passing successfully.
- **Speaker Notes**: The pipeline is our safety net, ensuring that every commit meets our quality standards automatically.

---

#### **[DEMO BREAK 2: The Collaboration Loop] (10 mins)**

**Goal**: Demonstrate a collaborative cycle: Branch $\rightarrow$ Introduce Conflict $\rightarrow$ Resolve in VSCode $\rightarrow$ Push $\rightarrow$ Create MR with Template $\rightarrow$ Trigger Pipeline.

**Step-by-Step Instructions**:
1. On `feature-branch`, modify a line that exists on `main`.
2. Switch to `main` and modify the *same* line differently.
3. Attempt to merge `feature-branch` into `main` in VSCode.
4. Use the VSCode Merge Editor to resolve the conflict.
5. Push the resolved branch to GitLab.
6. Open a Merge Request in the GitLab web UI using a template.
7. Show the resulting Pipeline running in GitLab.

**Code/Config Blocks**:
```bash
# Simulating conflict
git checkout main
echo "conflict line" >> file.txt
git checkout feature-branch
echo "different conflict line" >> file.txt
git merge main
```

**Narration Notes**: This is the "daily driver" workflow for any engineer. Highlight how the tools guide you through the hardest parts of Git.
