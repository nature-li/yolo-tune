from pathlib import Path
from ultralytics import YOLO


def train_yolo(
    model_path: str = "yolov8n.pt",
    data_path: str = "data.yaml",
    epochs: int = 80,
    imgsz: int = 640,
    batch: int = 16,
    device: int | str = 0,
    project: str = "runs/train",
    name: str = "jersey_det",
    workers: int = 4,
    pretrained: bool = True,
) -> None:
    """
    训练 YOLO 检测模型

    参数:
        model_path: 预训练模型路径，例如 yolov8n.pt
        data_path: 数据集配置文件路径，例如 data.yaml
        epochs: 训练轮数
        imgsz: 输入图片尺寸
        batch: batch size
        device: 训练设备，0 表示第 0 块 GPU，'cpu' 表示 CPU
        project: 训练结果输出根目录
        name: 本次实验名称
        workers: DataLoader 的 worker 数量
        pretrained: 是否使用预训练权重

    说明:
        训练完成后，结果通常保存在:
        runs/train/jersey_det/

        其中最重要的文件:
        - weights/best.pt
        - weights/last.pt
    """
    data_file = Path(data_path)
    if not data_file.exists():
        raise FileNotFoundError(f"找不到数据配置文件: {data_path}")

    model = YOLO(model_path)

    model.train(
        data=str(data_file),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=device,
        project=project,
        name=name,
        workers=workers,
        pretrained=pretrained,
        verbose=True,
    )


if __name__ == "__main__":
    train_yolo(
        model_path="yolov8n.pt",   # 预训练模型
        data_path="data.yaml",     # 你的数据集配置
        epochs=80,                 # 训练轮数
        imgsz=640,                 # 输入尺寸
        batch=16,                  # 可按显存调整
        device=0,                  # 0 表示使用第一张 GPU；没有 GPU 可写 "cpu"
        project="runs/train",
        name="basket_jersey",
        workers=4,
        pretrained=True,
    )