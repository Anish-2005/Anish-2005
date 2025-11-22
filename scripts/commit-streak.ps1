Param(
    [string]$ReadmePath = "README.md"
)

# Check for git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git not found in PATH. Install Git or run this script from a repo with git available."
    exit 2
}

# Get unique commit dates (author date) in yyyy-MM-dd format, newest first
# We trim and deduplicate to handle multiple commits per day
$raw = git log --pretty=format:%ad --date=short 2>$null
$dates = @()
if ($raw) {
    $raw -split "\n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" } | Sort-Object -Unique -Descending | ForEach-Object { $dates += $_ }
}

if (-not $dates -or $dates.Count -eq 0) {
    $streak = 0
} else {
    $today = Get-Date
    $streak = 0
    $current = $today
    while ($true) {
        $dateStr = $current.ToString('yyyy-MM-dd')
        if ($dates -contains $dateStr) {
            $streak++
            $current = $current.AddDays(-1)
        } else {
            break
        }
    }
}

# Choose a color based on streak to make the badge look nicer
switch ($streak) {
    { $_ -eq 0 } { $color = '808080' ; break }         # gray
    { $_ -le 3 } { $color = 'FFB020' ; break }         # amber
    { $_ -le 7 } { $color = 'FF6B6B' ; break }         # coral
    default { $color = '4ECDC4' }                     # greenish
}

# Last commit date for tooltip
$lastCommit = ($dates | Select-Object -First 1) -as [string]
if (-not $lastCommit) { $lastCommit = 'N/A' }

# Build a prettier shields.io badge URL (label=Streak, message="X days", color)
$label = [System.Uri]::EscapeDataString('Commit Streak')
$message = [System.Uri]::EscapeDataString("$streak day" + (if ($streak -ne 1) { 's' } else { '' }))
$badgeUrl = "https://img.shields.io/badge/$label-$message-$color?style=for-the-badge&logo=github&logoColor=white"

# Markdown image with title showing last commit date
$badge = "<p align=`"center`"><img src=`"$badgeUrl`" alt=`"Commit Streak: $streak`" title=`"Last commit: $lastCommit`"/></p>"

if (-not (Test-Path $ReadmePath)) {
    Write-Output $badge
    exit 0
}

$content = Get-Content -Path $ReadmePath -Raw -ErrorAction Stop
$pattern = '(?s)<!-- COMMIT_STREAK_START -->(.*?)<!-- COMMIT_STREAK_END -->'

if ($content -match $pattern) {
    $replacement = "<!-- COMMIT_STREAK_START -->`n$badge`n<!-- COMMIT_STREAK_END -->"
    $new = [System.Text.RegularExpressions.Regex]::Replace($content, $pattern, $replacement, [System.Text.RegularExpressions.RegexOptions]::Singleline)
    Set-Content -Path $ReadmePath -Value $new -Encoding UTF8
    Write-Output "Updated '$ReadmePath' with commit streak: $streak"
} else {
    Write-Warning "No commit-streak placeholder found in '$ReadmePath'. Add <!-- COMMIT_STREAK_START --> and <!-- COMMIT_STREAK_END --> to the file where you want the badge."
    Write-Output $badge
}
