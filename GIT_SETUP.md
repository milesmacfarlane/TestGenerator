# Git Setup and Push Instructions

## Initial Repository Setup

### 1. Navigate to your project directory
```bash
cd /path/to/TestGenerator
```

### 2. Initialize Git repository
```bash
git init
```

### 3. Add all files
```bash
git add .
```

### 4. Check what will be committed
```bash
git status
```

You should see:
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ `QUICKSTART.md`
- ✅ `LICENSE`
- ✅ `requirements.txt`
- ✅ `app.py`
- ✅ `src/` directory with all Python files
- ✅ `data/README.md`
- ✅ `docs/SETUP.md`
- ✅ `tests/test_basic.py`

**Should NOT see** (thanks to .gitignore):
- ❌ `__pycache__/`
- ❌ `.venv/`
- ❌ `.DS_Store`
- ❌ `temp_lookup_tables.xlsx`

### 5. Make initial commit
```bash
git commit -m "Initial commit: EMA40S Test Generator v0.1.0

- Mean/Median/Mode question generator
- Trimmed Mean question generator
- Streamlit web interface
- Statistics calculator utilities
- Data manager with fallback data
- Comprehensive documentation
- Basic test suite"
```

### 6. Add remote repository
```bash
git remote add origin https://github.com/milesmacfarlane/TestGenerator.git
```

### 7. Verify remote
```bash
git remote -v
```

Should show:
```
origin  https://github.com/milesmacfarlane/TestGenerator.git (fetch)
origin  https://github.com/milesmacfarlane/TestGenerator.git (push)
```

### 8. Push to GitHub
```bash
# If repository is empty on GitHub:
git branch -M main
git push -u origin main

# If you already have README on GitHub:
git pull origin main --rebase
git push -u origin main
```

## Complete File List to Commit

### Root Directory
```
.gitignore           # Git exclusions
LICENSE              # MIT license
README.md            # Project overview
QUICKSTART.md        # Quick start guide
requirements.txt     # Python dependencies
app.py              # Main application
```

### Source Code (`src/`)
```
src/
├── __init__.py
├── data_manager.py
├── statistics_calculator.py
├── question_models.py
└── generators/
    ├── __init__.py
    ├── mean_median_mode.py
    └── trimmed_mean.py
```

### Data Directory (`data/`)
```
data/
└── README.md        # Data format documentation
```

Note: `WorksheetMergeMasterSourceFile.xlsx` should NOT be committed (excluded by .gitignore)

### Documentation (`docs/`)
```
docs/
└── SETUP.md         # Setup and deployment guide
```

### Tests (`tests/`)
```
tests/
└── test_basic.py    # Basic unit tests
```

## Verify Everything Looks Good

### Check repository on GitHub
1. Go to https://github.com/milesmacfarlane/TestGenerator
2. Verify all files are present
3. Check that README displays properly
4. Ensure .gitignore is working (no cache files, etc.)

### Test locally
```bash
# Clone to a new location to test
cd /tmp
git clone https://github.com/milesmacfarlane/TestGenerator.git
cd TestGenerator

# Install and run
pip install -r requirements.txt
streamlit run app.py
```

## Making Changes After Initial Push

### Regular workflow
```bash
# Make your changes
# ...

# Check what changed
git status

# Add changed files
git add .

# Commit with descriptive message
git commit -m "Add weighted mean generator"

# Push to GitHub
git push origin main
```

### Creating feature branches (recommended)
```bash
# Create new branch
git checkout -b feature/weighted-mean

# Make changes and commit
git add .
git commit -m "Implement weighted mean generator"

# Push branch to GitHub
git push origin feature/weighted-mean

# Then create Pull Request on GitHub
# After merge, switch back to main
git checkout main
git pull origin main
```

## Common Git Commands

### Check status
```bash
git status                 # See what's changed
git log --oneline          # See commit history
git diff                   # See uncommitted changes
```

### Undo changes
```bash
git checkout -- file.py    # Discard changes to file
git reset HEAD file.py     # Unstage file
git reset --soft HEAD~1    # Undo last commit (keep changes)
```

### Branch management
```bash
git branch                 # List branches
git checkout -b new-branch # Create and switch to branch
git merge feature-branch   # Merge branch into current
git branch -d old-branch   # Delete merged branch
```

### Update from GitHub
```bash
git pull origin main       # Get latest changes
```

## Troubleshooting

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/milesmacfarlane/TestGenerator.git
```

### "error: failed to push some refs"
```bash
git pull origin main --rebase
git push origin main
```

### Accidentally committed large file
```bash
# Remove from commit
git rm --cached large_file.xlsx

# Update .gitignore
echo "*.xlsx" >> .gitignore

# Commit the changes
git add .gitignore
git commit -m "Remove large file and update .gitignore"
git push origin main
```

### Want to start fresh
```bash
# Delete .git directory
rm -rf .git

# Start over from step 1
git init
# ... continue with setup
```

## GitHub Repository Settings

### Recommended settings:

1. **Branch Protection** (Settings → Branches)
   - Protect `main` branch
   - Require pull request reviews
   - Require status checks to pass

2. **Issues** (Settings → General)
   - Enable Issues for bug tracking
   - Enable Projects for roadmap

3. **Wiki** (optional)
   - Enable for additional documentation

4. **Releases** (when ready)
   - Create v0.1.0 release
   - Attach downloadable zip

## Next Steps After Push

1. ✅ Verify all files on GitHub
2. 📝 Edit repository description on GitHub
3. 🏷️ Add topics: `education`, `mathematics`, `streamlit`, `python`, `manitoba`
4. 📋 Create first Issue for next feature
5. 🚀 Consider deploying to Streamlit Cloud

---

**You're all set!** 🎉

Your repository is now live at:
https://github.com/milesmacfarlane/TestGenerator
