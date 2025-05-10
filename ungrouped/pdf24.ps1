# After using PDF24 Compression for 9999 DPI and 100% Image quality,
# use this PowerShell script to *BATCH* remove the prefix.

Get-ChildItem -Filter "*.pdf" | ForEach-Object {
    $originalName = $_.Name
    
    # This pattern looks for '_9999dpi_' followed by any characters (.*?)
    # up until '.pdf' at the end of the filename.
    # The (?=\.pdf$) is a "positive lookahead" - it checks for '.pdf' 
    # without including it in the actual match to be removed.
    $patternToRemove = '_9999dpi_.*?(?=\.pdf$)'
    
    # Perform the replacement
    $newName = $originalName -replace $patternToRemove, '' # Replace with an empty string
    
    # Only rename if the name has actually changed
    if ($newName -ne $originalName) {
        Rename-Item -Path $_.FullName -NewName $newName
        Write-Host "Renamed '$originalName' to '$newName'"
    } else {
        # This line can be uncommented if you want to see which files didn't match
        # Write-Host "Pattern not found or no change for '$originalName'"
    }
}
