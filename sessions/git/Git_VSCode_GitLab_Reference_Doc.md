# Mastering Git with VSCode and GitLab: The Complete Guide

<br>

## 📖 Introduction

This documentation serves as a deep-dive resource for engineers working within the Git/GitLab ecosystem using Visual Studio Code. Whether you are performing daily feature development or managing complex release cycles, this guide covers the essential workflows and best practices.

<br>

## 🛠 Prerequisites

Before following the advanced tutorials in this guide, ensure you have the following configured:

- [ ] **Git Installed**: Version 2.x or higher.
- [ ] **VSCode Installed**: Latest stable version with the "GitLens" extension (optional but highly recommended).
- [ ] **SSH Key Configured**: Ensure your public key is added to your GitLab profile for seamless authentication.
- [ ] **GitLab Access**: Permissions to create branches and Merge Requests in your target repository.

<br>

## 🚀 Core Workflow & Configuration

<br>

### Setting up your Identity

To ensure every commit is correctly attributed, configure your global Git settings:

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (must match your GitLab email)
git config --global user.email "your.email@example.com"
```

<br>

### The Importance of `.gitignore`

The `.gitignore` file is critical for repository health. It prevents sensitive information and unnecessary files from being tracked.

> [!IMPORTANT]
{.is-danger}
**Never commit secrets!** Always ensure `.env`, `*.pem`, and other credential files are included in your `.gitignore`.

**Common patterns to include:**
| Pattern | Description |
| :--- | :--- |
| `*.log` | All log files |
| `node_modules/` | Dependency folders |
| `.env` | Environment variables containing secrets |
| `dist/` or `build/` | Compiled build artifacts |

<br>

## 💻 Local Development Mastery

<br>

### Atomic Commits & The Diff Tool

The principle of **Atomic Commits** states that each commit should represent a single, logical change. This makes debugging much easier via `git revert`.

In VSCode, always use the **Source Control View** to review your changes.
1. Open the Source Control tab (`Ctrl+Shift+G`).
2. Click on a modified file to open the **Side-by-Side Diff**.
3. Inspect the "red" (removed) and "green" (added) lines.

<br>

### Using Git Stash for Context Switching

When you are in the middle of a feature but need to switch to a hotfix branch, use `stash`:

```bash
# Save your current uncommitted changes
git stash

# ... perform your urgent work on another branch ...

# Bring your changes back
git stash pop
```

<br>

## 🔄 Synchronization & Advanced Git

<br>

### Fetch vs. Pull

| Command | Action | Risk Level |
| :--- | :--- | :--- |
| `git fetch` | Downloads metadata from remote; does not change your local code. | **Low** (Safe) |
| `git pull` | Downloads and attempts to merge remote changes into your current branch. | **Medium** (Can cause conflicts) |

<br>

### Rebase: Maintaining a Clean History

Rebasing allows you to integrate changes from `main` into your feature branch by "replaying" your commits on top of the latest `main`.

```bash
git checkout feature-branch
git fetch origin
git rebase origin/main
```

> [!TIP]
{.is-info}
Use `rebase` to keep a linear, easy-to-read history. However, **never** rebase branches that have already been pushed to a shared remote repository, as this rewrites history and confuses teammates.

<br>

## 🤝 GitLab Collaboration & CI/CD

<br>

### The Merge Request (MR) Lifecycle

A Merge Request is the formal process of proposing code changes. To ensure high-quality reviews:

1. **Use Templates**: Always fill out the MR description template provided by your team.
2. **Link Issues**: Use keywords like `Clues #123` or `Fixes #456` to automate task management.
3. **Reviewer Feedback**: Address all comments before requesting a final approval.

<br>

### Resolating Merge Conflicts in VSCode

When two developers modify the same line, Git cannot decide which version is correct. Use the **VSCode Merge Editor**:

1. Identify the conflicted files in the Source Control tab.
2. Open the file; you will see `<<<<<<< HEAD` and `>>>>>>> branch-name`.
3. Click **"Resolve in Merge Editor"**.
4. Select **"Accept Current"**, **"Accept Incoming"**, or manually edit the result.

<br>

### GitLab Pipelines (CI/CD)

GitLab Pipelines automate the testing and deployment of your code. A typical pipeline includes:

- **Build**: Compiling code or installing dependencies.
- **Test**: Running unit, integration, and linting tests.
- **Deploy**: Pushing the verified code to staging or production environments.

<br>

## 📖 Glossary of Terms

| Term | Definition |
| :--- | :--- |
| **HEAD** | A pointer to the current checked-out branch/commit. |
| **Repository (Repo)** | The container for your project, including all history and files. |
| **Staging Area** | An intermediate area where changes are gathered before a commit. |
                | **Merge Request (MR)** | A request to merge one branch into another in GitLab. |
| **Prune** | The act of removing local references to branches that no longer exist on remote. |

<br>

## 🔗 External References

- [Official Git Documentation](https://git-scm.com/doc)
- [GitLab Workflow Guide](https://docs.gitlab.com/ee/topics/git/workflow.html)
- [VSCode Git Integration Guide](https://code.visualstudio.com/docs/sourcecontrol/overview)
