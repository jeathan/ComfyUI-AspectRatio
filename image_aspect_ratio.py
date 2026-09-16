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
    """根据图片宽高判断最接近的比例，并输出该比例名称。"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
                "height": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
            },
        }

    # ratio 用 "*"（Any）而不是 "STRING"：
    # ComfyUI 后端 comfy_execution/validation.py 会拒绝 STRING -> COMBO 的连接
    # （STRING 与 COMBO 无类型交集），而 "*" 可以连到任何输入，
    # 包括 comfyui-Banana-API-3 的 aspect_ratio 这类下拉框输入。
    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("ratio",)
    FUNCTION = "detect"
    CATEGORY = "utils/aspect"

    def detect(self, image=None, width=0, height=0):
        # 优先使用显式传入的宽高，其次从图片张量读取
        if width > 0 and height > 0:
            w, h = width, height
        elif image is not None:
            # IMAGE 形状: (batch, height, width, channels)
            h, w = image.shape[1], image.shape[2]
        else:
            raise ValueError("ImageAspectRatio: 需要连接 image，或填写 width/height")

        name = closest_ratio_name(w, h)
        return (name,)


NODE_CLASS_MAPPINGS = {"ImageAspectRatio": ImageAspectRatio}
NODE_DISPLAY_NAME_MAPPINGS = {"ImageAspectRatio": "Image Aspect Ratio"}
