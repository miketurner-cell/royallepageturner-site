#!/bin/bash
# Deploy royallepageturner.com to Netlify
# Usage: ./deploy.sh

cd "$(dirname "$0")"

echo ""
echo "=== HUB SITE — DEPLOY ==="
echo ""

# No pre-deploy checker yet for hub site — skip to deploy
echo "Deploying to Netlify..."
echo ""

if ! command -v netlify &> /dev/null; then
    echo "Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# If not yet linked to Netlify, this will prompt you to select/create a site
netlify deploy --prod --dir .

echo ""
echo "✅ Done! Site is live at royallepageturner.com"
echo ""
