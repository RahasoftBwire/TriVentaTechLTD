# TriVenta Tech Ltd - GitHub Deployment Guide

## 🚀 **Quick Deployment to GitHub**

Since Git is not installed on this system, here's your step-by-step guide to get your TriVenta Tech website live on GitHub:

---

## 📋 **Prerequisites**

1. **GitHub Account**: Make sure you have access to the repository:
   - Repository: `https://github.com/RahasoftBwire/TriVentaTechLTD.git`
   - You should have push access to this repository

2. **Git Installation** (if not already installed):
   - Download Git from: https://git-scm.com/download/windows
   - Install with default settings
   - Restart your terminal after installation

---

## 🔧 **Deployment Steps**

### **Method 1: Using Git Command Line (Recommended)**

1. **Install Git** (if needed):
   ```bash
   # Download and install Git from https://git-scm.com/
   # Restart PowerShell after installation
   ```

2. **Navigate to your project folder**:
   ```bash
   cd "C:\Users\PC\Desktop\TriVentaTecltd"
   ```

3. **Initialize Git repository**:
   ```bash
   git init
   ```

4. **Add the remote repository**:
   ```bash
   git remote add origin https://github.com/RahasoftBwire/TriVentaTechLTD.git
   ```

5. **Add all files**:
   ```bash
   git add .
   ```

6. **Commit your changes**:
   ```bash
   git commit -m "Initial commit: Complete TriVenta Tech website with portfolio, live chat, and enhanced features"
   ```

7. **Push to GitHub**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

### **Method 2: Using GitHub Desktop (User-Friendly)**

1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Install and sign in** with your GitHub account
3. **Clone the repository**:
   - File → Clone Repository
   - URL: `https://github.com/RahasoftBwire/TriVentaTechLTD.git`
   - Local Path: Choose a temporary location
4. **Copy your files**:
   - Copy all files from `C:\Users\PC\Desktop\TriVentaTecltd\` 
   - Paste into the cloned repository folder
5. **Commit and Push**:
   - Review changes in GitHub Desktop
   - Add commit message: "Complete TriVenta Tech website"
   - Click "Commit to main"
   - Click "Push origin"

### **Method 3: Manual Upload via GitHub Web Interface**

1. **Go to**: https://github.com/RahasoftBwire/TriVentaTechLTD
2. **Upload files**:
   - Click "Upload files" or drag and drop
   - Select all files from your `TriVentaTecltd` folder
   - Add commit message: "Complete TriVenta Tech website"
   - Click "Commit changes"

---

## 🌐 **Enable GitHub Pages**

After uploading your files:

1. **Go to Repository Settings**:
   - Navigate to: https://github.com/RahasoftBwire/TriVentaTechLTD/settings

2. **Configure Pages**:
   - Scroll down to "Pages" section
   - Source: "Deploy from a branch"
   - Branch: "main"
   - Folder: "/ (root)"
   - Click "Save"

3. **Your website will be live at**:
   ```
   https://rahasoftbwire.github.io/TriVentaTechLTD/
   ```

---

## 📁 **Files to Upload**

Make sure these essential files are included:

### **Core Website Files:**
- ✅ `index.html` - Homepage
- ✅ `about.html` - About page
- ✅ `services.html` - Services page
- ✅ `portfolio.html` - Portfolio showcase
- ✅ `why-us.html` - Why choose us
- ✅ `team.html` - Team page
- ✅ `blog.html` - Blog section
- ✅ `contact.html` - Contact form

### **Legal & SEO Files:**
- ✅ `privacy-policy.html` - Privacy policy
- ✅ `terms-of-service.html` - Terms of service
- ✅ `404.html` - Error page
- ✅ `sitemap.xml` - SEO sitemap
- ✅ `robots.txt` - Search engine rules

### **Assets & Branding:**
- ✅ `logo-hexagon-premium.svg` - Main logo
- ✅ `logo-header-hexagon.svg` - Header logo
- ✅ `favicon-hexagon.svg` - Website icon

### **Documentation:**
- ✅ `README.md` - Project documentation
- ✅ `business-plan.md` - Business plan
- ✅ `company-profile.json` - Company data
- ✅ `.gitignore` - Git ignore rules

---

## 🔧 **Post-Deployment Setup**

### **1. Update Analytics**
Replace `GA_MEASUREMENT_ID` in all HTML files with your actual Google Analytics ID:
```html
<!-- In each HTML file, replace: -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_ACTUAL_GA_ID"></script>
```

### **2. Configure Contact Form**
Set up form handling service (Formspree, Netlify Forms, or custom backend):
```html
<!-- In contact.html, update form action: -->
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

### **3. Update Domain References**
Replace `www.triventatech.com` with your actual domain in:
- All HTML meta tags
- `sitemap.xml`
- `README.md`

---

## 🎯 **Custom Domain Setup** (Optional)

If you have a custom domain:

1. **Add CNAME file**:
   ```bash
   echo "www.triventatech.com" > CNAME
   ```

2. **Configure DNS**:
   - Add CNAME record: `www` → `rahasoftbwire.github.io`
   - Add A records for apex domain to GitHub Pages IPs

3. **Update GitHub Pages settings**:
   - Enter your custom domain in repository settings
   - Enable "Enforce HTTPS"

---

## 📞 **Support**

If you encounter any issues:

1. **Check GitHub Status**: https://www.githubstatus.com/
2. **GitHub Pages Documentation**: https://docs.github.com/en/pages
3. **Contact Support**: Create an issue in the repository

---

## 🚀 **Quick Commands Reference**

```bash
# Initialize and deploy (run in project folder)
git init
git remote add origin https://github.com/RahasoftBwire/TriVentaTechLTD.git
git add .
git commit -m "Initial deployment"
git branch -M main
git push -u origin main

# Future updates
git add .
git commit -m "Update: [describe your changes]"
git push origin main
```

---

## ✅ **Verification Checklist**

After deployment, verify:

- [ ] All pages load correctly
- [ ] Logo displays properly
- [ ] Live chat widget works
- [ ] Portfolio filtering functions
- [ ] Contact form submits
- [ ] Mobile responsiveness
- [ ] All navigation links work
- [ ] SEO meta tags are present

---

**Your TriVenta Tech website is ready to go live! 🚀**