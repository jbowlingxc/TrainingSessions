# 🌳 Git & GitLab Training Guide

> **Audience:** IT Infrastructure Engineers (Ansible & Terraform workflows)
>
> This guide covers the Git fundamentals you need for day-to-day infrastructure-as-code collaboration on GitLab.
>
> **Primary method:** Use the **VS Code Source Control GUI** for all daily operations. Git commands are provided as secondary references.

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

### In VS Code

1. Open the **Source Control** panel (`Ctrl+Shift+G` / `Cmd+Shift+G`).
2. Click the **branch name** in the status bar (bottom-left corner).
3. Select `main` from the list.
4. Click the **Pull** icon (↓) in the Source Control panel to fetch and integrate remote changes.

> 💡 **Why it matters for IaC:** A broken `main` means broken deployments. Terraform state and Ansible playbooks on `main` are what your CI/CD pipelines run against.

![VS Code Source Control panel with pull button](https://via.placeholder.com/800x300?text=VS+Code+Source+Control+Pull+Action)

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

### Creating a branch in VS Code

1. Open the **Source Control** panel (`Ctrl+Shift+G` / `Cmd+Shift+G`).
2. Click the **branch name** in the status bar (bottom-left corner).
3. Click **Create New Branch…** at the top of the dropdown.
4. Type your branch name (e.g., `feature/add-rds-instance`) and press **Enter**.
5. VS Code automatically creates the branch and switches to it.

> 💡 **Pro tip:** You can also create a branch directly from the GitLab UI under **Repository > Branches > New branch**. This is useful when working from multiple machines.

![VS Code create new branch dialog](https://via.placeholder.com/600x300?text=VS+Code+Create+New+Branch+Dialog)

> 💡 **Before creating a branch,** make sure `main` is up to date (see above section).

---

## 🗂️ Managing Local Branches

### Viewing branches

**In VS Code:**

- Open the **Source Control** panel (`Ctrl+Shift+G` / `Cmd+Shift+G`).
- Click the **branch name** in the status bar (bottom-left).
- All local branches are listed, with the current branch marked with `✓`.
- Remote branches appear under **Remote** in the same list.

> 💡 **Tip:** Hover over a branch to see its last commit message and date.

### Switching branches

**In VS Code:**

1. Click the **branch name** in the status bar (bottom-left).
2. Type to search the list.
3. Click the branch you want to switch to.

### Deleting branches

**In VS Code:**

1. Click the **branch name** in the status bar to open the branch picker.
2. **Right-click** the branch you want to delete.
3. Select **Delete Branch…** from the context menu.
4. Confirm the deletion.

> 💡 To delete a **remote** branch: right-click the branch in the list and select **Delete Remote Branch…**, or visit the GitLab UI under **Repository > Branches**.

### Cleaning up stale branches

**In VS Code:**

1. Open the **Source Control** panel (`Ctrl+Shift+G`).
2. Click the **branch name** in the status bar.
3. Click **Pull** (↓) — this fetches and automatically prunes remote branches that no longer exist on the server.

> Alternatively, open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run `Git: Pull` to fetch and prune.

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

### Making atomic commits in VS Code

1. Open the **Source Control** panel (`Ctrl+Shift+G` / `Cmd+Shift+G`).
2. Under **Changes**, you'll see all modified files listed.
3. **Expand** a file to see its diff inline.
4. **Check the box** next to individual files or hunks (click the `+` icon within a diff to stage a specific change).
5. Type your commit message in the **commit message** box at the top.
6. Click **Commit** (✓) to stage and commit the selected changes.

> 💡 **Selective staging:** Click the `·` (three dots) next to a file in the Changes list to stage individual hunks within that file, or right-click the file and choose **Stage Selected Ranges**.

![VS Code Source Control with selective staging](https://via.placeholder.com/800x400?text=VS+Code+Selective+Staging+UI)

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

### Rebasing in VS Code

1. Open the **Source Control** panel (`Ctrl+Shift+G`).
2. Click the **branch name** in the status bar (bottom-left).
3. Right-click `main` and select **Rebase Onto…** (or **Rebase Current Branch Onto…** depending on your VS Code version).
4. Select `main` as the target branch.
5. VS Code will rebase your current branch on top of `main`.

### Handling rebase conflicts in VS Code

1. When conflicts arise, VS Code will prompt you with a dialog.
2. Open each conflicted file — look for `<<<<<<<`, `=======`, `>>>>>>>` markers.
3. Edit the files to resolve conflicts.
4. In the Source Control panel, the conflicted files will show under **Merge Changes**.
5. Click the **✓ (Accept)** or **✗ (Reject)** buttons for each hunk.
6. Once all conflicts are resolved, click **Commit Merge** to complete the rebase.

> 💡 **If the rebase goes wrong:** Click the **Undo** icon in the Source Control panel, or use the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run `Git: Abort Rebase`.

![VS Code conflict resolution UI](https://via.placeholder.com/800x400?text=VS+Code+Merge+Conflict+Resolution)

### When to rebase vs. merge

| Rebase ✅                          | Merge ✅                          |
|------------------------------------|-----------------------------------|
| Your branch is personal/work-in-progress | Branch has been shared/merged elsewhere |
| Before opening a merge request     | Integrating a reviewed MR        |
| Keeping history clean for review   | Preserving exact event history   |

> ⚠️ **Never rebase commits that have been pushed to a shared branch.** If you must, use `git push --force-with-lease` (safer than `--force`) and coordinate with your team.

### Interactive rebase (squashing)

Before opening your MR, clean up your history:

1. Open the **Command Palette** (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. Run `Git: Squash Commits` or `Git: Rebase Interactive`.
3. Follow the prompts to squash, reword, or drop commits.

> 💡 **Alternative:** Use the VS Code GitLens extension for a visual interactive rebase experience with a commit graph.

---

## 🔀 Creating Merge Requests

### What is a Merge Request (MR)?

A MR proposes changes from a feature branch into `main`. It enables **code review**, **CI validation**, and **approval gating** before integration.

### Creating an MR via VS Code

1. Commit and **push** your changes:
   - Open the **Source Control** panel (`Ctrl+Shift+G`).
   - Click the **Push** icon (↑) in the status bar, or click **Sync Changes** and then **Push**.
2. Once pushed, a notification appears in the bottom-right corner offering to **Create Pull Request**.
3. Click **Create Pull Request** to open GitLab's MR creation page in your browser.

### Creating an MR via GitLab UI

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

1. Open the **Source Control** panel (`Ctrl+Shift+G` / `Cmd+Shift+G`).
2. Click the **branch name** in the status bar and select `main`.
3. Click the **Pull** icon (↓) in the Source Control panel.

### Step 2: Create your feature branch

1. Click the **branch name** in the status bar.
2. Click **Create New Branch…** at the top of the dropdown.
3. Type `feature/add-rds-instance` and press **Enter**.

### Step 3: Make your changes (atomic commits)

#### Commit 1: Add the Terraform module

1. Make your changes to `terraform/modules/rds/main.tf`, `variables.tf`, and `outputs.tf`.
2. Open the **Source Control** panel — the files appear under **Changes**.
3. Check the boxes next to all three files to stage them.
4. Type the commit message:

   ```
   feat: add RDS instance Terraform module

   Provision a PostgreSQL RDS instance in the prod VPC with
   automated backups and maintenance windows.

   Includes:
   - Main module with subnet group and parameter group
   - Outputs for endpoint, ARN, and identifier
   - Variable overrides for environment-specific sizing
   ```

5. Click **Commit** (✓).

#### Commit 2: Update the Terraform root configuration

1. Make changes to `terraform/main.tf` and `terraform/environments/prod.tfvars`.
2. Stage both files in the Source Control panel.
3. Type the commit message:

   ```
   feat: include RDS module in production environment

   Wire the new rds module into the prod root configuration
   and add environment-specific variables for instance class
   and storage allocation.
   ```

4. Click **Commit** (✓).

#### Commit 3: Update Ansible inventory

1. Make changes to `ansible/inventory/prod.yml`.
2. Stage the file.
3. Type the commit message:

   ```
   chore: add RDS endpoint to Ansible inventory

   Add the RDS connection details to prod inventory so that
   application playbooks can reference the database host.
   ```

4. Click **Commit** (✓).

#### Commit 4: Fix a formatting issue you noticed

1. Make the formatting fix to `terraform/modules/rds/main.tf`.
2. Stage the file.
3. Click **Amend Last Commit** (the curved arrow icon next to the commit box) to fold this change into the previous commit, or create a new commit as shown above.

### Step 4: Push and create the MR

1. Click the **Push** icon (↑) in the status bar, or click **Sync Changes** → **Push**.
2. When the notification appears, click **Create Pull Request** to open GitLab's MR page.
3. Fill in the title and description using the template from the [MR Message Practices](#-merge-request-message-practices) section.
4. Click **Create merge request**.

### Step 5: Address review feedback

1. Make additional changes in VS Code as needed.
2. Stage and commit them in the Source Control panel.
3. If `main` has moved since you branched:
   - Click the **branch name** in the status bar.
   - Right-click `main` and select **Rebase Onto…** → `main`.
   - Resolve any conflicts that appear.
4. Click **Sync Changes** → **Push** to update the MR.

### Step 6: Get approvals and merge

1. Once CI passes and you have the required approvals:
2. Review the **Changes** tab in GitLab one final time.
3. Confirm the **Terraform Plan** output (if shown by CI).
4. Click **Merge**.
5. Choose **Delete source branch** to clean up.

### Step 7: Sync your local `main`

1. Click the **branch name** in the status bar and select `main`.
2. Click the **Pull** icon (↓) in the Source Control panel.

### Step 8: Clean up

1. Click the **branch name** in the status bar.
2. Right-click your feature branch and select **Delete Branch…**.
3. Confirm the deletion.

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

> 📌 **Quick reference card:** Print this page or bookmark it. When in doubt, the **Source Control** panel (`Ctrl+Shift+G` / `Cmd+Shift+G`) in VS Code handles most Git operations visually — no commands needed.

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
