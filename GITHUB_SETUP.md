# GitHub Setup Instructions

> **Status**: ✅ Project ready for GitHub. Follow these steps to push your project to GitHub.

---

## 📋 Prerequisites

- ✅ Git installed on your machine: [Download Git](https://git-scm.com/)
- ✅ GitHub account created: [Create Account](https://github.com/)
- ✅ `visfraud` project initialized locally with `.git` folder

## 🔍 Verify Local Git Setup

### Check if Git is initialized:
```bash
cd c:\Users\palla\visfraud
git status
```

If you see:
```
On branch main
Your branch is up to date with 'origin/main'.
```

✅ **Git is already initialized!** Skip to Step 2.

If you see:
```
fatal: not a git repository
```

❌ **Need to initialize Git first**. Go to [Step 0](#step-0-initialize-git-locally).

---

## 🚀 Step-by-Step Setup

### Step 0: Initialize Git Locally (if needed)

```bash
cd c:\Users\palla\visfraud

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: VisFraud fraud detection project"
```

### Step 1: Create Repository on GitHub

1. **Log in to GitHub**: https://github.com/
2. **Click `+` icon** (top right) → **New repository**
3. **Repository settings**:
   - **Repository name**: `visfraud`
   - **Description**: "Visual Saliency for Fraud Pattern Detection"
   - **Visibility**: 
     - Choose `Public` if you want others to see it (portfolio, open source)
     - Choose `Private` if it's personal research
   - **Add .gitignore**: Skip (already have one locally)
   - **License**: Skip (will add manually)
4. **Click "Create repository"**

✅ **GitHub will show you the setup commands** in the next screen.

---

### Step 2: Connect Local Repository to GitHub

After creating the GitHub repo, you'll see commands like these. Run them in PowerShell:

```powershell
# Set the remote repository URL
git remote add origin https://github.com/your-username/visfraud.git

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Replace `your-username` with your actual GitHub username.**

---

### Step 3: Verify Push Success

Check GitHub:
1. Go to: `https://github.com/your-username/visfraud`
2. ✅ You should see all your files uploaded
3. ✅ Verify these key files appear:
   - `README.md` (with GitHub formatting)
   - `CONTRIBUTING.md`
   - `LICENSE`
   - `REPORT.md`
   - `.github/` folder with issue templates
   - `notebooks/`, `src/`, `data/`, `scripts/`

---

## 🔑 Authentication Setup

### Option A: SSH Keys (Recommended)

**Generate SSH key:**
```powershell
ssh-keygen -t ed25519 -C "your-email@example.com"
```
- Press Enter for all prompts (use default location and no passphrase)

**Add to GitHub:**
1. Go to: https://github.com/settings/keys
2. Click **"New SSH key"**
3. Paste the key from: `~/.ssh/id_ed25519.pub`
4. Title: "VisFraud Development Machine"

**Test connection:**
```powershell
ssh -T git@github.com
```

Should output:
```
Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
```

### Option B: Personal Access Token (Alternative)

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Token settings**:
   - **Name**: "VisFraud Push"
   - **Expiration**: 90 days
   - **Scopes**: Check `repo` (full control of private repositories)
4. Click **"Generate token"**
5. ✅ **Copy the token immediately** (you won't see it again)

**Configure Git:**
```powershell
# Use token as password when pushing
# Or configure git credential helper:
git config --global credential.helper wincred
```

When prompted for credentials:
- **Username**: `your-username`
- **Password**: Paste your personal access token

---

## 📝 Initial Commit & Push

### If you haven't pushed yet:

```powershell
cd c:\Users\palla\visfraud

# Check status
git status

# Add all files (if not done)
git add .

# Commit with clear message
git commit -m "Initial commit: VisFraud visual fraud detection project

- Gramian Angular Field (GAF) and Recurrence Plot encoding
- PyTorch CNN classifier with ~14K parameters
- Grad-CAM saliency map explainability
- XGBoost baseline benchmark
- Three executable Jupyter notebooks
- Comprehensive documentation and GitHub setup"

# Push to GitHub
git push -u origin main
```

---

## 📦 Making Changes & Pushing Updates

### Standard workflow:

```powershell
# Make changes to files
# Edit notebooks, code, etc.

# Check what changed
git status

# Stage specific files
git add src/model.py src/train.py

# Or stage all changes
git add .

# Commit with descriptive message
git commit -m "Improve model architecture with residual connections"

# Push to GitHub
git push origin main
```

### For feature development:

```powershell
# Create feature branch
git checkout -b feature/add-ensemble-models

# Make changes and commit
git add .
git commit -m "Add ensemble method combining CNN and XGBoost"

# Push feature branch
git push origin feature/add-ensemble-models

# On GitHub: Create Pull Request from feature branch to main
# (This allows for review before merging)
```

---

## 🏷️ Add GitHub Topics (Optional)

1. Go to your repository: `https://github.com/your-username/visfraud`
2. Click **⚙️ Settings** → scroll down to **"Topics"**
3. Add relevant topics:
   - `fraud-detection`
   - `machine-learning`
   - `deep-learning`
   - `interpretability`
   - `credit-card-fraud`
   - `explainable-ai`
   - `gradcam`
   - `pytorch`

---

## 📌 Add Repository Description

1. On your repository homepage, click **⚙️ Settings**
2. Scroll to **"Repository details"** section
3. **Description**: "Visual Saliency for Fraud Pattern Detection | CNN + Grad-CAM"
4. **Website**: (optional) Add blog post or paper link
5. Click **"Save"**

---

## ✨ Add Repository Badge (Optional)

Add this to your README.md to show your GitHub stars:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/your-username/visfraud.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/your-username/visfraud/stargazers/)
```

---

## 🔔 Enable Notifications

1. Go to your repository
2. Click **👁️ Watch** (top right)
3. Choose notification level (usually "Participating and @mentions")

---

## ✅ Checklist: Repository Ready

- [ ] GitHub account created
- [ ] Git initialized locally
- [ ] SSH key or token configured
- [ ] GitHub repository created
- [ ] Local repo connected to GitHub (`git remote -v` shows `origin`)
- [ ] Files pushed to GitHub (can see on github.com)
- [ ] `.github/` folder with issue/PR templates visible
- [ ] `LICENSE` file visible
- [ ] `README.md` with proper formatting
- [ ] `REPORT.md` present
- [ ] `CONTRIBUTING.md` present
- [ ] `.gitignore` working (data/, .venv/ not pushed)

---

## 📚 Useful Git Commands

### View commits:
```powershell
git log --oneline -5
```

### Check remote:
```powershell
git remote -v
```

### Update from GitHub (if working with others):
```powershell
git pull origin main
```

### Undo last commit (before push):
```powershell
git reset --soft HEAD~1
```

### View differences:
```powershell
git diff
```

---

## 🆘 Troubleshooting

### "fatal: not a git repository"
```powershell
cd c:\Users\palla\visfraud
git init
git add .
git commit -m "Initial commit"
```

### "Permission denied (publickey)"
- **SSH issue**: Generate and add SSH key (see Option A above)
- **Or use token**: Switch to HTTPS and use PAT (see Option B)

### "fatal: The current branch main has no upstream branch"
```powershell
git push -u origin main
```

### Cannot push: "Updates were rejected"
```powershell
# Pull latest changes
git pull origin main

# Resolve conflicts if any, then push
git push origin main
```

### Want to delete entire Git history and start fresh:
```powershell
# Remove .git folder
Remove-Item -Recurse -Force .git

# Reinitialize
git init
git add .
git commit -m "Initial commit"
```

---

## 📖 Next Steps

1. ✅ **Push to GitHub** using steps above
2. ✅ **Add repository topics** for discoverability
3. ✅ **Create GitHub Pages** (optional) to showcase results
4. ✅ **Enable discussions** for community feedback
5. ✅ **Setup GitHub Actions** for automated testing (workflows already added)
6. ✅ **Add collaborators** if working with others

---

## 📞 Need Help?

- **GitHub Docs**: https://docs.github.com/
- **Git Guide**: https://git-scm.com/book/
- **SSH Issues**: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

---

**Status**: 🎉 Your project is ready to go to GitHub!
