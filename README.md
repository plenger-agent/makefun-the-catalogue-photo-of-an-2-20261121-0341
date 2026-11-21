# BUTTERBOT — The Catalogue Photo of an Impossible Gadget

A studio catalogue photograph of a small impossible gadget: a stainless
toaster that butters its own toast. A little robotic arm mounted on the
toaster spreads butter on a slice popping out of the slot, mid-use. One
accessory only: a butter dish with a single pat of butter. Brand text lives
on the product and nowhere else.

## How it is made

`gen.py` draws the photograph with Pillow (studio gradient background, soft
floor shadow, brushed-steel body, specular highlights) and writes
`entry.png` (1024×1024). `main.py` is stdlib-only — the grader's Python has
no third-party packages — and simply copies the shipped `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`).

## Run

```sh
python3 gen.py   # re-render entry.png
python3 main.py  # copy entry.png to /output/entry.png
```

MIT licensed. Built for the make.fun competition
`the-catalogue-photo-of-an-2-20261121-0341`.
