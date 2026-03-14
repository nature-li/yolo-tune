import os
import re


def rename_images(dir_path, prefix):
    """
    将目录中的 jpg 文件重命名为 prefix_00x.jpg

    参数：
        dir_path : 图片目录，例如 "basket"
        prefix   : 新文件名前缀，例如 "basket" 或 "negative"
    """
    files = os.listdir(dir_path)
    pattern = re.compile(r"\.jpg$", re.IGNORECASE)
    items = []
    # 收集 jpg 文件
    for f in files:
        if pattern.search(f):
            items.append(f)

    # 排序（保证顺序稳定）
    items.sort()
    for i, old_name in enumerate(items, start=1):
        new_name = f"{prefix}_{i:03d}.jpg"
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        print(f"{old_name} -> {new_name}")
        os.rename(old_path, new_path)


if __name__ == "__main__":
    rename_images("basket", "basket")
    rename_images("negative", "negative")
