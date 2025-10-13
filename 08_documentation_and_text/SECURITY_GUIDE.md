# 🔒 RhythmIQ Security Guidelines

## 🛡️ **IMPORTANT: What NOT to Push to Git**

### ❌ **NEVER PUSH THESE:**

1. **🤖 ML Models & Training Data**
   - `05_trained_models/` - Contains proprietary algorithms
   - `01_data/` - Contains medical ECG images (privacy sensitive)
   - Any `.joblib`, `.pkl`, `.h5` files

2. **🔑 Sensitive Configuration**
   - API keys, passwords, tokens
   - Database connection strings  
   - Environment variables with secrets
   - Personal configuration files

3. **📊 Generated Results**
   - Confusion matrices, plots, visualizations
   - Analysis reports and summaries
   - Temporary output files

4. **📁 Large Files**
   - Images (PNG, JPG, etc.)
   - Video files
   - Large datasets

## ✅ **Safe to Push:**

1. **📝 Source Code**
   - Python scripts (`.py` files)
   - Java source code (`.java` files)
   - Web templates (`.html`, `.css`, `.js`)

2. **📚 Documentation**
   - README files
   - Code documentation
   - Setup guides (without secrets)

3. **⚙️ Configuration Templates**
   - Maven `pom.xml`
   - `requirements.txt` (dependencies only)
   - Configuration templates (no actual secrets)

## 🔐 **Additional Security Measures:**

1. **Use Environment Variables** for secrets:
   ```bash
   export API_KEY="your-secret-key"
   ```

2. **Create `.env.template`** files instead of actual `.env`:
   ```
   API_KEY=your_api_key_here
   DATABASE_URL=your_database_url_here
   ```

3. **Use Git Hooks** to prevent accidental commits:
   ```bash
   git config --local core.hooksPath .githooks/
   ```

4. **Regular Security Audits:**
   ```bash
   # Check what would be committed
   git status
   git diff --cached
   
   # Review before pushing
   git log --oneline -5
   ```

## 🚨 **If You Accidentally Push Secrets:**

1. **Immediately change** all exposed credentials
2. **Remove from Git history:**
   ```bash
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch path/to/secret/file' \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. **Force push** (⚠️ Use carefully):
   ```bash
   git push --force-with-lease origin main
   ```

## 📋 **Pre-Push Checklist:**

- [ ] No API keys or passwords in files
- [ ] No trained models or datasets
- [ ] No generated images or reports  
- [ ] No personal/private configuration
- [ ] Only source code and documentation
- [ ] Run `git status` to verify files

**Remember: Once pushed to Git, consider data potentially compromised!** 🔒