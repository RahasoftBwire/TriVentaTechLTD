# Remove all emojis from index.html
$content = Get-Content "index.html" -Raw -Encoding UTF8

# Remove specific emojis from hero section
$content = $content -replace '<span class="badge-icon">[^<]+</span>\s*', ''
$content = $content -replace '<span class="chip-icon">[^<]+</span>\s*', ''
$content = $content -replace '<div class="stat-icon">[^<]+</div>\s*', ''
$content = $content -replace '🚀', ''
$content = $content -replace '🌟', ''
$content = $content -replace '✨', ''
$content = $content -replace '⚡', ''
$content = $content -replace '🎯', ''
$content = $content -replace '💡', ''
$content = $content -replace '🎉', ''
$content = $content -replace '🏆', ''
$content = $content -replace '😊', ''
$content = $content -replace '⭐', ''
$content = $content -replace '🌍', ''
$content = $content -replace '💼', ''
$content = $content -replace '🏢', ''
$content = $content -replace '🎓', ''
$content = $content -replace '🏦', ''
$content = $content -replace '🌐', ''
$content = $content -replace '🤖', ''
$content = $content -replace '🔒', ''
$content = $content -replace '☁️', ''
$content = $content -replace '📱', ''
$content = $content -replace '💰', ''
$content = $content -replace '📧', ''
$content = $content -replace '☎️', ''

$content | Set-Content "index.html" -Encoding UTF8 -NoNewline
Write-Host "Emojis removed from index.html"
