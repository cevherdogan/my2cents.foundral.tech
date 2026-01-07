cd /Users/cevherdogan/github/my2cents.foundral.tech

ZIP=../my2cents.foundral.tech_final_$(date +%Y%m%d_%H%M%S).zip

# Create a clean package (exclude git + venv + caches)
zip -r "$ZIP" . \
  -x ".git/*" \
  -x ".venv/*" \
  -x "__pycache__/*" \
  -x "*.pyc" \
  -x ".DS_Store" \
  -x "data/logs/*"

echo "Created: $ZIP"
ls -lh "$ZIP"

