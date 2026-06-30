Generowanie diagramu klas
=========================

Pliki:
- `generate_viz.py` — skrypt Python, który skanuje projekt i generuje diagram klas (Graphviz).
- `update_diagram.ps1` — skrypt PowerShell do szybkiego wygenerowania pliku .dot i opcjonalnego wyrenderowania SVG.

Szybkie kroki (Windows PowerShell):

1. Zainstaluj zależności Pythona (w środowisku projektu):

   python -m pip install -r .\requirements.txt

2. Wygeneruj tylko plik .dot (bez potrzeby instalowania Graphviz systemowego):

   PowerShell -File .\scripts\update_diagram.ps1

3. Wygeneruj i wyrenderuj SVG (wymaga zainstalowanego Graphviz i `dot` w PATH):

   PowerShell -File .\scripts\update_diagram.ps1 -Render

Możesz też uruchomić bezpośrednio skrypt Pythona:

   python .\scripts\generate_viz.py --root . --output .\scripts\class_diagram.svg --dot-only

Po wygenerowaniu plików znajdziesz:
- `scripts/class_diagram.dot` — źródło Graphviz (.dot)
- `scripts/class_diagram.svg` — wygenerowany SVG (jeśli wyrenderowano)

Jeżeli chcesz rozbudować parser (np. wykrywanie pól/atrybutów, relacji asocjacji), mogę dodać to do `generate_viz.py`.

