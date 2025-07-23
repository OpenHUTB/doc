# geom模块概述

`carla::geom` 是 HUTB 引擎中专门负责几何计算和坐标变换的模块。它提供了常用的几何基本类型（如二维/三维向量、整数向量）、位置（Location）、旋转（Rotation）和变换（Transform）等数据结构，以及相关的数学工具函数。该模块还实现了经纬度与世界坐标的转换（GeoLocation 和 Mercator 投影函数）、有向边界框（BoundingBox）计算、样条曲线（CubicPolynomial）等功能。此外，它包含网格（Mesh）和网格生成（MeshFactory）类用于道路和场景几何的构造，以及网格简化（Simplification）和基于 R 树的空间索引（PointCloudRtree、SegmentCloudRtree）等高级功能。总体而言，`geom` 模块负责车辆、自行车、路网等对象的几何表示及其间的空间运算与变换。

- ## 目录
  1. [主要类与功能说明](#主要类与功能说明)
  2. [其他模块的引用](#其他模块的引用)
  3. [Math](#Math)
  4. [Vector3D/Vector2D/Vector3DInt](#Vector3D/Vector2D/Vector3DInt)
  5. [Mesh](#Mesh)
  6. [Simplification](#Simplification)
  7. [RTree](#RTree)
  8. [Location](#Location)
  9. [Rotation](#Rotation)
  10. [Transform](#Transform)
  11. [CubicPolynomial](#CubicPolynomial)
  12. [BoundingBox](#BoundingBox)
  13. [GeoLocation](#GeoLocation)
  <span id="主要类与功能说明"></span>
## 主要类与功能说明

- **[Vector2D/Vector3D/Vector3DInt](#Vector3D/Vector2D/Vector3DInt)**：分别表示二维浮点向量、三维浮点向量和三维整型向量，支持算术运算（加减、点乘、叉乘等）、长度计算、归一化等常见操作。
- **[Location](#Location)**：三维位置类，继承自 `Vector3D`，并提供了位置之间的欧氏距离等额外功能。
- **[Rotation](#Rotation)**：旋转类（俯仰、偏航、横滚），可转换为对应的方向向量和旋转矩阵等。
- **[Transform](#Transform)**：变换类，由位置（Location）和旋转（Rotation）构成，支持将点从本地坐标系转换到世界坐标系（以及逆变换）。
- **[Math](#Math)**：静态数学工具类，提供夹取、距离（3D/2D）、点到线段距离、向量夹角、线性插值、坐标旋转、经纬度转换（`LatLonToMercator`、`MercatorToLatLon` 等）等功能函数。
- **[GeoLocation](#GeoLocation)**：地理位置类，用于表示纬度、经度、高度，并可将世界坐标位置（Location）转换为对应的地理坐标。
- **[CubicPolynomial](#CubicPolynomial)**：三次多项式类，可表示形式为 `a + b*x + c*x^2 + d*x^3` 的函数，用于道路曲线拟合与计算。
- **[BoundingBox](#BoundingBox)**：有向边界框类，由中心位置、尺度和旋转构成，提供判断点是否在框内、计算八个顶点坐标（局部或世界空间）等方法。
- **[Mesh](#Mesh)**：网格容器类及其生成器。`Mesh` 用于存储顶点、法线、纹理坐标、索引和材质信息，可导出为 OBJ/PLY 等格式；
- **[Simplification](#Simplification)**：网格简化类，根据指定简化率对给定网格进行简化操作（使用第三方简化库）。
- **[RTree](#RTree)**:是一种用于空间索引的树形结构,提供检索方法用于点云和线段云的快速空间查询（最近邻、相交判定等），主要使用在物体的碰撞使用。
<span id="其他模块的引用"></span>
## 其他模块的引用

- **HUTB 客户端（`client`）模块：**  该模块大量使用几何类型来描述场景中对象的位置和姿态。例如，`carla::client::World::SpawnActor` 方法的接口中使用了 `geom::Transform` 作为参数[carla.org](https://carla.org/Doxygen/html/dd/d5b/World_8h_source.html#:~:text=111 SharedPtr)；`carla::client::TrafficLight` 类中使用 `geom::BoundingBox` 表示灯组的遮挡盒（如 `GetLightBoxes` 返回多个 BoundingBox）[carla.org](https://carla.org/Doxygen/html/df/def/classcarla_1_1client_1_1TrafficLight.html#:~:text=std%3A%3Avector,const)，以及继承自 `Actor` 的 `AddAngularImpulse(const Vector3D&)` 方法使用了三维向量[carla.org](https://carla.org/Doxygen/html/df/def/classcarla_1_1client_1_1TrafficLight.html#:~:text=const geom%3A%3ABoundingBox  %26 33,const)。这些用法说明客户端模块在创建和控制 actor（车辆、交通灯等）时依赖 `geom` 提供的几何表示与变换工具。

- **HUTB 路网（`road`）模块：** 路网模块对道路、交叉口等结构建模时使用了边界框和几何计算。比如 `carla::road::Map` 在计算路口冲突、获取交叉口的 BoundingBox 列表时会用到 `geom::BoundingBox`[carla.org](https://carla.org/Doxygen/html/d8/d68/classcarla_1_1geom_1_1BoundingBox.html#:~:text=Referenced by carla%3A%3Anav%3A%3ANavigation%3A%3AAddOrUpdateVehicle,operator)；构建道路网格时也会涉及多边形与向量运算。此外，`MapBuilder::SDFToMesh` 等功能也参考了 BoundingBox 的顶点计算[carla.org](https://carla.org/Doxygen/html/d8/d68/classcarla_1_1geom_1_1BoundingBox.html#:~:text=Referenced by carla%3A%3Anav%3A%3ANavigation%3A%3AAddOrUpdateVehicle,operator)。

- **HUTB 导航（`nav`）模块：** 该模块（包括 `Navigation` 和 `WalkerManager`）使用 `geom::Vector3D` 和 `geom::BoundingBox` 来管理交通参与者的路径和位置。例如 `Navigation::AddOrUpdateVehicle`、`Navigation::AddWalker` 等方法中频繁操作三维位置向量[carla.org](https://carla.org/Doxygen/html/d9/dfe/classcarla_1_1geom_1_1Vector3D.html#:~:text=Referenced by carla%3A%3Aroad%3A%3AMap%3A%3AAddElementToRtree,carla%3A%3Arss%3A%3ARssCheck%3A%3AAppendRoutingTarget)；同时，导航中的安全检查也会用到边界盒计算（如附近路段障碍物的边界框）。

- **HUTB RSS 模块：** 路网安全（RSS）检查模块使用三维向量来存储车辆位置，并计算规划路线目标，比如 `RssCheck::AppendRoutingTarget` 中会使用 `geom::Vector3D`[carla.org](https://carla.org/Doxygen/html/d9/dfe/classcarla_1_1geom_1_1Vector3D.html#:~:text=Referenced by carla%3A%3Aroad%3A%3AMap%3A%3AAddElementToRtree,carla%3A%3Arss%3A%3ARssCheck%3A%3AAppendRoutingTarget)。

- **HUTB 交通管理（Traffic Manager）模块：** 交通管理使用 `geom` 中的几何类型进行轨迹规划和位置更新。在多个阶段（如 `MotionPlanStage::SafeAfterJunction`、`LocalizationStage::Update`）中可见对 `Vector3D` 的调用[carla.org](https://carla.org/Doxygen/html/d9/dfe/classcarla_1_1geom_1_1Vector3D.html#:~:text=Referenced by Length,and)，用于计算车辆运动和加速度等。

- **其他依赖：** 还有一些功能模块也使用了 `geom`。例如，`client::TrafficLight::GetStopWaypoints()` 返回的是与交通灯相关的停车点（Waypoints），这些 Waypoint 本身也封装了 `Location/Transform` 等；`client::TrafficLight` 的触发体积（TriggerVolume）也是 `geom::BoundingBox` 类型[carla.org](https://carla.org/Doxygen/html/df/def/classcarla_1_1client_1_1TrafficLight.html#:~:text=const geom%3A%3ABoundingBox  %26 33,const)。此外，路网构建和传感器处理等环节也可能间接使用几何变换方法。

下面是其主要类的代码说明文档。

<span id="Math"></span>

# [Math](#Math)

## 概述
`carla::geom::Math` 提供了一系列数学常量与常用数学运算函数，主要用于三维/二维向量运算、角度转换、距离计算、线性插值等。

---

## 模板常量

### **<font color="#7fb800">Pi</font>**
```cpp
template <typename T>
static constexpr T Pi();
```
- **模板参数**  
  - <font color="#f8805a">T</font>：必须为浮点类型  
- **返回值**：π（3.141592653589793…），类型为 <font color="#f8805a">T</font>

### **<font color="#7fb800">Pi2</font>**
```cpp
template <typename T>
static constexpr T Pi2();
```
- **模板参数**  
  - <font color="#f8805a">T</font>：必须为浮点类型  
- **返回值**：2π，即 2 × **<font color="#7fb800">Pi</font>**，类型为 <font color="#f8805a">T</font>

---

## 角度转换

### **<font color="#7fb800">ToDegrees</font>**
```cpp
template <typename T>
static constexpr T ToDegrees(T rad);
```
- **参数**  
  - <font color="#f8805a">rad</font>：弧度值  
- **返回值**：度数，等于 <font color="#f8805a">rad</font> × (180 / π)

### **<font color="#7fb800">ToRadians</font>**
```cpp
template <typename T>
static constexpr T ToRadians(T deg);
```
- **参数**  
  - <font color="#f8805a">deg</font>：度数值  
- **返回值**：弧度，等于 <font color="#f8805a">deg</font> × (π / 180)

---

## 范围与平方

### **<font color="#7fb800">Clamp</font>**
```cpp
template <typename T>
static T Clamp(T a, T min = T(0), T max = T(1));
```
- **参数**  
  - <font color="#f8805a">a</font>：待限制的值  
  - <font color="#f8805a">min</font>：下界，默认 0  
  - <font color="#f8805a">max</font>：上界，默认 1  
- **返回值**：将 <font color="#f8805a">a</font> 限制在 [<font color="#f8805a">min</font>,<font color="#f8805a">max</font>] 范围内的结果

### **<font color="#7fb800">Square</font>**
```cpp
template <typename T>
static T Square(const T &a);
```
- **参数**  
  - <font color="#f8805a">a</font>：输入值  
- **返回值**：<font color="#f8805a">a</font>²

---

## 向量运算

### **<font color="#7fb800">Cross</font>**
```cpp
static auto Cross(const Vector3D &a, const Vector3D &b);
```
- **参数**  
  - <font color="#f8805a">a</font>, <font color="#f8805a">b</font>：三维向量  
- **返回值**：叉积向量

设\(a=[x_1,y_1,z_1],b=[x_2,y_2,z_2]\)那么它们的叉积\(a\times b\)为：
$$
a\times b=\begin{pmatrix}y_1z_2-z_1y_2\\z_1x_2-x_1z_2\\x_1y_2-y_1x_2\end{pmatrix}
$$

### **<font color="#7fb800">Dot</font>**

```cpp
static auto Dot(const Vector3D &a, const Vector3D &b);
```
- **参数**  
  - <font color="#f8805a">a</font>, <font color="#f8805a">b</font>：三维向量  
- **返回值**：点积（标量）

向量的点积计算公式为:
$$
a\cdot b=\sum_i^n a_ib_i
$$


其中\(n\)是向量的维度。

### **<font color="#7fb800">Dot2D</font>**

```cpp
static auto Dot2D(const Vector3D &a, const Vector3D &b);
```
- **参数**  
  - <font color="#f8805a">a</font>, <font color="#f8805a">b</font>：仅取 x,y 分量  
- **返回值**：二维点积

---

## 距离计算

### **<font color="#7fb800">DistanceSquared</font>**
```cpp
static auto DistanceSquared(const Vector3D &a, const Vector3D &b);
```
- **参数**  
  - <font color="#f8805a">a</font>：起点向量  
  - <font color="#f8805a">b</font>：终点向量  
- **返回值**：两点间三维距离的平方

### **<font color="#7fb800">DistanceSquared2D</font>**
```cpp
static auto DistanceSquared2D(const Vector3D &a, const Vector3D &b);
```
- **参数**  
  - <font color="#f8805a">a</font>：起点向量  
  - <font color="#f8805a">b</font>：终点向量  
- **返回值**：两点间二维距离的平方

### **<font color="#7fb800">Distance</font>**
```cpp
static auto Distance(const Vector3D &a, const Vector3D &b);
```
- **参数**  
  - <font color="#f8805a">a</font>：起点向量  
  - <font color="#f8805a">b</font>：终点向量  
- **返回值**：两点间三维距离

### **<font color="#7fb800">Distance2D</font>**
```cpp
static auto Distance2D(const Vector3D &a, const Vector3D &b);
```
- **参数**  
  - <font color="#f8805a">a</font>：起点向量  
  - <font color="#f8805a">b</font>：终点向量  
- **返回值**：两点间二维距离

---

## 插值

### **<font color="#7fb800">LinearLerp</font>**
```cpp
static float LinearLerp(float a, float b, float f);
```
- **参数**  
  - <font color="#f8805a">a</font>, <font color="#f8805a">b</font>：端点值  
  - <font color="#f8805a">f</font>：插值因子 (0…1)  
- **返回值**：线性插值结果

---

## 复杂几何运算

### **<font color="#7fb800">GetVectorAngle</font>**
```cpp
static double GetVectorAngle(const Vector3D &a, const Vector3D &b);
```
- **参数**  
  - <font color="#f8805a">a</font>, <font color="#f8805a">b</font>：三维向量  
- **返回值**：向量 <font color="#f8805a">a</font> 与 <font color="#f8805a">b</font> 之间的夹角（弧度）

### **<font color="#7fb800">DistanceSegmentToPoint</font>**
```cpp
static std::pair<float, float> DistanceSegmentToPoint(
    const Vector3D &p,
    const Vector3D &v,
    const Vector3D &w);
```
- **参数**  
  - <font color="#f8805a">p</font>：要计算距离的点  
  - <font color="#f8805a">v</font>：线段起点  
  - <font color="#f8805a">w</font>：线段终点  
- **返回值**：`(沿线段的弧长距离, 点到线段的欧氏距离)`

设：

- 点 \(p\)
- 线段起点 \(v\)
- 线段终点 \(w\)

线段向量为：\(\vec{d} = \vec{w} - \vec{v}\)
向量 \(\vec{vp} = \vec{p} - \vec{v}\)

**1. 计算投影参数 t**

该参数t 表示点 p 在 \(\vec{d}\)上的投影比例位置：

$$
t = \frac{(\vec{p} - \vec{v}) \cdot (\vec{w} - \vec{v})}{\|\vec{w} - \vec{v}\|^2}
$$

然后将 t限制在 [0,1] 范围内（因为只在线段上）：

```cpp
t = Clamp(t, 0.0f, 1.0f);
```

**2. 计算投影点坐标**

$$
\vec{proj} = \vec{v} + t \cdot (\vec{w} - \vec{v})
$$

**3. 返回结果**

- 第一项：投影点到线段起点的距离（线段弧长）

  $$
  \text{distance\_along\_segment} = t \cdot \|\vec{w} - \vec{v}\|
  $$

- 第二项：点 p 到投影点的欧氏距离

  $$
  \text{distance\_to\_segment} = \|\vec{p} - \vec{proj}\|
  $$

### **<font color="#7fb800">DistanceArcToPoint</font>**

```cpp
static std::pair<float, float> DistanceArcToPoint(
    Vector3D p,
    Vector3D start_pos,
    float length,
    float heading,
    float curvature);
```
- **参数**  
  - <font color="#f8805a">p</font>：要计算距离的点  
  - <font color="#f8805a">start_pos</font>：圆弧起始位置  
  - <font color="#f8805a">length</font>：圆弧长度  
  - <font color="#f8805a">heading</font>：起始航向（弧度）  
  - <font color="#f8805a">curvature</font>：曲率  
- **返回值**：`(沿圆弧的弧长距离, 点到圆弧的最近距离)`

**1. 处理特殊情况**

若曲率为 0，圆弧退化为直线段，调用 `DistanceSegmentToPoint` 即可：
```cpp
if (std::abs(curvature) < 1e-6) return DistanceSegmentToPoint(...);
```

**2. 圆心计算**

设圆弧是逆时针方向（曲率为正），那么：

- 曲率半径 \(R = \frac{1}{|curvature|}\)
- 圆心在起点的垂直方向上：

$$
center = start\_pos + R \cdot \begin{bmatrix} -\sin(heading) \\ \cos(heading) \end{bmatrix}
\quad \text{（当 curvature > 0）}
$$

**3. 将点 p映射到极坐标下**

- 向量 \(\vec{v} = p - center\)
- 距离为 \(r = \|\vec{v}\|\)
- 角度 \(\theta_p = \arctan2(p_y - c_y, p_x - c_x)\)

**4. 计算圆弧起始角度 \(\theta_0\)**

由于起始点位于弧上的起点，其角度为：

$$
\theta_0 = \arctan2(start\_pos_y - c_y, start\_pos_x - c_x)
$$

**5. 弧长范围映射（0 到 total_arc_angle）**

总的圆心角：

$$
\Delta \theta = \frac{length}{R}
$$

点到起点的圆心角（根据方向判断）：

$$
\Delta \theta_p = \text{WrapAngle}(\theta_p - \theta_0)
$$

- 如果 curvature > 0，逆时针方向；否则顺时针。

投影点是否在圆弧范围内需判断 \(0 \leq \Delta \theta_p \leq \Delta \theta\)

**6. 计算投影点坐标**
$$
proj = center + R \cdot \begin{bmatrix} \cos(\theta_p) \\ \sin(\theta_p) \end{bmatrix}
$$

**7. 计算结果**

- 沿弧长距离：

  $$
  s = R \cdot \Delta \theta_p
  $$

- 欧氏距离：

  $$
  d = \|\vec{p} - \vec{proj}\|
  $$

若超出圆弧范围，则与端点距离更近，返回：

```cpp
Distance(p, start_pos) 或 Distance(p, arc_end)
```

---

### **<font color="#7fb800">RotatePointOnOrigin2D</font>**

```cpp
static Vector3D RotatePointOnOrigin2D(Vector3D p, float angle);
```
- **参数**  
  - <font color="#f8805a">p</font>：二维点  
  - <font color="#f8805a">angle</font>：旋转角度（弧度）  
- **返回值**：绕原点旋转后的二维点

### **<font color="#7fb800">GetForwardVector</font>**
```cpp
static Vector3D GetForwardVector(const Rotation &rotation);
```
- **参数**  
  - <font color="#f8805a">rotation</font>：旋转信息  
- **返回值**：前向单位向量

### **<font color="#7fb800">GetRightVector</font>**
```cpp
static Vector3D GetRightVector(const Rotation &rotation);
```
- **参数**  
  - <font color="#f8805a">rotation</font>：旋转信息  
- **返回值**：右向单位向量

### **<font color="#7fb800">GetUpVector</font>**
```cpp
static Vector3D GetUpVector(const Rotation &rotation);
```
- **参数**  
  - <font color="#f8805a">rotation</font>：旋转信息  
- **返回值**：上向单位向量

---

## 范围生成

### **<font color="#7fb800">GenerateRange</font>**
```cpp
static std::vector<int> GenerateRange(int a, int b);
```
- **参数**  
  - <font color="#f8805a">a</font>：起始整数  
  - <font color="#f8805a">b</font>：结束整数  
- **返回值**：包含从 <font color="#f8805a">a</font> 到 <font color="#f8805a">b</font>（含）的所有整数的向量

<span id="Vector3D/Vector2D/Vector3DInt"></span>

# [Vector3D/Vector2D/Vector3DInt](#Vector3D/Vector2D/Vector3DInt)

## 概述
它们用于表示向量，包含坐标分量与丰富的向量运算接口，也支持与 UE4 的类型互转及 MsgPack 序列化。

---

## Vector2D

### **<font color="#7fb800">SquaredLength</font>**
- **原型**：`float SquaredLength() const;`  
- **说明**：返回向量长度的平方：$$x^2 + y^2$$  
- **示例**：  
  ```cpp
  Vector2D v(3.0f,4.0f);
  float sq = v.SquaredLength(); // sq == 25
  ```

### **<font color="#7fb800">Length</font>**
- **原型**：`float Length() const;`  
- **说明**：返回向量长度：$$\sqrt{x^2 + y^2}$$  
- **示例**：  
  ```cpp
  Vector2D v(3.0f,4.0f);
  float len = v.Length(); // len == 5
  ```

### **<font color="#7fb800">MakeUnitVector</font>**
- **原型**：`Vector2D MakeUnitVector() const;`  
- **说明**：返回归一化后的单位向量：$$\frac{1}{\|v\|}(x,y)$$  
- **示例**：  
  ```cpp
  Vector2D v(0.0f,5.0f);
  Vector2D u = v.MakeUnitVector(); // u ≈ (0,1)
  ```

---

## Vector3D

### **<font color="#7fb800">SquaredLength</font>**
- **原型**：`float SquaredLength() const;`  
- **说明**：返回：$$x^2 + y^2 + z^2$$  
- **示例**：  
  
  ```cpp
  Vector3D  v3(1.0f,2.0f,2.0f);
  float sq3 = v3.SquaredLength(); // sq3 == 9
  ```

### **<font color="#7fb800">Length</font>**
- **原型**：`float Length() const;`  
- **说明**：返回：$$\sqrt{x^2 + y^2 + z^2}$$  
- **示例**：  
  ```cpp
  float len3 = v3.Length(); // len3 == 3
  ```

### **<font color="#7fb800">SquaredLength2D</font>** / **<font color="#7fb800">Length2D</font>**
- **原型**：  
  
  - `float SquaredLength2D() const;` 返回 $$x^2 + y^2$$  
  - `float Length2D() const;` 返回 $$\sqrt{x^2 + y^2}$$  
- **示例**：  
  ```cpp
  Vector3D vxy(3.0f,4.0f,7.0f);
  float sq2d = vxy.SquaredLength2D(); // 25
  float len2d = >vxy.Length2D();        // 5
  ```

### **<font color="#7fb800">Abs</font>**
- **原型**：`Vector3D Abs() const;`  
- **说明**：返回 $$(|x|,|y|,|z|)$$  
- **示例**：  
  ```cpp
  Vector3D vneg(-1.0f,-2.0f,3.0f);
  Vector3D apos = vneg.Abs(); // (1,2,3)
  ```

### **<font color="#7fb800">MakeUnitVector</font>**
- **原型**：`Vector3D MakeUnitVector() const;`  
- **说明**：返回标准归一化单位向量  
- **示例**：  
  ```cpp
  Vector3D vnorm(0.0f,0.0f,5.0f);
  Vector3D unorm = vnorm.MakeUnitVector(); // (0,0,1)
  ```

### **<font color="#7fb800">MakeSafeUnitVector</font>**
- **原型**：`Vector3D MakeSafeUnitVector(float epsilon) const;`  
- **说明**：长度小于 $$\epsilon$$ 时返回原向量，否则归一化  
- **示例**：  
  ```cpp
  Vector3D vsafe(1e-4f,0,0);
  Vector3D svec = vsafe.MakeSafeUnitVector(1e-3f); // unchanged
  ```

---

## Vector3DInt

### **<font color="#7fb800">SquaredLength</font>**
- **原型**：`int64_t SquaredLength() const;`  
- **说明**：返回整数平方和：$$x^2 + y^2 + z^2$$  
- **示例**：  
  ```cpp
  Vector3DInt vi(2,3,6);
  int64_t sqint = vi.SquaredLength(); // 49
  ```

### **<font color="#7fb800">Length</font>**
- **原型**：`double Length() const;`  
- **说明**：返回：$$\sqrt{x^2 + y^2 + z^2}$$  
- **示例**：  
  ```cpp
  double lint = vi.Length(); // 7.0
  ```

## UE4 互转（仅在 UE4 模式开启时）

```cpp
Vector3D ToMeters() const;
Vector3D ToCentimeters() const;
FVector ToFVector() const;
```
- **示例**：  
  ```cpp
  Vector3D v(100,200,300);
  FVector f = v.ToFVector();     // f = (100,200,300)
  Vector3D m = v.ToMeters();     // m = (1,2,3)
  Vector3D cm = m.ToCentimeters(); // cm = (100,200,300)
  ```

---

## MsgPack 序列化

```cpp
template <typename Packer>
void msgpack_pack(Packer& pk) const;

void msgpack_unpack(clmdep_msgpack::object const& o);

template <typename MSGPACK_OBJECT>
void msgpack_object(MSGPACK_OBJECT* o, clmdep_msgpack::zone& sneaky_variable_that_shadows_z) const;
```
- **说明**：使用内置宏 `make_define_array(x,y,z)` 实现序列化/反序列化。  
- **示例**：  
  ```cpp
  // pack
  clmdep_msgpack::sbuffer sbuf;
  msgpack::pack(sbuf, Vector3D(1,2,3));
  // unpack
  auto obj = msgpack::unpack(sbuf.data(), sbuf.size()).get();
  Vector3D v;
  v.msgpack_unpack(obj);
  ```

---

<span id="Mesh"></span>

# [Mesh](#Mesh)

## 概述
`carla::geom::Mesh` 类是一个网格数据容器，提供验证、构建、导出以及与 UE4 类型互转的功能。支持顶点、法线、索引、UV 和材质分组的管理。

---

## 类型别名

- **vertex_type**：顶点类型，`Vector3D`  
- **normal_type**：法线类型，`Vector3D`  
- **index_type**：索引类型，`size_t`  
- **uv_type**：纹理坐标类型，`Vector2D`  
- **material_type**：材质类型，`MeshMaterial`

---

## 构造函数

### **Mesh(...)**
```cpp
Mesh(
  const std::vector<vertex_type> &vertices = {},
  const std::vector<normal_type> &normals = {},
  const std::vector<index_type> &indexes = {},
  const std::vector<uv_type> &uvs = {}
);
```
- **说明**：可选传入初始顶点、法线、索引和 UV 列表。  
- **示例**：
  ```cpp
  std::vector<Vector3D> verts = { {0,0,0}, {1,0,0}, {0,1,0} };
  Mesh mesh(verts);
  ```

---

## 验证方法

### **IsValid**
```cpp
bool IsValid() const;
```
- **说明**：  
  1. 顶点列表非空；  
  2. 索引数若非零必须为 3 的倍数；  
  3. 所有开启的材质必须正确关闭。  
- **示例**：
  ```cpp
  if (!mesh.IsValid()) {
    std::cerr << "Invalid mesh!" << std::endl;
  }
  ```

---

## 网格构建方法

### **AddTriangleStrip**
```cpp
void AddTriangleStrip(const std::vector<vertex_type> &vertices);
```
- **说明**：按三角带（Triangle Strip）方式添加顶点，依次生成面。  
- **示例**：
  ```cpp
  mesh.AddTriangleStrip({{0,0,0},{1,0,0},{1,1,0},{0,1,0}});
  ```

### **AddTriangleFan**
```cpp
void AddTriangleFan(const std::vector<vertex_type> &vertices);
```
- **说明**：按三角扇（Triangle Fan）方式添加顶点，第一个顶点为中心。  
- **示例**：
  ```cpp
  mesh.AddTriangleFan({{0,0,0},{1,0,0},{1,1,0},{0,1,0}});
  ```

### **AddVertex / AddVertices**
```cpp
void AddVertex(vertex_type vertex);
void AddVertices(const std::vector<vertex_type> &vertices);
```
- **说明**：将顶点附加到内部列表。  
- **示例**：
  ```cpp
  mesh.AddVertex({0,0,1});
  mesh.AddVertices({{1,0,1},{0,1,1}});
  ```

### **AddNormal**
```cpp
void AddNormal(normal_type normal);
```
- **说明**：将法线附加到内部列表。  

### **AddIndex**
```cpp
void AddIndex(index_type index);
```
- **说明**：将单个面索引附加到内部列表。  

### **AddUV / AddUVs**
```cpp
void AddUV(uv_type uv);
void AddUVs(const std::vector<uv_type> &uvs);
```
- **说明**：添加纹理坐标 (u,v)。  

### **AddMaterial / EndMaterial**
```cpp
void AddMaterial(const std::string &material_name);
void EndMaterial();
```
- **说明**：开始／结束一个材质区间，记录当前索引范围。  
- **示例**：
  ```cpp
  mesh.AddMaterial("matA");
  // ... 添加三角面 ...
  mesh.EndMaterial();
  ```

---

## 导出方法

### **GenerateOBJ**
```cpp
std::string GenerateOBJ() const;
```
- **说明**：导出为标准 OBJ 格式：  
  - 顶点行：`v x y z`  
  - UV 行：`vt u v`  
  - 法线行：`vn x y z`  
  - 面行：`f i j k`  

### **GenerateOBJForRecast**
```cpp
std::string GenerateOBJForRecast() const;
```
- **说明**：为 Recast 库导出 OBJ，交换 y/z 并反转面顶点顺序。

### **GeneratePLY**
```cpp
std::string GeneratePLY() const;
```
- **说明**：导出为 PLY 格式（部分实现）。

---

## 访问方法

### **GetVertices / GetVerticesNum**
```cpp
const std::vector<vertex_type> &GetVertices() const;
size_t GetVerticesNum() const;
```

### **GetNormals**
```cpp
const std::vector<normal_type> &GetNormals() const;
```

### **GetIndexes / GetIndexesNum**
```cpp
const std::vector<index_type> &GetIndexes() const;
size_t GetIndexesNum() const;
```

### **GetUVs**
```cpp
const std::vector<uv_type> &GetUVs() const;
```

### **GetMaterials**
```cpp
const std::vector<material_type> &GetMaterials() const;
```

### **GetLastVertexIndex**
```cpp
size_t GetLastVertexIndex() const;
```
- **说明**：返回当前顶点总数。

---

## 合并网格

### **ConcatMesh**
```cpp
Mesh& ConcatMesh(const Mesh &rhs, int num_vertices_to_link);
```
- **说明**：将 `rhs` 网格合并到当前网格，并在相交处生成桥接三角面。  

### **operator+= / operator+**
```cpp
Mesh& operator+=(const Mesh &rhs);
friend Mesh operator+(const Mesh &lhs, const Mesh &rhs);
```
- **说明**：无桥接直接拼接顶点、法线、索引、UV 和材质区间。

---

## UE4 类型转换

### **operator FProceduralCustomMesh() const**
```cpp
operator FProceduralCustomMesh() const;
```
- **说明**：  
  - 顶点从米转换到厘米；  
  - 法线重新计算：  
$$
\mathbf{N} = \mathrm{normalize}\bigl((\mathbf{V}_1-\mathbf{V}_0)\times(\mathbf{V}_2-\mathbf{V}_0)\bigr)
$$
  - UV 坐标保留 (x,y)。  
- **示例**：
  ```cpp
  FProceduralCustomMesh ue_mesh = mesh;
  ```

---

<span id="Simplification"></span>

# [Simplification](#Simplification)

## 概述
`carla::geom::Simplification` 类用于对 `carla::geom::Mesh` 网格模型执行简化操作，通过指定简化比率，将三角形数减少到原始数量的若干百分比，从而降低模型复杂度。

---

## 构造函数

### **<font color="#7fb800">Simplification()</font>**
```cpp
Simplification() = default;
```
- **说明**：默认构造，无需初始化即可使用  
- **示例**：
  ```cpp
  carla::geom::Simplification sim; // 使用默认简化率（未指定）
  ```

### **<font color="#7fb800">Simplification(float simplificationrate)</font>**
```cpp
Simplification(float simplificationrate);
```
- **参数**  
  - **<font color="#f8805a">simplificationrate</font>**：目标简化比率（0.0–1.0），如 0.5 表示保留 50% 三角形  
- **示例**：
  ```cpp
  carla::geom::Simplification sim(0.25f); // 保留 25% 的三角形
  ```

---

## 公开数据成员

- **<font color="#f8805a">simplification_percentage</font>**  
  
  - 存储简化比率（0–1 之间的浮点数）  
  - **示例**：
    
    ```cpp
    float rate = sim.simplification_percentage; // 获取当前简化比率
    ```

---

## 方法

### **<font color="#7fb800">Simplificate</font>**
```cpp
void Simplificate(const std::unique_ptr<geom::Mesh>& pmesh);
```
- **说明**：对传入的 `Mesh` 对象执行网格简化，简化后会修改其顶点与索引数据。  
- **参数**  
  
  - **<font color="#f8805a">pmesh</font>**：指向待简化网格的智能指针引用  
- **示例**：
  ```cpp
  #include "carla/geom/Simplification.h"
  #include "carla/geom/Mesh.h"
  
  // 假设已创建或加载了一个 Mesh 对象
  std::unique_ptr<carla::geom::Mesh> mesh = LoadYourMesh();
  carla::geom::Simplification sim(0.5f);    // 保留 50% 三角形
  sim.Simplificate(mesh);                   // 执行简化
  // 之后 mesh->GetVertices() 和 mesh->GetIndexes() 已被更新为简化后的数据
  ```

---

<span id="RTree"></span>

# [RTree](#RTree)

## 简介
R-树（R-Tree）是一种用于空间索引的树形结构，通过将空间中相近对象聚合成最小外接矩形（MBR）构建索引，广泛应用于点云、线段云等三维几何对象的快速邻近查询与碰撞检测。

RTree包含两个模板类：
- `PointCloudRtree<T>`：支持对点云的插入、k-NN 查询、带过滤器查询；
- `SegmentCloudRtree<T>`：支持对线段云的插入、k-NN 查询、交集查询。

---

## 欧几里得距离公式

对任意两个 *n* 维点 **p** = (*p*<sub>1</sub>, *p*<sub>2</sub>, …, *p*<sub>n</sub>) 和 **q** = (*q*<sub>1</sub>, *q*<sub>2</sub>, …, *q*<sub>n</sub>)，欧几里得距离定义如下：

$$
d(\mathbf{p}, \mathbf{q}) = \sqrt{ \sum_{i=1}^n (p_i - q_i)^2 }
$$

---

## 类定义：PointCloudRtree

```cpp
template <typename T, size_t Dimension = 3>
class PointCloudRtree;
```

- `T`：元素类型；
- `Dimension`：空间维度，默认值为 `3`。

### 成员类型

```cpp
using BPoint = boost::geometry::model::point<float, Dimension>;
using TreeElement = std::pair<BPoint, T>;
```

### 方法说明

#### InsertElement

```cpp
void InsertElement(const BPoint &point, const T &element);
void InsertElement(const TreeElement &element);
```

- 插入一个点或点-元素对到 R 树中。

#### InsertElements

```cpp
void InsertElements(const std::vector<TreeElement> &elements);
```

- 批量插入元素。

#### GetNearestNeighbours

```cpp
std::vector<TreeElement> GetNearestNeighbours(const BPoint &point, size_t number_neighbours = 1) const;
```

- 返回距离给定点最近的 *k* 个邻居（默认 *k*=1）。

#### GetNearestNeighboursWithFilter

```cpp
template <typename Filter>
std::vector<TreeElement> GetNearestNeighboursWithFilter(const BPoint &point, Filter filter, size_t number_neighbours = 1) const;
```

- 在返回最近邻的基础上，添加用户自定义过滤条件。

#### GetTreeSize

```cpp
size_t GetTreeSize() const;
```

- 返回当前树中包含的元素数量。

---

## 类定义：`SegmentCloudRtree`

```cpp
template <typename T, size_t Dimension = 3>
class SegmentCloudRtree;
```

### 成员类型

```cpp
using BPoint = boost::geometry::model::point<float, Dimension>;
using BSegment = boost::geometry::model::segment<BPoint>;
using TreeElement = std::pair<BSegment, std::pair<T, T>>;
```

### 方法说明

#### InsertElement

```cpp
void InsertElement(const BSegment &segment, const T &element_start, const T &element_end);
void InsertElement(const TreeElement &element);
```

- 插入一条线段以及其两端关联的数据。

#### InsertElements

```cpp
void InsertElements(const std::vector<TreeElement> &elements);
```

- 批量插入线段。

#### GetNearestNeighbours

```cpp
template <typename Geometry>
std::vector<TreeElement> GetNearestNeighbours(const Geometry &geometry, size_t number_neighbours = 1) const;
```

- 返回与几何体最邻近的线段。

#### GetNearestNeighboursWithFilter

```cpp
template <typename Geometry, typename Filter>
std::vector<TreeElement> GetNearestNeighboursWithFilter(const Geometry &geometry, Filter filter, size_t number_neighbours = 1) const;
```

- 返回最邻近的线段，且满足过滤条件。

#### GetIntersections

```cpp
template <typename Geometry>
std::vector<TreeElement> GetIntersections(const Geometry &geometry) const;
```

- 查询与几何体相交的线段集合。注意：Boost Geometry 暂不支持 3D 线段与线段精确交集判断，结果可能不完全准确。

#### GetTreeSize

```cpp
size_t GetTreeSize() const;
```

- 返回线段树的大小。

---

<span id="Location"></span>

# [Location](#Location)

## 概述
`carla::geom::Location` 类继承自 `Vector3D`，表示三维空间中的位置点，提供与 `Vector3DInt` 间的互转、距离计算、算术与比较运算符重载，以及与 UE4 `FVector` 类型的互转。

---
**主要成员属性**

| 属性名 | 类型     | 说明           | 默认值 |
| ------ | -------- | -------------- | ------ |
| `x`    | `double` | X 坐标（前向） | `0.0`  |
| `y`    | `double` | Y 坐标（右向） | `0.0`  |
| `z`    | `double` | Z 坐标（上向） | `0.0`  |

## 构造函数

### **<font color="#7fb800">Location()</font>**
- **原型**：`Location() = default;`  
- **说明**：默认构造，坐标初始化为 (0, 0, 0)。  
- **示例**：  
  ```cpp
  Location loc_default; // (0,0,0)
  ```

### **<font color="#7fb800">Location(float x, float y, float z)</font>**  
*(继承自 `Vector3D`)*  
- **说明**：使用基类 `Vector3D` 构造函数，初始化三维坐标。  
- **示例**：  
  ```cpp
  Location loc_xyz(1.0f, 2.0f, 3.0f); // (1,2,3)
  ```

### **<font color="#7fb800">Location(const Vector3D &rhs)</font>**
- **原型**：`Location(const Vector3D &rhs);`  
- **说明**：从 `Vector3D` 对象转换而来，拷贝坐标。  
- **示例**：  
  ```cpp
  Vector3D v(4.0f,5.0f,6.0f);
  Location loc_from_v(v); // (4,5,6)
  ```

### **<font color="#7fb800">Location(const Vector3DInt &rhs)</font>**
- **原型**：`Location(const Vector3DInt &rhs);`  
- **说明**：从整数坐标 `Vector3DInt` 转换而来，按比例（int→float）赋值。  
- **示例**：  
  ```cpp
  Vector3DInt vi(7,8,9);
  Location loc_from_vi(vi); // (7,8,9)
  ```

---

## 距离计算方法

### **<font color="#7fb800">DistanceSquared</font>**
- **原型**:  
  ```cpp
  auto DistanceSquared(const Location &loc) const;
  ```
- **说明**：返回当前对象到 `loc` 的三维距离平方，计算公式：  
  $$d^2 = (x - x')^2 + (y - y')^2 + (z - z')^2$$  
- **示例**：  
  ```cpp
  Location a(0,0,0), b(1,2,2);
  auto d2 = a.DistanceSquared(b); // d2 == 9
  ```

### **<font color="#7fb800">Distance</font>**
- **原型**:  
  ```cpp
  auto Distance(const Location &loc) const;
  ```
- **说明**：返回当前对象到 `loc` 的欧氏距离，等于 $$\sqrt{DistanceSquared(loc)}$$。  
- **示例**：  
  ```cpp
  auto d = a.Distance(b); // d == 3
  ```

---

## 算术运算符

### **<font color="#7fb800">operator+=</font>**
- **原型**:  
  ```cpp
  Location &operator+=(const Location &rhs);
  ```
- **说明**：将 `rhs` 坐标加到当前对象。  
- **示例**:  
  ```cpp
  Location p1(1,1,1),p2(2,3,4);
  p1+= p2; // p1 = (3,4,5)
  ```

### **<font color="#7fb800">operator+</font>**
- **原型**:  
  ```cpp
  friend Location operator+(Location lhs, const Location &rhs);
  ```
- **说明**：返回两坐标相加的新 `Location`。  
- **示例**:  
  ```cpp
  auto sum = p1 + p2; // sum = (3,4,5)
  ```

### **<font color="#7fb800">operator-=</font>** / **<font color="#7fb800">operator-</font>**
- **原型**:  
  ```cpp
  Location &operator-=(const Location &rhs);
  friend Location operator-(Location lhs, const Location &rhs);
  ```
- **说明**：坐标差运算。  
- **示例**:  
  ```cpp
  Location diff = p2 - p1; // ( -1, -2, -3 )
  ```

---

## 比较运算符

### **<font color="#7fb800">operator==</font>** / **<font color="#7fb800">operator!=</font>**
- **原型**:  
  ```cpp
  bool operator==(const Location &rhs) const;
  bool operator!=(const Location &rhs) const;
  ```
- **说明**：逐分量比较相等或不等。  
- **示例**:  
  ```cpp
  bool eq= ( p1 ==p2 );
  bool ne = ( p1!= p2 );
  ```

---

## UE4 类型互转 (仅在 `LIBCARLA_INCLUDED_FROM_UE4` 定义时)

### **<font color="#7fb800">Location(const FVector &vector)</font>**
- **说明**：从 UE4 `FVector`（厘米）转换到米坐标。  
- **示例**:  
  ```cpp
  FVector fv{100,200,300};
  Location loc_ue(fv); // (1,2,3)
  ```

### **<font color="#7fb800">operator FVector()</font>**
- **说明**：将 `Location`（米）转换到 UE4 `FVector`（厘米）。  
- **示例**:  
  ```cpp
  FVector fv2= loc_xyz; // (100,200,300)
  ```

<span id="Rotation"></span>

# [Rotation](#Rotation)

## 概述
`carla::geom::Rotation` 用于表示三维空间中的旋转状态，包含俯仰（pitch）、偏航（yaw）、翻滚（roll）三个角度。提供方向向量计算、向量旋转/逆旋转，以及与 UE4 `FRotator` 的互转。

---

## 公开数据成员

- **<font color="#f8805a">pitch</font>**：绕 X 轴的旋转角度，默认 0.0f  
- **<font color="#f8805a">yaw</font>**：绕 Y 轴的旋转角度，默认 0.0f  
- **<font color="#f8805a">roll</font>**：绕 Z 轴的旋转角度，默认 0.0f  

---

## 构造函数

### **<font color="#7fb800">Rotation()</font>**  
- **原型**：`Rotation() = default;`  
- **说明**：默认构造，三角度均为 0。  
- **示例**：  
  ```cpp
  Rotation r0; // pitch=0,yaw=0,roll=0
  ```

### **<font color="#7fb800">Rotation(float p, float y, float r)</font>**  
- **原型**:  
  ```cpp
  Rotation(float p, float y, float r);
  ```
- **参数**  
  - **<font color="#f8805a">p</font>**：俯仰角（pitch）  
  - **<font color="#f8805a">y</font>**：偏航角（yaw）  
  - **<font color="#f8805a">r</font>**：翻滚角（roll）  
- **示例**:  
  ```cpp
  Rotation r1(10.0f, 20.0f, 30.0f);
  ```

---

## 方向向量方法

### **<font color="#7fb800">GetForwardVector</font>**  
- **原型**:  
  ```cpp
  Vector3D GetForwardVector() const;
  ```
- **说明**：返回物体前方单位向量，计算公式：  
  $$\begin{aligned}
    x &= \cos(\mathrm{yaw})\cos(\mathrm{pitch}),\\
    y &= \sin(\mathrm{yaw})\cos(\mathrm{pitch}),\\
    z &= \sin(\mathrm{pitch}).
  \end{aligned}$$  
- **示例**:  
  ```cpp
  Rotation r(0,90,0);
  Vector3D fwd = r.GetForwardVector(); // ≈ (0,1,0)
  ```

### **<font color="#7fb800">GetRightVector</font>**  
- **原型**:  
  ```cpp
  Vector3D GetRightVector() const;
  ```
- **说明**：返回物体右侧单位向量，具体计算见 `Math::GetRightVector`。  
- **示例**:  
  ```cpp
  Vector3D right = r.GetRightVector();
  ```

### **<font color="#7fb800">GetUpVector</font>**  
- **原型**:  
  ```cpp
  Vector3D GetUpVector() const;
  ```
- **说明**：返回物体上方单位向量，具体计算见 `Math::GetUpVector`。  
- **示例**:  
  ```cpp
  Vector3D up= r.GetUpVector();
  ```

---

## 向量旋转方法

### **<font color="#7fb800">RotateVector</font>**  
- **原型**:  
  ```cpp
  void RotateVector(Vector3D &in_point) const;
  Vector3D RotateVector(const Vector3D &in_point) const;
  ```
- **说明**：  
  按顺序绕 Z（roll）、X（pitch）、Y（yaw）轴旋转：  
  $$\mathbf{v}' = R_{\text{yaw}} R_{\text{roll}} R_{\text{pitch}}\,\mathbf{v}.$$  
- **示例**:  
  ```cpp
  Vector3D pt(1,0,0);
  r.RotateVector(pt);           // 原地旋转
  auto pt2 = r.RotateVector(pt); // 返回旋转后拷贝
  ```

### **<font color="#7fb800">InverseRotateVector</font>**  
- **原型**:  
  ```cpp
  void InverseRotateVector(Vector3D &in_point) const;
  ```
- **说明**：按上述顺序的逆矩阵（转置）对向量做逆旋转。  
- **示例**:  
  ```cpp
  Vector3D p3 = pt2;
  r.InverseRotateVector(p3); // 恢复原向量 (1,0,0)
  ```

---

## 比较运算符

### **<font color="#7fb800">operator==</font>** / **<font color="#7fb800">operator!=</font>**  
- **原型**:  
  ```cpp
  bool operator==(const Rotation &rhs) const;
  bool operator!=(const Rotation &rhs) const;
  ```
- **说明**：逐分量比较相等或不等。  
- **示例**:  
  ```cpp
  bool same = (r == Rotation(10,20,30));
  ```

---

## UE4 类型互转（`LIBCARLA_INCLUDED_FROM_UE4`）

### **<font color="#7fb800">Rotation(const FRotator &rotator)</font>**  
- **说明**：从 `FRotator` 构造。  
- **示例**:  
  ```cpp
  FRotator fr{15,25,35};
  Rotation **<font color="#f8805a">rue</font>**(fr);
  ```

### **<font color="#7fb800">operator FRotator()</font>**  
- **说明**：转换为 UE4 `FRotator`。  
- **示例**:  
  ```cpp
  FRotator outFR = r;
  ```

<span id="Transform"></span>

# [Transform](#Transform)

## 概述
`carla::geom::Transform` 表示在三维空间中的位置与旋转变换，封装了 `Location` 和 `Rotation` 两部分。提供向量变换、点变换、逆变换及 4×4 矩阵生成，并支持与 UE4 `FTransform` 类型互转。

---

## 公开数据成员

- **<font color="#f8805a">location</font>**：类型 `Location`，表示平移分量  
- **<font color="#f8805a">rotation</font>**：类型 `Rotation`，表示旋转分量  

---

## 构造函数

### **<font color="#7fb800">Transform()</font>**
- **原型**：`Transform() = default;`  
- **说明**：默认构造，`location` 和 `rotation` 均为默认值。  
- **示例**：  
  ```cpp
  Transform t0; // location=(0,0,0)、rotation=(0,0,0)
  ```

### **<font color="#7fb800">Transform(const Location &in_location)</font>**
- **原型**：`Transform(const Location &in_location);`  
- **说明**：只设置平移，旋转保持默认。  
- **示例**：  
  ```cpp
  Location loc(1,2,3);
  Transform t1(loc); // rotation=(0,0,0)
  ```

### **<font color="#7fb800">Transform(const Location &in_location, const Rotation &in_rotation)</font>**
- **原型**：`Transform(const Location &in_location, const Rotation &in_rotation);`  
- **说明**：同时设置平移与旋转。  
- **示例**：  
  ```cpp
  Rotation r(10,20,30);
  Transform t2(loc,r);
  ```

---

## 方向向量方法

### **<font color="#7fb800">GetForwardVector</font>**
- **原型**:  
  ```cpp
  Vector3D GetForwardVector() const;
  ```
- **说明**：基于 `rotation` 计算单位“前向”向量。  
- **示例**:  
  ```cpp
  Vector3D fwd = t2.GetForwardVector();
  ```

### **<font color="#7fb800">GetRightVector</font>**
- **原型**:  
  ```cpp
  Vector3D GetRightVector() const;
  ```
- **说明**：基于 `rotation` 计算单位“右向”向量。  
- **示例**:  
  ```cpp
  Vector3D right = t2.GetRightVector();
  ```

### **<font color="#7fb800">GetUpVector</font>**
- **原型**:  
  ```cpp
  Vector3D GetUpVector() const;
  ```
- **说明**：基于 `rotation` 计算单位“上向”向量.  
- **示例**:  
  ```cpp
  Vector3D up = t2.GetUpVector();
  ```

---

## 点/向量变换方法

### **<font color="#7fb800">TransformPoint</font>**
- **原型**:  
  ```cpp
  void TransformPoint(Vector3D &in_point) const;
  ```
- **说明**：先绕原点旋转，再平移。  
- **示例**:  
  ```cpp
  Vector3D p(1,0,0);
  t2.TransformPoint(p);
  ```

### **<font color="#7fb800">TransformVector</font>**
- **原型**:  
  ```cpp
  void TransformVector(Vector3D &in_vector) const;
  ```
- **说明**：仅旋转向量，不平移。  
- **示例**:  
  ```cpp
  Vector3D v(0,1,0);
  t2.TransformVector(v);
  ```

### **<font color="#7fb800">InverseTransformPoint</font>**
- **原型**:  
  ```cpp
  void InverseTransformPoint(Vector3D &in_point) const;
  ```
- **说明**：先平移逆变换，再旋转逆变换。  
- **示例**:  
  ```cpp
  Vector3D p2 = p;
  t2.InverseTransformPoint(p2);
  ```

---

## 矩阵生成方法

### **<font color="#7fb800">GetMatrix</font>**
- **原型**:  
  ```cpp
  std::array<float,16> GetMatrix() const;
  ```
- **说明**：生成变换的 4×4 齐次矩阵，结合旋转与平移：  
  $$
  M = \begin{pmatrix}
    R & t\\
    0 & 1
  \end{pmatrix}
  $$
- **示例**:  
  ```cpp
  auto m = t2.GetMatrix();
  ```

### **<font color="#7fb800">GetInverseMatrix</font>**
- **原型**:  
  ```cpp
  std::array<float,16> GetInverseMatrix() const;
  ```
- **说明**：生成逆变换矩阵 \(M^{-1}\)。  
- **示例**:  
  ```cpp
  auto mi = t2.GetInverseMatrix();
  ```

---

## 比较运算符

### **<font color="#7fb800">operator==</font>** / **<font color="#7fb800">operator!=</font>**
- **原型**:  
  ```cpp
  bool operator==(const Transform &rhs) const;
  bool operator!=(const Transform &rhs) const;
  ```
- **说明**：位置与旋转均相等时才返回 `true`。  
- **示例**:  
  ```cpp
  bool eq = (t1 == t2);
  ```

---

## UE4 类型互转（`LIBCARLA_INCLUDED_FROM_UE4`）

### **<font color="#7fb800">Transform(const FTransform &transform)</font>**
- **说明**：从 UE4 `FTransform` 构造。  
- **示例**:  
  ```cpp
  FTransform ut;
  Transform tue(ut);
  ```

### **<font color="#7fb800">operator FTransform()</font>**
- **说明**：转换为 UE4 `FTransform`。  
- **示例**:  
  ```cpp
  FTransform ut2= t2;
  ```

<span id="CubicPolynomial"></span>

# [CubicPolynomial](#CubicPolynomial)

## 概述
`carla::geom::CubicPolynomial` 用于描述和操作三次多项式  
$$f(x)=a + b\,x + c\,x^2 + d\,x^3$$  
支持偏移量修正、求值、求切线、以及多项式加法和数乘。

---

## 构造函数

### **<font color="#7fb800">CubicPolynomial()</font>**
- **原型**：`CubicPolynomial() = default;`  
- **说明**：默认构造，所有系数和偏移量初始化为 0。  
- **示例**:  
  ```cpp
  CubicPolynomial p0; // a=b=c=d=s=0
  ```

### **<font color="#7fb800">CubicPolynomial(const value_type &a, const value_type &b, const value_type &c, const value_type &d)</font>**
- **原型**:  
  ```cpp
  CubicPolynomial(const value_type &a,
                  const value_type &b,
                  const value_type &c,
                  const value_type &d);
  ```
- **说明**：按系数 (*a*,*b*,*c*,*d*)构造，无偏移量。  
- **示例**:  
  
  ```cpp
  CubicPolynomial p1(1.0, 2.0, 3.0, 4.0);
  ```

### **<font color="#7fb800">CubicPolynomial(const value_type &a, const value_type &b, const value_type &c, const value_type &d, const value_type &s)</font>**
- **原型**:  
  ```cpp
  CubicPolynomial(const value_type &a,
                  const value_type &b,
                  const value_type &c,
                  const value_type &d,
                  const value_type &s);
  ```
- **说明**：按系数与偏移量 $s$ 构造，实际存储系数已做偏移校正：  
  $$\tilde a = a - b s + c s^2 - d s^3,\quad \tilde b = b -2c s +3d s^2,\quad \tilde c = c-3d s,\quad \tilde d = d$$  
- **示例**:  
  ```cpp
  CubicPolynomial p2(1,2,3,4,0.5);
  ```

---

## 访问与修改

### **<font color="#7fb800">GetA/B/C/D</font>**
- **原型**:  
  
  ```cpp
  value_type GetA() const;
  value_type GetB() const;
  value_type GetC() const;
  value_type GetD() const;
  ```
- **说明**：分别返回当前存储的系数 *a*,*b*,*c*,*d*。。  
- **示例**:  
  
  ```cpp
  auto a = p2.GetA();
  ```

### **<font color="#7fb800">GetS</font>**
- **原型**:  
  
  ```cpp
  value_type GetS() const;
  ```
- **说明**：返回偏移量 *s*。  
- **示例**:  
  
  ```cpp
  auto s = p2.GetS(); // 0.5
  ```

### **<font color="#7fb800">Set(a,b,c,d[,s])</font>**
- **原型**:  
  
  ```cpp
  void Set(const value_type &a,
           const value_type &b,
           const value_type &c,
           const value_type &d);
  void Set(const value_type &a,
           const value_type &b,
           const value_type &c,
           const value_type &d,
           const value_type &s);
  ```
- **说明**：重置系数（和可选偏移量），与构造逻辑一致。  
- **示例**:  
  ```cpp
  p2.Set(0,1,0,0);      // f(x)=x
  p2.Set(1,2,3,4, 0.2); // 带偏移修正
  ```

---

## 多项式运算

### **<font color="#7fb800">Evaluate</font>**
- **原型**:  
  ```cpp
  value_type Evaluate(const value_type &x) const;
  ```
- **说明**：计算 $$f(x)=\tilde a + \tilde b\,x + \tilde c\,x^2 + \tilde d\,x^3$$
- **示例**:  
  ```cpp
  auto y = p1.Evaluate(2.0); // 1+2*2+3*4+4*8
  ```

### **<font color="#7fb800">Tangent</font>**
- **原型**:  
  ```cpp
  value_type Tangent(const value_type &x) const;
  ```
- **说明**：计算导数 $$f'(x)=\tilde b + 2\tilde c\,x + 3\tilde d\,x^2$$。  
- **示例**:  
  ```cpp
  auto m = p1.Tangent(2.0); // 2 + 2*3*2 + 3*4*4
  ```

---

## 复合运算符

### **<font color="#7fb800">operator+=</font>**
- **原型**:  
  ```cpp
  CubicPolynomial &operator+=(const CubicPolynomial &rhs);
  ```
- **说明**：系数逐项相加。  
- **示例**:  
  ```cpp
  p1 += p2;
  ```

### **<font color="#7fb800">operator+</font>**
- **原型**:  
  ```cpp
  friend CubicPolynomial operator+(CubicPolynomial lhs, const CubicPolynomial &rhs);
  ```
- **说明**：返回相加结果。  
- **示例**:  
  ```cpp
  auto sum= p1 + p2;
  ```

### **<font color="#7fb800">operator*=</font>**
- **原型**:  
  ```cpp
  CubicPolynomial &operator*=(const value_type &rhs);
  ```
- **说明**：系数逐项乘以标量。  
- **示例**:  
  ```cpp
  p1 *= 2.0;
  ```

### **<font color="#7fb800">operator*</font>**
- **原型**:  
  ```cpp
  friend CubicPolynomial operator*(CubicPolynomial lhs, const value_type &rhs);
  friend CubicPolynomial operator*(const value_type &lhs, CubicPolynomial rhs);
  ```
- **说明**：返回乘标量结果，支持标量在左或右。  
- **示例**:  
  ```cpp
  auto scaled = 0.5 * p1;
  ```

---

<span id="BoundingBox"></span>

# [BoundingBox](#BoundingBox)

## 概述
`carla::geom::BoundingBox` 表示三维空间中的轴对齐或旋转后的边界盒，包含中心位置、半尺寸（extent）和旋转信息。提供判断点包含、获取局部/世界顶点数组，以及与 UE4 类型互转。

---

## 构造函数

### **<font color="#7fb800">BoundingBox()</font>**
- **原型**：`BoundingBox() = default;`  
- **说明**：默认构造，`location=(0,0,0)`，`extent=(0,0,0)`，`rotation=(0,0,0)`。  
- **示例**：  
  ```cpp
  BoundingBox bb0; // 默认空盒
  ```

- **带参构造**：  
  
  ```cpp
  explicit BoundingBox(const Location &in_location,
                       const Vector3D &in_extent,
                       const Rotation &in_rotation);
  ```
- **说明**：指定中心、半尺寸和旋转。  
- **示例**：  
  ```cpp
  Location loc(1,2,3);
  Vector3D ext(0.5f,0.5f,1.0f);
  Rotation rot(0,45,0);
  BoundingBox bb1(loc, ext, rot);
  ```

- **带参构造**：  
  
  ```cpp
  explicit BoundingBox(const Location &in_location,
                       const Vector3D &in_extent);
  ```
- **说明**：指定中心和半尺寸，旋转为默认 `(0,0,0)`。  
- **示例**：  
  ```cpp
  BoundingBox bb2(loc, ext);
  ```

- **带参构造**：  
  
  ```cpp
  explicit BoundingBox(const Vector3D &in_extent);
  ```
- **说明**：指定半尺寸，中心和旋转使用默认值。  
- **示例**：  
  ```cpp
  BoundingBox bb3(ext);
  ```

---

## 核心方法

### **<font color="#7fb800">Contains</font>**
- **原型**：  
  ```cpp
  bool Contains(const Location &in_world_point,
                const Transform &in_bbox_to_world_transform) const;
  ```
- **说明**：判断世界空间点是否在边界盒内。  
  1. 使用 `inverseTransform` 将世界点变换到盒子局部空间；  
  2. 相对于 **<font color="#f8805a">location</font>** 归一化；  
  3. 判断坐标是否在 ±**<font color="#f8805a">extent</font>** 范围内。  
- **示例**：  
  ```cpp
  Location pt(1.1f,2.0f,3.0f);
  Transform tr(...);
  bool inside = bb1.Contains(pt, tr);
  ```

### **<font color="#7fb800">GetLocalVertices</font>**
- **原型**：  
  ```cpp
  std::array<Location,8> GetLocalVertices() const;
  ```
- **说明**：返回考虑旋转后的 8 个顶点在局部空间的位置：  
  $$\displaystyle \text{vertex}_i = \text{location} + \text{rotation.RotateVector}(\pm extent.x,\pm extent.y,\pm extent.z).$$  
- **示例**：  
  ```cpp
  auto verts = bb1.GetLocalVertices();
  ```

### **<font color="#7fb800">GetLocalVerticesNoRotation</font>**
- **原型**：  
  ```cpp
  std::array<Location,8> GetLocalVerticesNoRotation() const;
  ```
- **说明**：返回不考虑旋转，仅基于 **<font color="#f8805a">location</font>** 与 **<font color="#f8805a">extent</font>** 的 8 个顶点。  
- **示例**：  
  ```cpp
  auto vertsNR = bb1.GetLocalVerticesNoRotation();
  ```

### **<font color="#7fb800">GetWorldVertices</font>**
- **原型**：  
  ```cpp
  std::array<Location,8> GetWorldVertices(const Transform &in_bbox_to_world_tr) const;
  ```
- **说明**：先调用 **<font color="#7fb800">GetLocalVertices</font>**，再对每个顶点应用 `TransformPoint`，得到世界坐标顶点数组。  
- **示例**：  
  ```cpp
  auto worldVerts = bb1.GetWorldVertices(tr);
  ```

---

## 比较运算符

### **<font color="#7fb800">operator==</font>** / **<font color="#7fb800">operator!=</font>**
- **原型**：  
  ```cpp
  bool operator==(const BoundingBox &rhs) const;
  bool operator!=(const BoundingBox &rhs) const;
  ```
- **说明**：当且仅当 **<font color="#f8805a">location</font>**, **<font color="#f8805a">extent</font>**, **<font color="#f8805a">rotation</font>** 全部相等时才判定相等。  
- **示例**：  
  ```cpp
  bool eq = (bb1 == bb2);
  ```

---

## UE4 类型互转（`LIBCARLA_INCLUDED_FROM_UE4`）

### **<font color="#7fb800">BoundingBox(const FBoundingBox &Box)</font>**
- **说明**：将 UE4 `FBoundingBox` 转换为本地类型，单位从厘米转米：  
  $$\text{location}=Box.Origin,\quad \text{extent}=(Box.Extent/100).$$  
- **示例**：  
  ```cpp
  FBoundingBox ubox;
  BoundingBox bbU(ubox);
  ```

---

<span id="GeoLocation"></span>

# [GeoLocation](#GeoLocation)

## 概述
`carla::geom::GeoLocation` 用于在真实地理坐标系（WGS84，经纬度+海拔）与仿真局部坐标系`carla::geom::Location`（CARLA 自定义坐标）之间进行转换。当 CARLA 场景与 **OpenDRIVE 地图**或**真实地理数据（如地图对齐或高精地图）**结合时，`GeoLocation` 能实现：设定仿真地图的锚点（anchor）；映射仿真场景中物体的位置到全球坐标；实现与外部设备或真实车辆的数据融合（如 GPS 传感器仿真）。

---

| 使用情景           | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| **GPS 传感器仿真** | 通过 `GeoLocation`，GPS 传感器组件可以返回真实世界的纬度、经度、海拔值。 |
| **地理信息对齐**   | 将 CARLA 场景对齐到某一个真实地图（例如：以某个真实位置为原点）。 |
| **与高精地图接口** | 将车辆位置转换为 HD-Map 参考坐标，支持自动驾驶算法中的路径规划与定位模块。 |
| **坐标系统转换**   | 与外部系统（如 ROS、Apollo、Autoware）通信时，经常需要将局部坐标转换为 WGS84。 |

## 公共数据成员

- **<font color="#f8805a">latitude</font>** (double)：纬度，单位度 (°)，初始值 `0.0`  
- **<font color="#f8805a">longitude</font>** (double)：经度，单位度 (°)，初始值 `0.0`  
- **<font color="#f8805a">altitude</font>** (double)：海拔，单位米 (m)，初始值 `0.0`  

---

## 构造函数

### **<font color="#7fb800">GeoLocation()</font>**
- **原型**：`GeoLocation() = default;`  
- **说明**：使用默认值构造。  
- **示例**：  
  ```cpp
  GeoLocation g0; // (0,0,0)
  ```

### **<font color="#7fb800">GeoLocation(double latitude, double longitude, double altitude)</font>**
- **原型**：  
  ```cpp
  GeoLocation(double latitude, double longitude, double altitude);
  ```
- **说明**：按指定经纬度及海拔初始化。  
- **示例**：  
  ```cpp
  GeoLocation g1(37.7749, -122.4194, 30.0);
  ```

---

## 核心方法

### **<font color="#7fb800">Transform</font>**
- **原型**：  
  ```cpp
  GeoLocation Transform(const Location &location) const;
  ```
- **说明**：  
  1. 将当前经纬度和平面位移（**<font color="#f8805a">location.x</font>**, **<font color="#f8805a">location.y</font>**）转换为新的经纬度；  
  2. **<font color="#f8805a">altitude</font>** 累加 **<font color="#f8805a">location.z</font>**。  
- **示例**：  
  
  ```cpp
  GeoLocation geo(0.0, 0.0, 100.0);
  Location loc(10.0f, 20.0f, 5.0f);
  GeoLocation res = geo.Transform(loc);
  // 计算后 res.latitude, res.longitude 变化，res.altitude == 105.0
  ```

**转换原理**  

- 利用墨卡托投影将 `(latitude, longitude)` 映射为 `(mx, my)`；  
- 在投影平面上加上 `dx = location.x`、`dy = -location.y`（北向为正）；  
- 反变换回经纬度；  
- 海拔相加。

---

## 静态辅助函数

- **<font color="#7fb800">LatToScale</font>**  
  ```cpp
  static double LatToScale(double lat);
  ```
  - 说明：比例因子 \(=\cos(\mathrm{toRadians}(lat))\)。  

- **<font color="#7fb800">LatLonToMercator</font>** *(模板)*  
  
  ```cpp
  template<class T>
  static void LatLonToMercator(double lat, double lon, double scale, T &mx, T &my);
  ```
  - 说明：  
    $$mx = scale \times R \times \mathrm{toRadians}(lon),$$  
    $$my = scale \times R \times \ln\!\tan\Bigl(\tfrac{90+lat}{360}\pi\Bigr).$$  
  
- **<font color="#7fb800">MercatorToLatLon</font>**  
  ```cpp
  static void MercatorToLatLon(double mx, double my, double scale, double &lat, double &lon);
  ```
  - 说明：  
    $$lon = mx\tfrac{180}{\pi R\,scale},\quad
      lat = 360\arctan\exp\bigl(\tfrac{my}{R\,scale}\bigr)/\pi -90.$$

- **<font color="#7fb800">LatLonAddMeters</font>**  
  ```cpp
  static void LatLonAddMeters(
      double lat_start, double lon_start,
      double dx, double dy,
      double &lat_end, double &lon_end);
  ```
  - 说明：在起始经纬度处，沿东(dx)/北(dy)方向（米）偏移后计算新的经纬度。

---

## 比较运算符

### **<font color="#7fb800">operator==</font>** / **<font color="#7fb800">operator!=</font>**
- **原型**：  
  
  ```cpp
  bool operator==(const GeoLocation &rhs) const;
  bool operator!=(const GeoLocation &rhs) const;
  ```
- **说明**：当且仅当经度、纬度、海拔全相等时返回 `true`。  
- **示例**:  
  
  ```cpp
  bool same= (g1 == GeoLocation(37.7749,-122.4194,30.0));
  ```

---

## 序列化

- 使用 `MSGPACK_DEFINE_ARRAY(latitude, longitude, altitude)` 支持 MsgPack 序列化/反序列化。
