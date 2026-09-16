# Image Aspect Ratio (ComfyUI Custom Node)

English | [中文](README.md)

Detects the closest common aspect ratio from an image's width/height
(1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 5:4 / 4:5 / 9:16 / 16:9 / 9:21 / 21:9 / 1:2 / 2:1),
and displays the ratio name (`ratio`).

## 1. Installation

⚠️ ComfyUI only loads `__init__.py` for a "folder-style" custom node — it does not
scan other `.py` files inside the folder. If `__init__.py` is missing, the log shows
`FileNotFoundError: ...__init__.py` and `IMPORT FAILED`, the node appears as a **red box**
on the canvas, and its inputs show `UNKNOWN`.

Correct structure (both files are required):

```
ComfyUI/custom_nodes/ComfyUI-AspectRatio/
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

- **`image` input** (IMAGE): connect any image output; width/height are read and the ratio is detected automatically.
- **`ratio` output** (STRING): the detected ratio text, e.g. `"2:3"`, `"21:9"`, shown directly on the node.
- **`ratio_combo` output** (Any): the same value, meant for connecting to dropdown (COMBO) inputs
  such as Banana / GPT Image's `aspect_ratio`.

## 3. Merge into your own workflow

1. Open `aspect_ratio_demo.json` in ComfyUI;
2. Select the `Image Aspect Ratio` node and press `Ctrl+C`;
3. Switch to your own workflow tab and press `Ctrl+V`;
4. Connect your existing image output to this node's `image` input.

This node's ratio output can be connected to the relevant `aspect_ratio` input, including
the `aspect_ratio` of the Nano Banana 2/Pro or GPT Image 2/2.5 API relay stations. Of the
ratios (1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 5:4 / 4:5 / 9:16 / 16:9 / 9:21 / 21:9 / 1:2 / 2:1),
the first 9 are in the Banana plugin's option list; the last 4 (9:21 / 21:9 / 1:2 / 2:1)
are in the GPT Image 2/2.5 plugin's option list. Please confirm the target dropdown
includes the value, otherwise the link is allowed but may error at runtime with an
"invalid value".
