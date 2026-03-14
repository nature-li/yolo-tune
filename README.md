# YOLOv8 篮球服检测微调 Demo

基于 YOLOv8n 微调的目标检测 demo，识别图片中是否存在身穿篮球服的人。演示从数据采集、人工标注、数据增强到模型训练与预测的完整流程。

> **注意：** 受限于数据集规模（约 80 张），模型精度有限，本项目以流程演示为主。

---

## 环境依赖

```bash
pip install ultralytics anylabeling
```

---

## 流程概览

```
采集数据 → 人工标注 → 生成 label → 划分数据集 → 微调训练 → 预测验证
```

---

## 数据准备

### 1. 创建目录

```bash
mkdir -p basket negative
```

### 2. 采集正样本

搜索约 40 张 NBA 比赛图片，保存到 `basket/` 目录。

### 3. 采集负样本

搜索以下各类图片各 10 张，保存到 `negative/` 目录：

- 足球比赛照片
- 普通人街拍
- 跑步运动照片
- 其他人物照片

### 4. 重命名图片

```bash
python step_1_rename.py
```

---

## 标注

使用 [AnyLabeling](https://github.com/vietanhdev/anylabeling) 对 `basket/` 目录下的图片进行人工标注，框选图中穿篮球服的人。

`negative/` 目录下的图片**无需标注**，作为负样本直接参与训练。

![标注示例](docs/nba.jpg)

---

## 数据处理

### 生成 label 文件

```bash
python step_2_generate_label.py
```

### 划分训练集 / 验证集

```bash
python step_3_split_data.py
```

---

## 训练

```bash
python step_4_train.py
```

等价的 CLI 命令：

```bash
yolo detect train \
  model=yolov8n.pt \
  data=data.yaml \
  epochs=80 \
  imgsz=640 \
  project=runs/train \
  name=basket_jersey
```

训练结果保存在 `runs/train/basket_jersey/`。

---

## 预测

```bash
python step_5_predict.py
```

等价的 CLI 命令：

```bash
yolo detect predict \
  model=runs/train/basket_jersey/weights/best.pt \
  source=test/1.jpg
```
