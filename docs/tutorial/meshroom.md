# 3D 重建入门教程（基于 Meshroom）（英才广场爱因斯坦像）



## 一、实验环境配置

| 组件 | 版本 / 说明 |
|------|------------|
| 操作系统 | Windows 11 23H2 (Build 22631.6060) |
| GPU | NVIDIA GeForce RTX 4090 Laptop GPU |
| 驱动版本 | 560.78 |
| CUDA 版本 | 12.6 |
| 软件 | Meshroom 2023.3.0 |
| Python 环境 | 内置 3.7.4（仅部分插件使用） |

**建议：**

- 显卡驱动需与 CUDA 兼容  
- 安装 Visual C++ Redistributable  
- 保证 D:\ 或 C:\ 盘有 ≥ 20GB 空间  

---

## 二、数据采集与拍摄注意事项

### 1️⃣ 拍摄设备与模式

- 使用防抖、固定焦距设备  
- 若使用手机，开启“专业模式”，固定焦距、ISO、快门  
- 保存 `.JPG + .DNG（RAW）` 双格式更佳  

### 2️⃣ 拍摄参数一致性

- 固定焦段（26mm–28mm 等效焦距）  
- 白平衡固定  
- 不混用不同镜头焦段  

### 3️⃣ 拍摄数量与角度布局

- 建议 ≥ 60 张照片  
- 相邻重叠度 ≥ 70%  
- 拍摄两圈（水平 + 俯视或仰视）  

### 4️⃣ 文件整理

- 将所有照片放入 `images/` 文件夹  
- 文件名用英文和数字，避免中文空格  

---

## 三、Meshroom 模块与参数说明

### 1️⃣ CameraInit
- 读取相机参数  
- 手机拍摄需确保 EXIF 正确  
- 若 Sensor Width 缺失，需手动设置  

### 2️⃣ FeatureExtraction
- 提取特征点（SIFT）  
- 推荐设置：
  - Describer Preset: High  
  - Max Nb Features: 8000–10000  
  - Image Downscale: 1  

### 3️⃣ ImageMatching
- 生成候选图像对  
- 参数：
  - Geometric Model: Similarity  
  - Distance Ratio: 0.8  
  - Max Residual Error: 4.0  

### 4️⃣ FeatureMatching
- 匹配特征点  
- 可启用 GPU  
- 若匹配稀疏，调高 Match Nearest Neighbor Ratio  

### 5️⃣ StructureFromMotion (SfM)
- 计算相机位姿与稀疏点云  
- 参数：
  - Describer Types: SIFT  
  - Min Observation: 3  
- 输出文件：`sfm.abc`  

### 6️⃣ PrepareDenseScene
- 准备稠密点云输入  
- 默认即可  

### 7️⃣ DepthMap
- 生成深度图  
- 参数：
  - Downscale: 2  
  - Min Consistent Views: 3  
- 使用 GPU  

### 8️⃣ DepthMapFilter
- 滤除噪声  
- 参数：
  - Sigma: 1.5  
  - Nviews: 4  

### 9️⃣ Meshing
- 稠密点云 → 三角网格  
- 参数：
  - Max Input Points: 15,000,000  
  - Meshing Method: Multi-View  
- 输出 `.obj`  

### 🔟 MeshFiltering
- 平滑网格  
- Smoothing Iterations: 3–5  
- 可启用 Decimation 减小模型  

### 🧩 Texturing
- 生成纹理  
- 参数：
  - Texture Side: 4096  
  - Unwrap Method: Basic  
- 输出 `.obj + .mtl + .png`  

---

## 四、常见问题与优化建议

| 问题 | 解决办法 |
|------|-----------|
| 无法读取相机参数 | 手动设置 Sensor Width |
| 特征匹配稀疏 | 提高 Describer Preset |
| 模型噪声多 | 调高 DepthMapFilter Sigma |
| 纹理模糊 | 提升 Texture Side 或使用 RAW 图像 |

---

## 五、工程文件与成果组织建议
- Meshroom_Project/
  - images/             # 原始照片
  - MeshroomCache/      # 中间结果
  - 3D_Model/           # 输出结果
    - texturedMesh.obj
    - texturedMesh.mtl
    - texturedMesh.png
  - project.mg          # 工程文件
  - README.md           # 项目说明


**.obj 文件可用软件：**  
- MeshLab  
- Blender  
- Windows 3D 查看器  

重建效果：
![重建结果](../img/model_preview.png)


导入湖工商场景后的效果：

![](../img/hutb/Einstein.jpg)

![](../img/hutb/hutb_air.jpg)


## 使用方法

- [下载 3D 模型](https://pan.quark.cn/s/9d989d5757d9)
- [完整地图下载链接](../core_map.md#non-layered-maps)
- [完整资产仓库链接](https://git.code.tencent.com/OpenHUTB/Content) - 获取所有地图资产仓库修改权限请发送邮件到 open@hutb.edu.cn
- [基于摄影测量的三维重建详细教程](https://openhutb.github.io/3d/)


* 导入：打开 Blender，点击`文档`菜单 -> 导入 -> Wavefront(.obj)，选择下载的`texturedMesh.obj`，打开，点击右上角圆球的`视图着色方式：材质预览`，即可看到模型效果。

* 删除和模型无关的内容：点击`UV编辑`，点击右上角`视图着色方式：线框`（否则大部分的点选不中），选择不需要的部分按`Del`键，点击`顶点`。

---

**作者：** 夏庆森  
**环境：** Windows 11 + NVIDIA RTX 4090 + Meshroom 2023.3.0  
**拍摄设备：** iPhone 14 Pro Max（约 60 张照片）  
**适用对象：** 初学者，研究性学习、重建实验记录