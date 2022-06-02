#!/usr/bin/env pwsh

$MyInvocation.MyCommand.Path | Split-Path | Push-Location

# path to file.exe to check for png
# ========================================
$pathToFileExe = $args[0]
if (!$pathToFileExe) {
    throw 'please provide path to file.exe'
}

# thanks /u/TheLastJoaquin
# https://docs.google.com/spreadsheets/d/1Msr7Vdqfa6MlMXYSlERAnbTwEr4Fd7rVe2uvxaPjo14/edit#gid=0

# fetching csv data
# ========================================
$sheet = '1Msr7Vdqfa6MlMXYSlERAnbTwEr4Fd7rVe2uvxaPjo14'
New-Item -ItemType Directory -Force -Path 'output'
Invoke-WebRequest -OutFile 'output/input.csv' `
    -Uri "https://docs.google.com/spreadsheets/d/${sheet}/export?format=csv&gid=0"

# parsing csv into meaningful data
# ========================================
$headers = @(
    'Season',
    'Group',
    'Weapon',
    'Gambit',
    'Spacer1',
    'Trials',
    'Spacer2',
    'Nightfall',
    'CreditGambit',
    'CreditTrials',
    'CreditNightfall'
)
$csv = Import-Csv -Path 'output/input.csv' -Header $headers
$csv = $csv | Select-Object -Skip 4

$data = @()
foreach ($line in $csv) {
    $datum = [ordered]@{
        season           = $line.Season.Trim();
        group            = $line.Group.Trim();
        weapon           = $line.Weapon.Trim();
        gambit           = $line.Gambit.Trim();
        trials           = $line.Trials.Trim();
        nightfall        = $line.Nightfall.Trim();
        slug             = '';
        credit_gambit    = $line.CreditGambit.Trim();
        credit_trials    = $line.CreditTrials.Trim();
        credit_nightfall = $line.CreditNightfall.Trim();
    }

    # temp patch for future credits
    if ($datum.credit_gambit -contains 'add these later') {
        $datum.credit_gambit = ''
    }

    if ($datum.weapon -eq '') {
        break
    }

    if ($datum.group -eq '') {
        $datum.group = $data[-1].group
    }

    if ($datum.season -eq '') {
        $datum.season = $data[-1].season
    }

    $datum.slug = $datum.weapon.ToLower() -replace '[^A-z0-9]', ''
    $data += @(, $datum)
}

# cleaning image urls
# ========================================
$activities = @('gambit', 'trials', 'nightfall')
foreach ($datum in $data) {
    foreach ($act in $activities) {
        $imageUrl = $datum.($act)

        if ($imageUrl -match 'imgur.com/a/') {
            $html = (Invoke-WebRequest -Uri $imageUrl).Content
            $imageUrl = $html | Select-String -Pattern '"https://i.imgur.com/.+?"' | ForEach-Object { $_.Matches.Value } | Select-Object -First 1
            $imageUrl = $imageUrl -replace '"', ''
        }
        elseif ($imageUrl -match 'drive.google.com') {
            $driveId = $imageUrl.Split('/')[5]
            $imageUrl = "https://docs.google.com/uc?export=download&id=${driveId}"
        }

        $datum.($act) = $imageUrl ? $imageUrl : ''
    }
}

# fetching images
# ========================================
New-Item -ItemType Directory -Force -Path 'images'

foreach ($datum in $data) {
    foreach ($act in $activities) {
        $imageUrl = $datum.($act)
        $filename = "$($datum.slug)-$($act.ToLower())"
        $findFilename = Get-ChildItem -Path 'images' -Name -Include "${filename}*" | Select-Object -Last 1

        if ($findFilename) {
            Write-Output "images/${findFilename} already exist"
        }
        elseif ($imageUrl -match '^http') {
            Invoke-WebRequest -Uri "${imageUrl}" -OutFile "images/${filename}.jpg"
            $findFilename = "${filename}.jpg"

            $fileMetadata = & "${pathToFileExe}" @("images/${filename}.jpg")
            if ($fileMetadata -match 'PNG image data') {
                Move-Item -Path "images/${filename}.jpg" -Destination "images/${filename}.png"
                $findFilename = "${filename}.png"
                Write-Output "downloaded images/${findFilename} from ${imageUrl}"
            }
            elseif ($fileMetadata -match 'JPEG image data') {
                Write-Output "downloaded images/${findFilename} from ${imageUrl}"
            }
            else {
                Write-Output "(!) images/${findFilename} from ${imageUrl} might be corrupted"
            }
        }

        $datum.($act) = $findFilename ? $findFilename : ''
    }
}

# output to json
# ========================================
ConvertTo-Json -InputObject $data -Depth 100 | Out-File -FilePath "output/data.json"
