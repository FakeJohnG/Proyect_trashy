"""Convierte un dataset exportado de Roboflow (formato YOLO) de subclases a las clases finales.

Uso, desde la raíz del repo:
    python scripts/agrupar_clases.py --src /content/Residuos-1 --dst /content/residuos_v1

Qué hace:
  1. Lee los nombres de las subclases del data.yaml que exportó Roboflow
     (esa es la fuente de verdad de los ids).
  2. Usa configs/mapeo_clases.json para saber a qué clase final va cada subclase.
  3. Copia las imágenes y reescribe el primer número de cada línea de las etiquetas
     (el id de la clase) con el id de la clase final.
  4. Escribe un data_v1.yaml listo para entrenar con Ultralytics.
"""
import argparse
import json
import shutil
from collections import Counter
from pathlib import Path

import yaml

# Roboflow nombra las carpetas train / valid / test.
# Aquí las dejamos como images/train, images/val, images/test.
SPLITS = {"train": "train", "val": "valid", "test": "test"}


def leer_names(ruta_yaml):
    """Devuelve {id: nombre} desde un archivo yaml con la clave 'names'."""
    with open(ruta_yaml, encoding="utf-8") as f:
        names = yaml.safe_load(f)["names"]
    if isinstance(names, list):  # a veces Roboflow exporta una lista en vez de un dict
        names = dict(enumerate(names))
    return {int(i): nombre for i, nombre in names.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--src", required=True, help="Carpeta del dataset exportado de Roboflow")
    ap.add_argument("--dst", required=True, help="Carpeta donde se crea el dataset agrupado")
    ap.add_argument("--configs", default="configs", help="Carpeta con mapeo_clases.json y data_v1.yaml")
    args = ap.parse_args()

    src, dst, configs = Path(args.src), Path(args.dst), Path(args.configs)

    fino = leer_names(src / "data.yaml")                       # {id fino: nombre}
    finales = leer_names(configs / "data_v1.yaml")             # {id final: nombre}
    mapeo = json.loads((configs / "mapeo_clases.json").read_text(encoding="utf-8"))
    id_final = {nombre: i for i, nombre in finales.items()}    # {nombre final: id}

    # Comprobaciones: mejor parar con un aviso claro que etiquetar mal en silencio.
    sin_mapeo = [n for n in fino.values() if n not in mapeo]
    if sin_mapeo:
        raise SystemExit(f"Subclases del dataset sin mapeo en mapeo_clases.json: {sin_mapeo}")
    destino_invalido = sorted({v for v in mapeo.values() if v not in id_final})
    if destino_invalido:
        raise SystemExit(f"El mapeo apunta a clases que no existen en data_v1.yaml: {destino_invalido}")

    remap = {i: id_final[mapeo[nombre]] for i, nombre in fino.items()}  # id fino -> id final

    if dst.exists():
        shutil.rmtree(dst)  # empezar limpio para no mezclar con una corrida anterior

    cuenta = {}
    for destino, origen in SPLITS.items():
        img_src, lbl_src = src / origen / "images", src / origen / "labels"
        if not img_src.exists():
            print(f"(no hay carpeta '{origen}', se omite)")
            continue
        (dst / "images" / destino).mkdir(parents=True)
        (dst / "labels" / destino).mkdir(parents=True)
        for img in img_src.iterdir():
            shutil.copy(img, dst / "images" / destino / img.name)

        cuenta[destino] = Counter()
        for lbl in lbl_src.glob("*.txt"):
            lineas = []
            for linea in lbl.read_text().splitlines():
                partes = linea.split()
                if not partes:
                    continue
                nuevo = remap[int(partes[0])]
                partes[0] = str(nuevo)
                lineas.append(" ".join(partes))
                cuenta[destino][finales[nuevo]] += 1
            (dst / "labels" / destino / lbl.name).write_text("\n".join(lineas))

    data = {
        "path": str(dst.resolve()),
        "train": "images/train",
        "val": "images/val",
        "names": finales,
    }
    if (dst / "images" / "test").exists():
        data["test"] = "images/test"
    (dst / "data_v1.yaml").write_text(yaml.dump(data, allow_unicode=True, sort_keys=False))

    print(f"Dataset agrupado en: {dst}")
    for split, c in cuenta.items():
        print(f"  {split}: {dict(c)}")


if __name__ == "__main__":
    main()
