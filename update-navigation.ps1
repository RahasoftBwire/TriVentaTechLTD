# PowerShell script to update navigation across all HTML pages
# Bwire Global Tech - Navigation Consistency Update

$pages = @(
    "about.html",
    "team.html",
    "contact.html",
    "blog.html",
    "why-us.html",
    "portfolio.html",
    "careers.html",
    "news.html",
    "enroll.html",
    "downloads.html"
)

$dropdownNavigation = @"
                <nav class="main-nav">
                    <!-- Dropdown Navigation -->
                    <div class="nav-dropdown-container" id="navDropdownContainer">
                        <button class="nav-dropdown-btn" id="navDropdownBtn">
                            <span>Menu</span>
                            <svg width="12" height="8" viewBox="0 0 12 8" fill="none">
                                <path d="M1 1.5L6 6.5L11 1.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <ul class="nav-dropdown-menu" id="navDropdownMenu">
                            <li><a href="index.html">Home</a></li>
                            <li><a href="about.html">About</a></li>
                            <li><a href="services.html">Services</a></li>
                            <li><a href="portfolio.html">Portfolio</a></li>
                            <li><a href="downloads.html">Downloads</a></li>
                            <li><a href="why-us.html">Why Us</a></li>
                            <li><a href="team.html">Team</a></li>
                            <li><a href="blog.html">Blog</a></li>
                            <li><a href="enroll.html">Training</a></li>
                            <li><a href="contact.html">Contact</a></li>
                        </ul>
                    </div>
                    <a href="contact.html" class="cta-button">Get Started</a>
                </nav>
"@

Write-Host "Bwire Global Tech - Navigation Update Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($page in $pages) {
    $filePath = Join-Path $PSScriptRoot $page
    
    if (Test-Path $filePath) {
        Write-Host "Updating $page..." -ForegroundColor Yellow
        
        $content = Get-Content $filePath -Raw
        
        # Mark this page as active in the navigation
        $pageName = [System.IO.Path]::GetFileNameWithoutExtension($page)
        $customNav = $dropdownNavigation -replace "href=`"$page`"", "href=`"$page`" class=`"active`""
        
        # Replace old navigation with new dropdown navigation
        # This pattern matches the old <nav> with <ul> structure
        $pattern = '<nav class="main-nav">\s*<ul>[\s\S]*?</ul>\s*</nav>\s*<a href="contact\.html" class="cta-button">Get Started</a>'
        
        if ($content -match $pattern) {
            $content = $content -replace $pattern, $customNav
            Set-Content -Path $filePath -Value $content -NoNewline
            Write-Host "  ✓ Successfully updated $page" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Pattern not found in $page - manual update needed" -ForegroundColor Red
        }
    } else {
        Write-Host "  ✗ File not found: $page" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Navigation update complete!" -ForegroundColor Green
