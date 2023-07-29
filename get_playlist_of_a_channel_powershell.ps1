$User = Read-Host -Prompt 'Enter YouTube user name: '
$listsPage = "https://www.youtube.com/$User/playlists"
Write-Host "'$listsPage'"
$playlists = yt-dlp.exe -ij --flat -- $listsPage | ConvertFrom-Json | select id,url,title
$playlists.url | Out-File -FilePath "$User.txt" # list of URL