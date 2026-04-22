# 🌳 Git & GitLab Training Guide

> **Audience:** IT Infrastructure Engineers (Ansible & Terraform workflows)
>
> This guide covers the Git fundamentals you need for day-to-day infrastructure-as-code collaboration on GitLab.

---

## 📋 Table of Contents

1. [The Main Branch — Your Source of Truth](#-the-main-branch--your-source-of-truth)
2. [Creating Branches](#-creating-branches)
3. [Managing Local Branches](#-managing-local-branches)
4. [Atomic Commits](#-atomic-commits)
5. [Commit Message Practices](#-commit-message-practices)
6. [Rebasing Your Work](#-rebasing-your-work)
7. [Creating Merge Requests](#-creating-merge-requests)
8. [Merge Request Message Practices](#-merge-request-message-practices)
9. [End-to-End Workflow Example](#-end-to-end-workflow-example)
10. [References](#-references)

---

## 🟢 The Main Branch — Your Source of Truth

The `main` branch is the single source of truth for your infrastructure codebase.

- **Always stable.** Anything on `main` should deploy without errors.
- **Never commit directly to `main`.** Use feature branches for all work.
- **Pull before you branch.** Always update your local `main` before creating a new branch.

```bash
git checkout main
git pull origin main
```

> 💡 **Why it matters for IaC:** A broken `main` means broken deployments. Terraform state and Ansible playbooks on `main` are what your CI/CD pipelines run against.

![main branch protection rules in GitLab](https://via.placeholder.com/800x300?text=GitLab+Branch+Protection+Settings)

---

## 🌿 Creating Branches

### When to create a branch

- Every new feature, bug fix, or infrastructure change gets its own branch.
- One branch = one logical change. Don't mix unrelated work.

### Naming convention

```
<type>/<short-description>
```

| Prefix      | Use case                                      | Example                              |
|-------------|-----------------------------------------------|--------------------------------------|
| `feature/`  | New infrastructure (VPC, IAM, roles)          | `feature/add-rds-instance`           |
| `fix/`      | Bug fixes to existing playbooks/modules        | `fix/ansible-timeout-error`          |
| `chore/`    | Dependencies, docs, CI config changes          | `chore/update-terraform-provider`    |
| `refactor/` | Restructuring without behavior change           | `refactor/terraform-module-layout`   |
| `docs/`     | Documentation updates                          | `docs/add-README-deployment-guide`   |

### Creating a branch

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create and switch to a new branch
git checkout -b feature/add-rds-instance
```

> 💡 **Pro tip:** You can also create a branch directly from the GitLab UI under **Repository > Branches > New branch**. This is useful when working from multiple machines.

![creating a branch in GitLab UI](https://via.placeholder.com/800x400?text=GitLab+Branch+Creation+UI)

---

## 🗂️ Managing Local Branches

### Viewing branches

```bash
# List all local branches (current branch marked with *)
git branch

# List all local and remote-tracking branches
git branch -a

# Show branches with last commit info
git branch -v
```

### Switching branches

```bash
git checkout feature/add-rds-instance
# Or with newer Git (2.23+):
git switch feature/add-rds-instance
```

### Deleting branches

```bash
# Delete a local branch (must not be on it)
git branch -d feature/add-rds-instance

# Force delete (if merge was rejected)
git branch -D feature/add-rds-instance

# Delete a remote branch
git push origin --delete feature/add-rds-instance
```

### Cleaning up stale branches

```bash
# Fetch and prune remote branches that no longer exist on the server
git fetch --prune

# Delete all local branches that have been merged and exist on remote
git branch --merged main | grep -v "^\*\|  main" | xargs git branch -d

# Delete remote branches that were already merged
git remote prune origin
```

### VS Code branch management

The VS Code Source Control panel (`Ctrl+Shift+G` / `Cmd+Shift+G`) provides a visual branch picker:

1. Click the branch name in the **status bar** (bottom-left).
2. Type to search existing branches or create a new one.
3. Use **Pull**, **Push**, **Create Branch**, and **Delete** from the context menu.

![VS Code branch picker](https://via.placeholder.com/600x350?text=VS+Code+Branch+Picker+UI)

---

## ⚛️ Atomic Commits

An **atomic commit** is a single, self-contained change that:

- Does **one thing** well.
- Leaves the codebase in a working state.
- Can be understood in isolation.

### ✅ Good atomic commits

```
commit abc1234 — Add RDS instance Terraform module
commit def5678 — Update Ansible inventory for new RDS host
commit ghi9012 — Add RDS monitoring alert in GitLab CI
```

### ❌ Bad non-atomic commits

```
commit jkl3456 — Fixed stuff, added RDS, updated docs, changed CI
```

### Why atomic commits matter for IaC

| Risk with squashed commits          | Benefit of atomic commits              |
|-------------------------------------|----------------------------------------|
| Hard to `git revert` a single issue | Revert only the problematic change     |
| `git blame` is useless              | Clear authorship and intent            |
| Code review is overwhelming         | Reviewable, focused diffs              |
| Merge conflicts are harder to resolve | Smaller, easier-to-resolve conflicts |

### Tips for atomic commits

- **Stage selectively** before committing:

  ```bash
  # Interactive staging — pick exactly what to include
  git add -p

  # Or stage specific files
  git add terraform/modules/rds/main.tf
  git add ansible/inventory/prod.yml
  ```

- **Commit frequently** during your work session. It's easier to organize later than to untangle a mess.
- **Amend the last commit** if you forgot something (before pushing):

  ```bash
  git add forgotten-file.tf
  git commit --amend --no-edit
  ```

---

## 📝 Commit Message Practices

### Format

```
<type>: <short summary>

<detailed description, if needed>

<optional footer: references, breaking changes>
```

### Guidelines

- **Summary line:** 50 characters or fewer, imperative mood ("Add" not "Added").
- **Body:** Wrap at 72 characters. Explain **why**, not **what** (the code shows what).
- **Separate summary from body** with a blank line.

### Examples

```
feat: add RDS instance Terraform module

Provision a PostgreSQL RDS instance in the prod VPC with
automated backups and maintenance windows.

Includes:
- Main module with subnet group and parameter group
- Outputs for endpoint, ARN, and identifier
- Variable overrides for environment-specific sizing

Refs: #42
```

```
fix: resolve Ansible timeout on EC2 provisioning

The connection timeout was too aggressive for large instance
launches. Increased from 30s to 120s in the ec2_provision
role defaults.

Closes: #38
```

### Conventional Commit types

| Type       | Meaning                                  |
|------------|------------------------------------------|
| `feat`     | New feature or resource                  |
| `fix`      | Bug fix                                  |
| `docs`     | Documentation only                       |
| `chore`    | Maintenance, deps, CI                    |
| `refactor` | Code restructuring, no behavior change   |
| `test`     | Adding or updating tests                 |
| `ci`       | CI/CD pipeline changes                   |
| `style`    | Formatting, whitespace, semicolons       |

> 💡 **GitLab integration:** Use `Refs: #123` or `Closes: #456` in commit or merge request messages to link to issues. `Closes:` will auto-close the issue when merged.

---

## 🔄 Rebasing Your Work

Rebasing rewrites your branch's history to sit **on top of** the latest `main`.

### Why rebase?

- Keeps your branch history **linear and clean**.
- Avoids unnecessary merge commits between `main` and your branch.
- Makes code review easier — reviewers see only your changes, not main's history.

### Rebase workflow

```bash
# Update main
git checkout main
git pull origin main

# Switch back to your branch
git checkout feature/add-rds-instance

# Rebase onto updated main
git rebase main
```

### Handling rebase conflicts

```bash
# Git pauses when conflicts arise. Resolve them:
# 1. Open conflicted files — look for <<<<<<<, =======, >>>>>>> markers
# 2. Edit files to resolve conflicts
# 3. Stage resolved files
git add terraform/modules/rds/main.tf

# Continue the rebase
git rebase --continue

# If you need to abort and start over
git rebase --abort
```

### When to rebase vs. merge

| Rebase ✅                          | Merge ✅                          |
|------------------------------------|-----------------------------------|
| Your branch is personal/work-in-progress | Branch has been shared/merged elsewhere |
| Before opening a merge request     | Integrating a reviewed MR        |
| Keeping history clean for review   | Preserving exact event history   |

> ⚠️ **Never rebase commits that have been pushed to a shared branch.** If you must, use `git push --force-with-lease` (safer than `--force`) and coordinate with your team.

### Interactive rebase (squashing)

Before opening your MR, clean up your history:

```bash
git rebase -i main
```

This opens an editor with your commits. You can:

- `reword` — edit the commit message.
- `squash` / `s` — combine into the previous commit.
- `drop` — remove the commit entirely.
- `fixup` — squash and discard the commit message.

![interactive rebase editor](https://via.placeholder.com/800x400?text=Interactive+Rebase+Editor+Interface)

---

## 🔀 Creating Merge Requests

### What is a Merge Request (MR)?

A MR proposes changes from a feature branch into `main`. It enables **code review**, **CI validation**, and **approval gating** before integration.

### Creating an MR

**From the command line:**

```bash
# Push your branch (first time)
git push -u origin feature/add-rds-instance

# Subsequent pushes
git push
```

**From GitLab UI:**

1. Go to **Merge Requests > New merge request**.
2. Select source branch (`feature/add-rds-instance`) and target branch (`main`).
3. Click **Compare branches and continue**.
4. Fill in the title and description, then **Create merge request**.

![creating a merge request in GitLab](https://via.placeholder.com/800x400?text=GitLab+New+Merge+Request+Form)

### MR settings to understand

| Setting               | Purpose                                                  | Recommended for IaC repos       |
|-----------------------|----------------------------------------------------------|---------------------------------|
| **Approvals**         | Require N approvals before merge                         | At least 1                      |
| **CI must pass**      | Pipeline must succeed before merge                       | Enabled                           |
| **Protect branch**  | Prevent direct pushes to `main`                          | Always enabled                    |
| **Reviewer**          | Assign specific reviewers                                | Assign a peer for IaC changes   |
| **Watcher**           | Notify without requiring review                           | Add team members for visibility |

### Reviewing a merge request

As a reviewer, focus on:

- **Correctness:** Will this Terraform/Ansible change work in the target environment?
- **Idempotency:** Will running this repeatedly cause unintended side effects?
- **State safety:** Does this Terraform change risk state corruption?
- **Security:** Are secrets, IAM policies, or network rules appropriately scoped?
- **Testing:** Were changes validated in a non-production environment?

> 💡 **Terraform-specific review checklist:**
> - No hardcoded credentials or IPs
> - `terraform plan` output reviewed in the MR
> - State file migration is safe (no resource deletion without backup)
> - Provider versions are pinned

---

## 📄 Merge Request Message Practices

### Structure

```markdown
## 📋 Summary

Brief description of the change (2-3 sentences max).

## 🔄 Related Changes

- Terraform: adds `modules/rds/` with main.tf, variables.tf, outputs.tf
- Ansible: updates `inventory/prod.yml` with new host groups
- CI: adds RDS health check job to `.gitlab-ci.yml`

## 🔍 How to test

1. Apply the Terraform module in a staging environment:
   ```bash
   cd terraform/modules/rds
   terraform init
   terraform plan -var-file=../envs/staging.tfvars
   terraform apply -var-file=../envs/staging.tfvars
   ```
2. Verify the Ansible inventory is valid:
   ```bash
   ansible-inventory -i ansible/inventory/prod.yml --list
   ```
3. Run the CI pipeline on this branch.

## ✅ Checklist

- [ ] `terraform fmt` has been run
- [ ] `terraform validate` passes
- [ ] `ansible-lint` passes on modified playbooks
- [ ] Changes tested in a non-production environment
- [ ] Documentation updated (if applicable)

## 🔗 References

- Issue: #42
- Design doc: [link]
- Runbook: [link]
```

### MR title conventions

Use the same type prefix as commits:

```
feat: add RDS instance to production environment
fix: resolve provider version conflict in Terraform
docs: add deployment runbook for ECS cluster
chore: bump ansible-core to 2.15
```

---

## 🏁 End-to-End Workflow Example

Below is a complete walkthrough of a real-world scenario: **adding a new database instance to your infrastructure.**

### Step 1: Start from an updated `main`

```bash
git checkout main
git pull origin main
```

### Step 2: Create your feature branch

```bash
git checkout -b feature/add-rds-instance
```

### Step 3: Make your changes (atomic commits)

```bash
# Commit 1: Add the Terraform module
git add terraform/modules/rds/main.tf
git add terraform/modules/rds/variables.tf
git add terraform/modules/rds/outputs.tf
git commit -m "feat: add RDS instance Terraform module

Provision a PostgreSQL RDS instance in the prod VPC with
automated backups and maintenance windows.

Includes:
- Main module with subnet group and parameter group
- Outputs for endpoint, ARN, and identifier
- Variable overrides for environment-specific sizing"
```

```bash
# Commit 2: Update the Terraform root configuration
git add terraform/main.tf
git add terraform/environments/prod.tfvars
git commit -m "feat: include RDS module in production environment

Wire the new rds module into the prod root configuration
and add environment-specific variables for instance class
and storage allocation."
```

```bash
# Commit 3: Update Ansible inventory
git add ansible/inventory/prod.yml
git commit -m "chore: add RDS endpoint to Ansible inventory

Add the RDS connection details to prod inventory so that
application playbooks can reference the database host."
```

```bash
# Commit 4: Fix a formatting issue you noticed
git add terraform/modules/rds/main.tf
git commit --amend --no-edit
# Or commit separately:
# git add terraform/modules/rds/main.tf
# git commit -m "style: format RDS module with terraform fmt"
```

### Step 4: Push and create the MR

```bash
git push -u origin feature/add-rds-instance
```

Then create the MR via GitLab UI or:

```bash
gitlab-mr create \
  --source-branch feature/add-rds-instance \
  --target-branch main \
  --title "feat: add RDS instance to production environment" \
  --description "See GIT_TRAINING.md for MR template."
```

### Step 5: Address review feedback

```bash
# Make additional changes
# ... edit files ...

git add .
git commit -m "fix: adjust RDS instance class per review feedback"

# Rebase if main has moved
git fetch origin
git rebase origin/main

# Force push (safe because your branch hasn't been merged)
git push --force-with-lease
```

### Step 6: Get approvals and merge

Once CI passes and you have the required approvals:

1. Review the **Changes** tab in GitLab one final time.
2. Confirm the **Terraform Plan** output (if shown by CI).
3. Click **Merge**.
4. Choose **Delete source branch** to clean up.

### Step 7: Sync your local `main`

```bash
git checkout main
git pull origin main
```

### Step 8: Clean up

```bash
git branch -d feature/add-rds-instance
git fetch --prune
```

### Visual overview

```
main:    A — B — C — D — E — F — G — H
                                    ↕ merge
feature:                        C1 — C2 — C3 — C4
```

After rebase:

```
main:    A — B — C — D — E — F — G — H
                                    ↕ merge
feature:                         C1' — C2' — C3' — C4'
```

![workflow diagram](https://via.placeholder.com/800x300?text=Git+Workflow+Diagram:+Branch+-+Rebase+-+MR+-+Merge)

---

## 📚 References

### GitLab Documentation

| Topic | Link |
|-------|------|
| Merge Requests | https://docs.gitlab.com/ee/user/project/merge_requests/ |
| Branch Protection | https://docs.gitlab.com/ee/user/project/protected_branches/ |
| GitLab CI/CD | https://docs.gitlab.com/ee/ci/ |
| Issues Integration | https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-via-merge-request-descriptions |
| Branches | https://docs.gitlab.com/ee/user/project/repository/branches/ |
| Code Review | https://docs.gitlab.com/ee/user/project/merge_requests/approvals/ |

### Git Documentation & Guides

| Topic | Link |
|-------|------|
| Official Git Manual | https://git-scm.com/doc |
| Git Pro Book (free) | https://git-scm.com/book/en/v2 |
| Git Rebase Documentation | https://git-scm.com/docs/git-rebase |
| Git Commit Best Practices | https://cbea.ms/git-commit/ |
| Conventional Commits | https://www.conventionalcommits.org/ |
| Git Branching Model (GitFlow) | https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow |

### Infrastructure as Code Resources

| Topic | Link |
|-------|------|
| Terraform Best Practices | https://www.terraform-best-practices.com/ |
| Terraform Module Structure | https://www.terraform-best-practices.com/recommendations/module-structure/ |
| Ansible Best Practices | https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_best_practices.html |
| Terraform + Ansible Integration | https://developer.hashicorp.com/terraform/tutorials/ansible |

### Useful Git Commands Cheat Sheet

| Command | Purpose |
|---------|---------|
| `git log --oneline --graph --all` | Visual branch history |
| `git diff --stat` | Quick diff summary |
| `git stash push -m "description"` | Temporarily save uncommitted changes |
| `git stash pop` | Restore stashed changes |
| `git blame <file>` | See who changed each line |
| `git log -p -- <file>` | See patch history for a specific file |
| `git reflog` | Recover lost commits |
| `git restore --staged <file>` | Unstage a file (Git 2.23+) |
| `git restore <file>` | Discard working tree changes |

---

> 📌 **Quick reference card:** Print this page or bookmark it. When in doubt, `git status` is your best friend — it tells you exactly where you stand at any moment.
