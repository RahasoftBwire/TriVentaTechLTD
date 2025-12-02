# Render Deployment Instructions for Bwire Global Tech Website

## Option 1: Static Site (RECOMMENDED - FREE)

1. Go to Render Dashboard: https://dashboard.render.com
2. Click "New +" → Select "Static Site"
3. Connect Repository: RahasoftBwire/TriVentaTechLTD
4. Fill in these settings:

   **Name:** TriVentaTechLTD
   **Branch:** main
   **Build Command:** (leave empty)
   **Publish Directory:** . (just a dot)
   
5. Click "Create Static Site"

## Option 2: If You Need Manual Configuration

Since render.yaml is already in your repo, Render should auto-detect it.
But if needed, use these manual settings:

- **Name:** TriVentaTechLTD
- **Environment:** Static Site
- **Branch:** main  
- **Build Command:** (empty)
- **Publish Directory:** .
- **Auto-Deploy:** Yes

## Your site will be live at:
https://triventatechltd.onrender.com (or similar)

## Important Notes:
- ✅ This is a STATIC SITE (HTML/CSS/JS only)
- ✅ NO Docker needed
- ✅ NO build process needed
- ✅ FREE tier is perfect for this
- ✅ Auto-deploys on every git push

## If You See Docker Options:
You're in the WRONG section! 
Go back and select "Static Site" instead of "Web Service"
