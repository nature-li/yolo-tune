import os
import json
from pathlib import Path


def json_to_yolo(json_path, txt_path):
    """
    将标注 json 转换为 YOLO txt

    YOLO格式:
    class_id x_center y_center width height
    坐标需要归一化 (0~1)
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    img_w = data["imageWidth"]
    img_h = data["imageHeight"]

    lines = []
    for shape in data["shapes"]:
        label = shape["label"]
        # 这里只有一个类别
        class_id = 0
        points = shape["points"]
        x1, y1 = points[0]
        x2, y2 = points[1]
        x_center = (x1 + x2) / 2 / img_w
        y_center = (y1 + y2) / 2 / img_h
        width = abs(x2 - x1) / img_w
        height = abs(y2 - y1) / img_h
        line = f"{class_id} {x_center} {y_center} {width} {height}"
        lines.append(line)

    with open(txt_path, "w") as f:
        for l in lines:
            f.write(l + "\n")


def generate_labels(image_dir):
    """
    为目录中的图片生成 YOLO 标签

    参数:
        image_dir : basket 或 negative 目录

    逻辑:
        如果存在 json → 解析
        如果不存在 json → 生成空 txt
    """

    image_dir = Path(image_dir)
    for img_path in image_dir.glob("*.jpg"):
        json_path = img_path.with_suffix(".json")
        txt_path = img_path.with_suffix(".txt")
        if json_path.exists():
            print(f"parse json: {json_path}")
            json_to_yolo(json_path, txt_path)

        else:
            print(f"no json -> create empty label: {txt_path}")
            open(txt_path, "w").close()


if __name__ == "__main__":
    generate_labels("basket")
    generate_labels("negative")