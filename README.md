# Image Aspect Ratio（图片比例判断节点）

[English](README_en.md) | 中文

根据图片宽高，判断最接近哪个常用比例
（1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 5:4 / 4:5 / 9:16 / 16:9 / 9:21 / 21:9 / 1:2 / 2:1），
并显示比例名称（`ratio`）。

## 1. 安装节点

⚠️ ComfyUI 对「文件夹形式」的插件**只认 `__init__.py`**，不会去扫描文件夹里的
`.py` 文件。所以文件夹里必须同时有 `__init__.py`，否则日志会报
`FileNotFoundError: ...__init__.py` 和 `IMPORT FAILED`，节点在画布上显示为**红框**、
输入框显示 `UNKNOWN`。

正确结构（两个文件都要）：

```
ComfyUI/custom_nodes/ComfyUI-AspectRatio/
├── __init__.py                     # 必须有
└── image_aspect_ratio.py
```

`__init__.py` 内容：

```python
from .image_aspect_ratio import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
```

更简单的替代方案：把 `image_aspect_ratio.py` 单独丢进 `ComfyUI/custom_nodes/`
根目录（不建子文件夹），也会被正常加载。

放好后**重启 ComfyUI**。之后在节点列表 `utils/aspect` 分类下会看到
`Image Aspect Ratio` 节点。

## 2. 使用

- **输入 `image`**（IMAGE）：连接任意图片输出，自动读取宽高并判断比例。
- **输出 `ratio`**（STRING）：判断结果文本，如 `"2:3"`、`"21:9"`，会直接显示在节点上。
- **输出 `ratio_combo`**（Any）：与 `ratio` 相同的值，专门用于连接下拉框（COMBO）输入，
  如 Banana / GPT Image 的 `aspect_ratio`。

## 3. 合并进你自己的工作流

1. 在 ComfyUI 里打开 `aspect_ratio_demo.json`；
2. 选中 `Image Aspect Ratio` 节点，`Ctrl+C`；
3. 切到你自己的工作流标签页，`Ctrl+V` 粘贴；
4. 把你已有的图片输出连到这个节点的 `image` 输入即可。

本节点输出的比例值可连接到相关的 `aspect_ratio` 输入，包括 Nano Banana 2/Pro 或
GPT Image 2/2.5 的 API 中转站的 `aspect_ratio`。比例值
（1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 5:4 / 4:5 / 9:16 / 16:9 / 9:21 / 21:9 / 1:2 / 2:1）中，
前 9 个都在 Banana 插件的可选列表里；后 4 个（9:21 / 21:9 / 1:2 / 2:1）在
GPT Image 2/2.5 插件的可选列表里。需确认目标下拉框是否收录，否则连接虽放行、
运行时可能报「值非法」。
