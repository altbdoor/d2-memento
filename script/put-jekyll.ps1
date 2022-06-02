#!/usr/bin/env pwsh

$MyInvocation.MyCommand.Path | Split-Path | Push-Location

Copy-Item -Path 'output/data.json' -Destination '../_data/'

$data = Get-Content 'output/data.json' | ConvertFrom-Json
$activities = @('gambit', 'trials', 'nightfall')

Get-ChildItem -Path '../assets/images' | Remove-Item

foreach ($datum in $data) {
    foreach ($act in $activities) {
        $imageUrl = $datum.($act)

        Copy-Item -Force -Path "images/${imageUrl}" -Destination '../assets/images/'
    }
}
