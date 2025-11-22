Param(
    [string]$ReadmePath = "README.md"
)

# Check for git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git not found in PATH. Install Git or run this script from a repo with git available."
    exit 2
}

# Get unique commit dates (author date) in yyyy-MM-dd format, newest first
$dates = git log --pretty=format:%ad --date=short | Sort-Object -Unique -Descending

if (-not $dates) {
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

# Build shields.io badge markdown (URL-encode by replacing spaces)
$badge = "![Commit Streak](https://img.shields.io/badge/commit%20streak-$($streak)-4ECDC4?style=for-the-badge&logo=github&logoColor=white)"

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
