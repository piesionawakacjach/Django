
## zadanie domowe na następne spoktanie:
- dopisać views oraz html który wyświetli komentarz/e do zadania.
* jak ktoś chce spróbować może dorobić formularz dodania komentarza do zadania


# Django — projekt przykładowy

To repozytorium zawiera prosty projekt Django (aplikacja `devboard`) używany do ćwiczeń i zajęć.
Dokumentacja opisuje sposób przygotowania środowiska, uruchamiania aplikacji, wykonywania testów oraz generowania diagramu klas.


Spis treści
- Opis projektu
- Wymagania
- Szybkie uruchomienie (Windows)
- Testy
- Generowanie diagramu klas (Graphviz)
- Struktura repozytorium
- Jak rozwijać / wnosić zmiany

Opis projektu
---
Projekt zawiera prostą aplikację Django `devboard` (models, views, forms) — przykład aplikacji do śledzenia projektów i zadań.

Wymagania
---
- Python 3.10+ (projekt był rozwijany z wykorzystaniem Pythona 3.14 — dostosuj według środowiska)
- virtualenv (opcjonalnie, zalecane)
- zależności Python: plik `requirements.txt`
- (opcjonalnie) Graphviz — aby automatycznie wyrenderować diagramy SVG (`dot` w PATH)

Instalacja zależności (Windows PowerShell)

1) Utwórz i aktywuj wirtualne środowisko (opcjonalne, ale zalecane):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Zainstaluj zależności Pythona:

```powershell
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

Szybkie uruchomienie aplikacji (Windows PowerShell)

```powershell
# aktywuj wirtualne środowisko, jeśli jeszcze nie jest aktywne
.\.venv\Scripts\Activate.ps1
# uruchom serwer deweloperski
python manage.py runserver
```

Po uruchomieniu otwórz w przeglądarce: http://127.0.0.1:8000/

Migracje i baza danych

Projekt zawiera plik `db.sqlite3` i migracje w katalogu `devboard/migrations`. Jeśli chcesz zresetować bazę:

```powershell
# utwórz migracje (jeśli wprowadzasz zmiany)
python manage.py makemigrations
python manage.py migrate
```

Testy
---
Uruchom testy za pomocą pytest (plik `pytest.ini` jest skonfigurowany):

```powershell
python -m pytest -q
```

Generowanie diagramu klas
---
W repozytorium dodałem narzędzie do wygenerowania diagramu klas w formacie Graphviz (.dot) oraz skrypt PowerShell do wygodnego użycia.

- Skrypt Python: `scripts/generate_viz.py` — skanuje pliki .py i tworzy diagram klas oraz metod.
- Helper PowerShell: `scripts/update_diagram.ps1` — generuje `.dot` i (opcjonalnie) wyrenderowuje SVG używając `dot`.

Aby tylko wygenerować źródło `.dot` bez instalowania systemowego Graphviz:

```powershell
PowerShell -File .\scripts\update_diagram.ps1
```

Jeżeli masz zainstalowany Graphviz (binarki, w szczególności `dot`, w PATH) i chcesz od razu SVG:

```powershell
PowerShell -File .\scripts\update_diagram.ps1 -Render
```

Możesz też uruchomić bezpośrednio Pythona:

```powershell
python .\scripts\generate_viz.py --root . --output .\scripts\class_diagram.svg
# lub tylko zapisz .dot
python .\scripts\generate_viz.py --root . --output .\scripts\class_diagram.svg --dot-only
```

Wygenerowany plik `.dot` znajdziesz pod `scripts/class_diagram.dot`, a SVG (jeśli wyrenderowano) pod `scripts/class_diagram.svg`.

Struktura repozytorium
---
Główne pliki i katalogi:

- `manage.py` — punkt wejścia Django
- `db.sqlite3` — lokalna baza SQLite (przykładowa)
- `config/` — konfiguracja projektu (asgi, wsgi, ustawienia environment)
- `devboard/` — główna aplikacja: modele, widoki, formularze, testy
- `scripts/` — pomocnicze skrypty (generator diagramu, PS helper i dokumentacja)
- `requirements.txt` — zależności Python

Jak rozwijać projekt / dobre praktyki
---
- Przed wprowadzeniem zmian zrób branch feature:

```powershell
git checkout -b feature/nazwa-funkcjonalnosci
```

- Pisz testy dla nowych zachowań i uruchom `pytest` lokalnie.
- Jeśli dodajesz lub zmieniasz modele, utwórz migracje: `python manage.py makemigrations` i `python manage.py migrate`.

Wkład i zgłaszanie błędów
---
- Zgłaszaj problemy (issues) z opisem kroku reprodukcji i oczekiwanego zachowania.
- Twórz pull requesty z opisem zmian i, jeżeli to możliwe, przykładowymi testami.

Kontakt / dalsze kroki
---
Jeśli chcesz, mogę rozszerzyć dokumentację o:
- diagram architektury (workflow request -> view -> model)
- szczegółowy opis modeli i API
- instrukcje deploy (Docker, Heroku, itp.)

-----

Plik ten zastępuje poprzednią, krótką notatkę i ma być centralnym punktem dokumentacji projektu. Pliki pomocnicze (np. `scripts/README.md`) zawierają szczegóły dotyczące swoich narzędzi.
