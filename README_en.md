# Image Aspect Ratio (ComfyUI Custom Node)

English | [中文](README.md)

Detects the closest common aspect ratio from an image's width/height
(1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 5:4 / 4:5 / 9:16 / 16:9 / 9:21 / 21:9 / 1:2 / 2:1),
and outputs only the ratio name (`ratio`).

## 1. Installation

⚠️ ComfyUI only loads `__init__.py` for a "folder-style" custom node — it does not
scan other `.py` files inside the folder. If `__init__.py` is missing, the log shows
`FileNotFoundError: ...__init__.py` and `IMPORT FAILED`, the node appears as a **red box**
on the canvas, and its inputs show `UNKNOWN`.

Correct structure (both files are required):

```
ComfyUI/custom_nodes/aspect_ratio/
├── __init__.py                     # required
└── image_aspect_ratio.py
```

`__init__.py` contents:

```python
from .image_aspect_ratio import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
```

Simpler alternative: drop `image_aspect_ratio.py` directly into `ComfyUI/custom_nodes/`
(without a subfolder) and it will also be loaded.

**Restart ComfyUI** afterwards. The node `Image Aspect Ratio` will appear under the
`utils/aspect` category.

## 2. Usage

- **`image` input** (IMAGE, optional): connect any image output; width/height are read automatically.
- **`width` / `height` inputs** (INT, optional): type numbers directly when no image is connected.
  If both are non-zero, these numbers take priority.
- **`ratio` output** (string): the detected ratio, e.g. `"2:3"`, `"21:9"`.

## 3. Merge into your own workflow

1. Open `aspect_ratio_demo.json` in ComfyUI;
2. Select the `Image Aspect Ratio` node and press `Ctrl+C`;
3. Switch to your own workflow tab and press `Ctrl+V`;
4. Connect your existing image output to this node's `image` input.

## 4. Can't connect to a third-party node's dropdown input? (fixed)

`ratio` is typed `"*"` (Any) instead of `"STRING"` — on purpose.

Inputs like `comfyui-Banana-API-3`'s `aspect_ratio` are declared as
`(["Auto", "1:1", "9:16", ...], {...})`, i.e. type **COMBO (dropdown)**.
ComfyUI's `comfy_execution/validation.py` requires the two types to have a non-empty
intersection, and `STRING` has no intersection with `COMBO`, so a **STRING → COMBO**
connection is rejected:

```
STRING -> COMBO : False   ❌ rejected ("Return type mismatch between linked nodes")
*      -> COMBO : True    ✅ allowed
```

With `"*"` both the frontend and backend allow the link. Of the ratios this node outputs
(1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 5:4 / 4:5 / 9:16 / 16:9 / 9:21 / 21:9 / 1:2 / 2:1),
the first 9 are in Banana's option list; the last 4 (9:21 / 21:9 / 1:2 / 2:1) need the
target dropdown to include them, otherwise the link is allowed but may error at runtime
with an "invalid value".

> Tip: if you ever hit another dropdown input you can't connect, the generic fix is to
> type the upstream output as `"*"` instead of `"STRING"`.
