import math

# ---------------------------------------------------------------------------
# 判断比例：完全按数学比值计算，不迁就任何「习惯叫法」。
# 距离用对数距离 |log(实际宽高比) - log(目标比值)|：
# 这样 2:3 与 3:2 两个方向是对称的，正方形不会偏向竖图。
# ---------------------------------------------------------------------------
TARGETS = [
    ("1:1",  1, 1),
    ("2:3",  2, 3),
    ("3:2",  3, 2),
    ("3:4",  3, 4),
    ("4:3",  4, 3),
    ("5:4",  5, 4),
    ("4:5",  4, 5),
    ("9:16", 9, 16),
    ("16:9", 16, 9),
    ("9:21", 9, 21),
    ("21:9", 21, 9),
    ("1:2",  1, 2),
    ("2:1",  2, 1),
]


def closest_ratio_name(w, h):
    """返回最接近的比例名，纯数学计算（对数距离）。"""
    r = w / h
    return min(
        TARGETS,
        key=lambda t: abs(math.log(r) - math.log(t[1] / t[2])),
    )[0]


class ImageAspectRatio:
    """根据图片宽高判断最接近的比例，并把结果直接显示在节点上。"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    # ratio 用 "STRING"（输出端口显示文本）；ratio_combo 用 "*"（Any）专门连接下拉框
    # （COMBO）输入，例如 Banana / GPT Image 的 aspect_ratio（STRING -> COMBO 会被拒绝）。
    # OUTPUT_NODE = True + ui.text：把判断结果（如 "16:9"）直接显示在节点上，
    # 效果类似 ShowText / PreviewAny。
    RETURN_TYPES = ("STRING", "*")
    RETURN_NAMES = ("ratio", "ratio_combo")
    FUNCTION = "detect"
    CATEGORY = "utils/aspect"
    OUTPUT_NODE = True

    def detect(self, image):
        # IMAGE 形状: (batch, height, width, channels)
        h, w = image.shape[1], image.shape[2]
        name = closest_ratio_name(w, h)
        return {"ui": {"text": [name]}, "result": (name, name)}


NODE_CLASS_MAPPINGS = {"ImageAspectRatio": ImageAspectRatio}
NODE_DISPLAY_NAME_MAPPINGS = {"ImageAspectRatio": "Image Aspect Ratio"}
