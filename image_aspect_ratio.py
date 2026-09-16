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

# ---------------------------------------------------------------------------
# 每种比例的「精确」标准尺寸：宽高严格等于该比例，且都是 64 的倍数。
#
# 这里刻意不用 SDXL 那套习惯尺寸（832x1216、896x1152、768x1344 等），
# 因为那些尺寸并不是精确的 2:3 / 3:4 / 9:16，会和上面的判断结果自相矛盾：
#   例如按习惯把 896x1152 叫 3:4，但它实际是 7:9，本节点会判成 4:5。
# 换成精确值后，判断与输出完全一致 —— 任何一张标准尺寸图喂进来，
# 判出的比例仍然是自己（见 _verify_connect.py 的自洽性测试）。
#
# 注意：9:16 在「64 倍数 + 精确比例」两个约束下，最接近 1MP 的解是 576x1024
#（下一档 1152x2048 是 2.36MP，偏大）。若嫌小，可把下面尺寸表整体放宽到
# 16 倍数，9:16 即可用 720x1280（需自行核对是否满足你所用的底模要求）。
# 21:9（=7:3）同理取 1344x576；1:2 取 704x1408（均已接近 1MP 且为 64 倍数）。
# ---------------------------------------------------------------------------
STANDARD_SIZE = {
    "1:1":  (1024, 1024),
    "2:3":  (768, 1152),
    "3:2":  (1152, 768),
    "3:4":  (768, 1024),
    "4:3":  (1024, 768),
    "5:4":  (1280, 1024),
    "4:5":  (1024, 1280),
    "9:16": (576, 1024),
    "16:9": (1024, 576),
    "9:21": (576, 1344),
    "21:9": (1344, 576),
    "1:2":  (704, 1408),
    "2:1":  (1408, 704),
}


def closest_ratio_name(w, h):
    """返回最接近的比例名，纯数学计算（对数距离）。"""
    r = w / h
    return min(
        TARGETS,
        key=lambda t: abs(math.log(r) - math.log(t[1] / t[2])),
    )[0]


class ImageAspectRatio:
    """根据图片宽高判断最接近的比例，并输出该比例的精确标准尺寸。"""

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
    RETURN_TYPES = ("*", "INT", "INT")
    RETURN_NAMES = ("ratio", "target_width", "target_height")
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
        tw, th = STANDARD_SIZE[name]
        return (name, tw, th)


NODE_CLASS_MAPPINGS = {"ImageAspectRatio": ImageAspectRatio}
NODE_DISPLAY_NAME_MAPPINGS = {"ImageAspectRatio": "Image Aspect Ratio"}
