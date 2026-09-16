# Image Aspect Ratio（图片比例判断节点）

[English](README_en.md) | 中文

根据图片宽高，判断最接近哪个常用比例
（1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 5:4 / 4:5 / 9:16 / 16:9 / 9:21 / 21:9 / 1:2 / 2:1），
只输出比例名称（`ratio`）。

## 1. 安装节点

⚠️ ComfyUI 对「文件夹形式」的插件**只认 `__init__.py`**，不会去扫描文件夹里的
`.py` 文件。所以文件夹里必须同时有 `__init__.py`，否则日志会报
`FileNotFoundError: ...__init__.py` 和 `IMPORT FAILED`，节点在画布上显示为**红框**、
输入框显示 `UNKNOWN`。

正确结构（两个文件都要）：

```
ComfyUI/custom_nodes/aspect_ratio/
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

- **输入 `image`**（IMAGE，可选）：连接任意图片输出，自动读取宽高。
- **输入 `width` / `height`**（INT，可选）：不连图片时，直接填数值判断。
  如果两者都填了非 0 值，优先使用这里填的数字。
- **输出 `ratio`**（字符串）：判断结果，如 `"2:3"`、`"21:9"`。

## 3. 合并进你自己的工作流

1. 在 ComfyUI 里打开 `aspect_ratio_demo.json`；
2. 选中 `Image Aspect Ratio` 节点，`Ctrl+C`；
3. 切到你自己的工作流标签页，`Ctrl+V` 粘贴；
4. 把你已有的图片输出连到这个节点的 `image` 输入即可。

## 4. 连不上第三方节点的「下拉框」输入？（已修复）

`ratio` 的输出类型是 `"*"`（Any，任意类型）而**不是** `"STRING"`，这是故意的。

像 `comfyui-Banana-API-3` 的 `aspect_ratio` 这种输入，声明形式是
`(["Auto", "1:1", "9:16", ...], {...})`，类型是 **COMBO（下拉框）**。
ComfyUI 后端 `comfy_execution/validation.py` 的校验逻辑是「两边类型必须有交集」，
而 `STRING` 与 `COMBO` 没有任何交集，所以 **STRING → COMBO 的连接会被拒绝**：

```
STRING -> COMBO : False   ❌ 被拒绝（报 Return type mismatch between linked nodes）
*      -> COMBO : True    ✅ 可连
```

改成 `"*"` 后前后端都放行。本节点输出的比例值
（1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 5:4 / 4:5 / 9:16 / 16:9 / 9:21 / 21:9 / 1:2 / 2:1）
中，前 9 个**都在 Banana 插件的可选列表里**；后 4 个（9:21 / 21:9 / 1:2 / 2:1）
需确认目标下拉框是否收录，否则连接虽放行、运行时可能报「值非法」。

> 补充：如果你以后遇到别的「下拉框」输入连不上，通用解法就是把上游节点的
> 输出类型写成 `"*"`，而不是 `"STRING"`。
