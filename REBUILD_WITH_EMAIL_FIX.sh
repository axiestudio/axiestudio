#!/bin/bash

echo ""
echo "========================================"
echo "  REBUILDING AXIESTUDIO WITH EMAIL FIX"
echo "========================================"
echo ""
echo "The email verification fix is already in the source code!"
echo "We just need to rebuild the Docker image to use the fixed code."
echo ""

echo "🔧 Step 1: Stopping any running containers..."
docker-compose down

echo ""
echo "🔧 Step 2: Rebuilding Docker image with fixed email service..."
docker-compose build --no-cache

echo ""
echo "🔧 Step 3: Starting AxieStudio with the fix..."
docker-compose up -d

echo ""
echo "✅ REBUILD COMPLETE!"
echo ""
echo "🎉 Email verification should now work correctly!"
echo ""
echo "📧 The fix includes:"
echo "   ✅ Added missing text_body parameter"
echo "   ✅ Both text and HTML email versions"
echo "   ✅ Enterprise-level error handling"
echo "   ✅ Professional email templates"
echo ""
echo "🧪 Test the fix:"
echo "   1. Go to http://localhost:7860"
echo "   2. Create a new user account"
echo "   3. Request verification code"
echo "   4. Check your email inbox"
echo "   5. Enter the 6-digit code"
echo ""
echo "📊 Check logs: docker-compose logs -f"
echo ""
