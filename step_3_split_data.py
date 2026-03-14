import random
import shutil
from pathlib import Path


def collect_samples(src_dir):
    """
    收集一个目录中的样本信息

    参数:
        src_dir: 源目录，例如 basket 或 negative
    返回:
        samples: 列表，元素为 (img_path, txt_path)
    逻辑:
        1. 扫描目录下所有 jpg 文件
        2. 检查是否存在同名 txt
        3. 如果不存在 txt，报错
        4. 返回图片和标签路径对
    """
    src_dir = Path(src_dir)
    samples = []

    for img_path in sorted(src_dir.glob("*.jpg")):
        txt_path = img_path.with_suffix(".txt")
        if not txt_path.exists():
            raise FileNotFoundError(f"找不到对应标签文件: {txt_path}")
        samples.append((img_path, txt_path))
    return samples


def ensure_dir(path):
    """
    确保目录存在，不存在则创建

    参数:
        path: 目录路径
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def reset_dataset_dirs(output_dir):
    """
    重建输出目录结构

    参数:
        output_dir: 输出根目录，例如 dataset

    目录结构:
        dataset/
        ├── images/train
        ├── images/val
        ├── labels/train
        └── labels/val
    """
    output_dir = Path(output_dir)
    if output_dir.exists():
        shutil.rmtree(output_dir)

    ensure_dir(output_dir / "images" / "train")
    ensure_dir(output_dir / "images" / "val")
    ensure_dir(output_dir / "labels" / "train")
    ensure_dir(output_dir / "labels" / "val")


def split_samples(samples, train_ratio=0.8, seed=42):
    """
    将样本划分为训练集和验证集

    参数:
        samples: [(img_path, txt_path), ...]
        train_ratio: 训练集比例，例如 0.8
        seed: 随机种子，保证每次划分结果可复现

    返回:
        train_samples, val_samples
    """
    samples = samples[:]
    random.seed(seed)
    random.shuffle(samples)

    train_count = int(len(samples) * train_ratio)
    train_samples = samples[:train_count]
    val_samples = samples[train_count:]

    return train_samples, val_samples


def copy_samples(samples, output_dir, split_name):
    """
    将样本复制到目标目录

    参数:
        samples: [(img_path, txt_path), ...]
        output_dir: 输出根目录，例如 dataset
        split_name: train 或 val

    复制结果:
        图片 -> dataset/images/train 或 val
        标签 -> dataset/labels/train 或 val
    """
    output_dir = Path(output_dir)

    image_dst_dir = output_dir / "images" / split_name
    label_dst_dir = output_dir / "labels" / split_name

    for img_path, txt_path in samples:
        shutil.copy2(img_path, image_dst_dir / img_path.name)
        shutil.copy2(txt_path, label_dst_dir / txt_path.name)


def organize_yolo_dataset(
    basket_dir="basket",
    negative_dir="negative",
    output_dir="dataset",
    train_ratio=0.8,
    seed=42,
):
    """
    组织 YOLO 数据集

    参数:
        basket_dir: 正样本目录，里面通常有目标
        negative_dir: 负样本目录，通常是空标签
        output_dir: 输出目录
        train_ratio: 训练集比例
        seed: 随机种子

    逻辑:
        1. 收集 basket 和 negative 中的样本
        2. 分别做 train/val 划分
           - 这样能保证正负样本都会进入 train 和 val
        3. 创建 dataset 目录结构
        4. 复制图片和标签
        5. 打印统计信息
    """
    basket_samples = collect_samples(basket_dir)
    negative_samples = collect_samples(negative_dir)

    basket_train, basket_val = split_samples(
        basket_samples, train_ratio=train_ratio, seed=seed
    )
    negative_train, negative_val = split_samples(
        negative_samples, train_ratio=train_ratio, seed=seed
    )

    train_samples = basket_train + negative_train
    val_samples = basket_val + negative_val

    reset_dataset_dirs(output_dir)

    copy_samples(train_samples, output_dir, "train")
    copy_samples(val_samples, output_dir, "val")

    print("数据集组织完成")
    print(f"basket 总数   : {len(basket_samples)}")
    print(f"negative 总数 : {len(negative_samples)}")
    print(f"train 总数    : {len(train_samples)}")
    print(f"val 总数      : {len(val_samples)}")
    print()
    print(f"basket train  : {len(basket_train)}")
    print(f"basket val    : {len(basket_val)}")
    print(f"negative train: {len(negative_train)}")
    print(f"negative val  : {len(negative_val)}")


if __name__ == "__main__":
    organize_yolo_dataset(
        basket_dir="basket",
        negative_dir="negative",
        output_dir="dataset",
        train_ratio=0.8,
        seed=84,
    )