"""
Generuje diagram klas i metod projektu w formacie SVG/PDF używając biblioteki graphviz.

Użycie:
    python scripts/generate_viz.py --output class_diagram.svg

Wymagania:
    pip install graphviz
    (na Windowsie trzeba też zainstalować Graphviz i dodać do PATH: https://graphviz.org/download/)

Skrypt skanuje pliki .py w katalogu projektu (pomijając wirtualne środowiska i katalogi __pycache__)
i tworzy diagram, gdzie każdy węzeł to klasa z listą jej metod.
"""
from __future__ import annotations

import ast
import os
import argparse
from typing import Dict, List, Tuple

try:
    from graphviz import Digraph
except Exception as e:
    raise SystemExit(
        "Biblioteka 'graphviz' nie jest zainstalowana. Zainstaluj ją: pip install graphviz"
    )


IGNORED_DIRS = {"venv", "env", ".venv", ".env", "__pycache__", "htmlcov", "backup"}


def collect_python_files(root: str) -> List[str]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # pomiń ignorowane katalogi
        parts = set(dirpath.split(os.sep))
        if parts & IGNORED_DIRS:
            continue
        for fname in filenames:
            if fname.endswith(".py"):
                files.append(os.path.join(dirpath, fname))
    return files


def parse_file(path: str) -> List[ast.AST]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=path)
        return tree.body
    except Exception:
        return []


def extract_classes_from_file(path: str) -> Dict[str, Dict]:
    classes: Dict[str, Dict] = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=path)
    except Exception:
        return classes

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            cls_name = node.name
            methods: List[Tuple[str, str]] = []  # (name, type)
            bases = [get_base_name(b) for b in node.bases]
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    mtype = "method"
                    # sprawdź dekoratory na @classmethod/@staticmethod
                    for dec in item.decorator_list:
                        if isinstance(dec, ast.Name) and dec.id == "classmethod":
                            mtype = "classmethod"
                        elif isinstance(dec, ast.Name) and dec.id == "staticmethod":
                            mtype = "staticmethod"
                    methods.append((item.name, mtype))
            classes[cls_name] = {"methods": methods, "bases": bases, "file": path}
    return classes


def get_base_name(node) -> str:
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        parts = []
        curr = node
        while isinstance(curr, ast.Attribute):
            parts.append(curr.attr)
            curr = curr.value
        if isinstance(curr, ast.Name):
            parts.append(curr.id)
        return ".".join(reversed(parts))
    elif isinstance(node, ast.Subscript):
        # typing generics like Generic[T]
        return get_base_name(node.value)
    return "?"


def build_class_map(root: str) -> Dict[str, Dict]:
    py_files = collect_python_files(root)
    class_map: Dict[str, Dict] = {}
    for p in py_files:
        found = extract_classes_from_file(p)
        for k, v in found.items():
            # jeśli nazwa powtarza się, dodaj sufiks z nazwą pliku modułu
            if k in class_map:
                key = f"{k} ({os.path.splitext(os.path.basename(p))[0]})"
            else:
                key = k
            class_map[key] = v
    return class_map


def render_diagram(class_map: Dict[str, Dict], output: str, engine: str = "dot") -> None:
    dot = Digraph("Classes", format=os.path.splitext(output)[1].lstrip("."), engine=engine)
    dot.attr(rankdir="LR")
    for cls, info in class_map.items():
        method_lines = []
        for name, mtype in info["methods"]:
            prefix = "~" if mtype == "method" else ("C:" if mtype == "classmethod" else "S:")
            method_lines.append(f"{prefix} {name}()")
        label = "{" + cls + "|" + "\\l".join(method_lines) + "\\l}" if method_lines else cls
        dot.node(cls, label=label, shape="record")

    # relacje dziedziczenia
    for cls, info in class_map.items():
        for base in info.get("bases", []):
            # jeśli baza istnieje w mapie, narysuj krawędź
            for candidate in class_map.keys():
                if candidate.split(" (")[0] == base:
                    dot.edge(candidate, cls, arrowhead="empty")

    # Spróbuj wyrenderować przy pomocy zainstalowanej binarki Graphviz. Jeśli to się nie powiedzie,
    # zapisz plik .dot aby użytkownik mógł wyrenderować go lokalnie później.
    try:
        out = dot.render(filename=os.path.splitext(output)[0], cleanup=True)
        print(f"Wygenerowano: {out}")
    except Exception:
        dot_path = os.path.splitext(output)[0] + ".dot"
        with open(dot_path, "w", encoding="utf-8") as f:
            f.write(dot.source)
        print(f"Zapisano plik .dot: {dot_path} (brak binarki Graphviz lub błąd renderowania)")


def main():
    parser = argparse.ArgumentParser(description="Generuj diagram klas projektu (graphviz)")
    parser.add_argument("--root", default=".", help="Katalog projektu (domyślnie .)")
    parser.add_argument("--output", default="class_diagram.svg", help="Plik wyjściowy (svg, pdf, png)")
    parser.add_argument("--engine", default="dot", help="Silnik graphviz (dot, neato...)")
    parser.add_argument("--dot-only", action="store_true", help="Zapisz tylko plik .dot bez próby uruchamiania binarki Graphviz")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    class_map = build_class_map(root)
    if not class_map:
        print("Nie znaleziono klas w projekcie.")
        return
    if args.dot_only:
        # jeśli użytkownik chce tylko .dot, wymuśmy zapis źródła
        dot = Digraph("Classes", format=os.path.splitext(args.output)[1].lstrip("."), engine=args.engine)
        dot.attr(rankdir="LR")
        for cls, info in class_map.items():
            method_lines = []
            for name, mtype in info["methods"]:
                prefix = "~" if mtype == "method" else ("C:" if mtype == "classmethod" else "S:")
                method_lines.append(f"{prefix} {name}()")
            label = "{" + cls + "|" + "\\l".join(method_lines) + "\\l}" if method_lines else cls
            dot.node(cls, label=label, shape="record")
        dot_path = os.path.splitext(args.output)[0] + ".dot"
        with open(dot_path, "w", encoding="utf-8") as f:
            f.write(dot.source)
        print(f"Zapisano plik .dot: {dot_path}")
    else:
        render_diagram(class_map, args.output, engine=args.engine)


if __name__ == "__main__":
    main()

