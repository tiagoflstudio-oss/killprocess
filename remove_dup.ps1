$a = Get-Content "gui.py"
# Remove linhas 530 a 750 (0-indexed: 529 a 749)
$b = $a[0..528] + $a[750..($a.Length - 1)]
Set-Content "gui.py" -Value $b -Encoding UTF8
Write-Host "Feito. Total linhas: $($b.Length)"
