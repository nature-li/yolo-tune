from pathlib import Path
from ultralytics import YOLO


def predict_images(
    model_path: str = "runs/train/basket_jersey/weights/best.pt",
    source: str = "dataset/images/val",
    imgsz: int = 640,
    conf: float = 0.25,
    save: bool = True,
    project: str = "runs/predict",
    name: str = "basket_jersey_pred",
) -> None:
    """
    使用训练好的 YOLO 模型进行预测

    参数:
        model_path: 模型权重路径，通常是 best.pt
        source: 待预测的图片路径，可以是：
                1. 单张图片路径
                2. 图片目录
        imgsz: 推理输入尺寸
        conf: 置信度阈值，低于该值的框会被过滤
        save: 是否保存可视化结果图
        project: 预测结果输出根目录
        name: 本次预测任务名称

    输出:
        预测后的可视化图片通常保存在：
        runs/predict/basket_jersey_pred/
    """
    model_file = Path(model_path)
    if not model_file.exists():
        raise FileNotFoundError(f"找不到模型文件: {model_path}")

    src_path = Path(source)
    if not src_path.exists():
        raise FileNotFoundError(f"找不到待预测路径: {source}")

    model = YOLO(model_path)

    results = model.predict(
        source=str(src_path),
        imgsz=imgsz,
        conf=conf,
        save=save,
        project=project,
        name=name,
        verbose=True,
        exist_ok=True,
    )

    print(f"\n预测完成，共返回 {len(results)} 个结果对象")
    print(f"结果目录: {Path(project) / name}")


if __name__ == "__main__":
    predict_images(
        model_path="runs/detect/runs/train/basket_jersey/weights/best.pt",
        source="test",   # 可以改成单张图，比如 "test.jpg"
        imgsz=640,
        conf=0.25,
        save=True,
        project="runs/predict",
        name="basket_jersey_pred",
    )