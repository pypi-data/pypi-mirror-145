import typer
import pykakasi

app = typer.Typer()
kks = pykakasi.kakasi()


@app.command()
def core(words: str,
         kana: bool = typer.Option(False), k: bool = typer.Option(False),
         romaji: bool = typer.Option(False), r: bool = typer.Option(False),
         detail: bool = typer.Option(False), d: bool = typer.Option(False)):
    result = []
    convert = kks.convert(words)
    for c in convert:
        if kana or k:
            result.append(c['kana'])
        elif romaji or r:
            result.append(c['hepburn'])
        else:
            result.append(c['hira'])
    if detail or d:
        pass
    print(' '.join(result))
