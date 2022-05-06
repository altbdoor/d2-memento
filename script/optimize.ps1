#!/usr/bin/env pwsh

$MyInvocation.MyCommand.Path | Split-Path | Push-Location

# path to cjpeg to compress to jpeg
# ========================================
$pathToCjpeg = $args[0]
if (!$pathToCjpeg) {
    throw 'please provide path to cjpeg.exe'
}

$images = Get-ChildItem -Path 'images' | Where-Object { $_.Name -match '\.png$' }
foreach ($img in $images) {
    $baseFilename = Split-Path -Path "$($img.Name)" -LeafBase
    Write-Output "compressing $($img.Name)..."
    & "${pathToCjpeg}" @('-quality', '90', '-outfile', "images/${baseFilename}.jpg", "images/${baseFilename}.png")

    $beforeSize = '{0:n2}M' -f ($img.Length / 1mb)
    $afterSize = Get-ChildItem -Filter "images/${baseFilename}.jpg"
    $afterSize = '{0:n2}M' -f ($afterSize.Length / 1mb)

    Write-Output "compressed from ${beforeSize} to ${afterSize}"
}

Write-Output 'patching data.json to use the JPG files...'
$activities = @('gambit', 'trials', 'nightfall')
$data = Get-Content 'output/data.json' | ConvertFrom-Json

foreach ($datum in $data) {
    foreach ($act in $activities) {
        $imageUrl = $datum.($act)

        if ($imageUrl -match '\.png$') {
            $datum.($act) = $imageUrl -replace '.png', '.jpg'
        }
    }
}

ConvertTo-Json -InputObject $data -Depth 100 | Out-File -FilePath "output/data.json"
