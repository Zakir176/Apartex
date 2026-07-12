$status = git status --porcelain
foreach ($line in $status) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    
    $parts = $line.Substring(3)
    $file = $parts.Trim()
    
    if ($file -match '^"(.*)"$') {
        $file = $matches[1]
    }
    
    if ($file -eq "backend/apartex.db" -or $file -eq "commit_all.ps1") {
        continue
    }
    
    $state = $line.Substring(0, 2)
    $basename = Split-Path $file -Leaf
    
    Write-Host "Processing $file ($state)"
    
    if ($state -match 'D') {
        git rm $file
        git commit -m "chore: remove $basename"
    } elseif ($state -match '\?') {
        git add $file
        git commit -m "feat: add $basename"
    } else {
        git add $file
        git commit -m "chore: update $basename"
    }
}
git push -f origin HEAD
