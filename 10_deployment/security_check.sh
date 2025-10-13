#!/bin/bash
# 🔍 Pre-commit Security Check Script

echo "🔒 RhythmIQ Security Check - Scanning for sensitive files..."
echo "================================================================"

# Check for potential secrets in staged files
echo "🔍 Checking staged files for potential secrets:"
git diff --cached --name-only | while read file; do
    if [[ -f "$file" ]]; then
        # Check for common secret patterns
        if grep -i -E "(api[_-]?key|password|secret|token|credential)" "$file" > /dev/null 2>&1; then
            echo "⚠️  WARNING: Potential secret found in: $file"
        fi
        
        # Check for file extensions that shouldn't be committed
        case "$file" in
            *.joblib|*.pkl|*.h5|*.model)
                echo "❌ BLOCKED: Model file detected: $file"
                ;;
            *.png|*.jpg|*.jpeg|*.gif)
                echo "❌ BLOCKED: Image file detected: $file"
                ;;
            *.env|*secret*|*credential*)
                echo "❌ BLOCKED: Sensitive config detected: $file"
                ;;
            *)
                echo "✅ Safe to commit: $file"
                ;;
        esac
    fi
done

echo ""
echo "🎯 Files that will be committed:"
git status --porcelain | grep "^A\|^M" | cut -c4-

echo ""
echo "📊 Repository size check:"
du -sh .git/

echo ""
echo "🔐 Security recommendations:"
echo "- Review all files before committing"
echo "- Never commit API keys or passwords"  
echo "- Keep model files and datasets local"
echo "- Use environment variables for secrets"

echo ""
echo "✅ Run 'git commit' if everything looks safe!"