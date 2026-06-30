<#
.
Skrypt PowerShell do szybkiej aktualizacji diagramu klas.

Użycie:
  PowerShell.exe -ExecutionPolicy Bypass -File .\scripts\update_diagram.ps1

Parametry:
  -Output <ścieżka>    - ścieżka pliku wynikowego (domyślnie .\scripts\class_diagram.svg)
  -Render              - jeżeli podane, spróbuje wyrenderować SVG używając binarki `dot` (jeśli jest w PATH)

Skrypt wywołuje Pythona do wygenerowania pliku .dot (nie wymaga zainstalowanej binarki Graphviz).
Jeżeli chcesz, aby skrypt od razu wyrenderował grafikę, użyj parametru -Render (wymaga zainstalowanego Graphviz).
#>

param(
    [string]$Output = ".\scripts\class_diagram.svg",
    [switch]$Render
)

Write-Host "Generuję źródło diagramu (.dot) za pomocą skryptu Python..."

$py = "python"
$script = Join-Path -Path (Get-Location) -ChildPath "scripts/generate_viz.py"

$cmd = "$py `"$script`" --root . --output `"$Output`" --dot-only"
Write-Host "Uruchamiam: $cmd"
& $py $script --root . --output $Output --dot-only

$dotPath = [System.IO.Path]::ChangeExtension($Output, ".dot")
if (-Not (Test-Path $dotPath)) {
    Write-Error "Nie znaleziono wygenerowanego pliku .dot: $dotPath"
    exit 1
}

Write-Host "Plik .dot zapisano: $dotPath"

if ($Render) {
    # sprawdź czy dot jest dostępny
    $dot = Get-Command dot -ErrorAction SilentlyContinue
    if ($null -eq $dot) {
        Write-Warning "Nie znaleziono binarki 'dot' w PATH. Zainstaluj Graphviz lub usuń parametr -Render."
        exit 2
    }
    $out = $Output
    Write-Host "Wyrenderowuję SVG: dot -Tsvg $dotPath -o $out"
    & dot -Tsvg $dotPath -o $out
    if (Test-Path $out) {
        Write-Host "Wyrenderowano: $out"
    } else {
        Write-Warning "Nie udało się wyrenderować pliku SVG. Sprawdź instalację Graphviz."
    }
} else {
    Write-Host "Aby wyrenderować SVG automatycznie, uruchom skrypt z parametrem -Render (wymaga Graphviz)."
}

