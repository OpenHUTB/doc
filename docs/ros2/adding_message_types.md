# 向 Carla 添加新的 ROS 2 消息类型

Carla 使用 Fast-CDR（Common Data Representation）将手写的 C++ POD （Plain Old Data）结构体直接序列化到 CDR 字节缓冲区，从而发布 ROS 2 数据。构建时没有 IDL（Interface Definition Language）编译器或代码生成步骤。因此，支持新的消息类型需要手动完成 7 个步骤。本指南将逐步介绍每个步骤。

## 前提条件

- 已安装并运行 Docker（仅在步骤 [4](#step_4) 中需要）。
- 要添加的类型的 `.msg` 文件。标准的 ROS 2 类型（例如 `sensor_msgs/msg/NavSatFix`）在任何 ROS 2 安装中都已存在。如果您要定义新的 `carla_msgs` 类型，请先编写它（参见步骤 [1](#step_1)）。 

---

## 步骤 1 - 编写 `.msg` 文件（标准 ROS 2 类型可跳过此步骤） <span id='step_1'></span>

如果该类型已存在于标准 ROS 2 包中，请跳过此步骤，并在步骤 [4](#step_4) 中使用现有的 `.msg` 文件。

对于新的 `carla_msgs` 类型，请按照 [ROS 2 接口定义格式](https://design.ros2.org/articles/legacy_interface_definition.html) 创建 `.msg` 文件。每行要么是字段声明，要么是注释（`# ...`）：

```
# carla_msgs/msg/CarlaSpeedometer.msg
std_msgs/Header header
float32 speed   # m/s
```

嵌套类型的字段类型名称使用 `pkg_name/TypeName`（字段行本身不包含 `msg/`）。支持的基本类型：`bool`、`int8`、`uint8`、`int16`、`uint16`、`int32`、`uint32`、`int64`、`uint64`、`float32`、`float64`、`string`。固定数组使用 `type[N]`；无界序列使用 `type[]`。

---

## 步骤 2 - 创建 C++ POD 结构体  <span id='step_2'></span>

创建 `LibCarla/source/carla/ros2/types/msg/MyType.h` 文件。规则：

- 该结构体位于命名空间 `namespace carla::ros2::msg` 中。
- 仅包含 `<array>`、`<vector>`、`<string>`、`<cstdint>` 以及同级的 `msg/*.h` 头文件 - 不包含 DDS 或 Fast-CDR。
- 将基本类型字段初始化为零，使用 `= 0` 或 `= 0.0`。 
- 对于固定长度数组，使用 `std::array<T, N>`；对于无界序列，使用 `std::vector<T>`。
- 按值嵌套其他消息类型。

**叶子类型**（所有字段均为基本类型）：

```cpp
// LibCarla/source/carla/ros2/types/msg/MyLeaf.h
#pragma once
#include <cstdint>

namespace carla { namespace ros2 { namespace msg {

struct MyLeaf {
  float speed = 0.0f;
  uint32_t count = 0u;
};

}}} // namespace carla::ros2::msg
```

**复合类型**（嵌套消息、固定数组、字符串）：

```cpp
// LibCarla/source/carla/ros2/types/msg/MyComposite.h
#pragma once
#include <array>
#include <string>
#include "carla/ros2/types/msg/Header.h"
#include "carla/ros2/types/msg/Vector3.h"

namespace carla { namespace ros2 { namespace msg {

struct MyComposite {
  Header header;
  std::string frame_id;
  Vector3 velocity;
  std::array<double, 9> covariance = {};   // 固定的 3x3 矩阵
};

}}} // namespace carla::ros2::msg
```

**序列类型**（可变长度向量）：

```cpp
// LibCarla/source/carla/ros2/types/msg/MyList.h
#pragma once
#include <vector>
#include "carla/ros2/types/msg/SomeElement.h"

namespace carla { namespace ros2 { namespace msg {

struct MyList {
  std::vector<SomeElement> items;
};

}}} // namespace carla::ros2::msg
```

### 并排示例：`.msg` 到 POD

将 `sensor_msgs/msg/Imu.msg` 完全转换为等效的 POD 结构体。每个 `.msg` 行都按顺序映射到一个 C++ 字段；嵌套类型解析为相应的 `msg::*` 结构体并通过头文件包含。

`sensor_msgs/msg/Imu.msg`:

```
# sensor_msgs/msg/Imu.msg
std_msgs/Header header
geometry_msgs/Quaternion orientation
float64[9] orientation_covariance
geometry_msgs/Vector3 angular_velocity
float64[9] angular_velocity_covariance
geometry_msgs/Vector3 linear_acceleration
float64[9] linear_acceleration_covariance
```

`LibCarla/source/carla/ros2/types/msg/Imu.h`:

```cpp
// LibCarla/source/carla/ros2/types/msg/Imu.h
#pragma once
#include <array>
#include "carla/ros2/types/msg/Header.h"
#include "carla/ros2/types/msg/Quaternion.h"
#include "carla/ros2/types/msg/Vector3.h"

namespace carla { namespace ros2 { namespace msg {

struct Imu {
  Header header;
  Quaternion orientation;
  std::array<double, 9> orientation_covariance = {};
  Vector3 angular_velocity;
  std::array<double, 9> angular_velocity_covariance = {};
  Vector3 linear_acceleration;
  std::array<double, 9> linear_acceleration_covariance = {};
};

}}} // namespace carla::ros2::msg
```

上述映射规则：

| `.msg` 标记                   | C++ 字段                                |
| ------------------------------ | ---------------------------------------- |
| `std_msgs/Header header`       | `Header header;` （按值嵌套）       |
| `geometry_msgs/Quaternion q`   | `Quaternion q;` （按值嵌套）        |
| `float64[9] covariance`        | `std::array<double, 9> covariance = {};` |
| `float64 x`                    | `double x = 0.0;`                        |
| `string frame_id`              | `std::string frame_id;`                  |
| `type[] items`                 | `std::vector<type> items;`               |


!!! 注意
    `type_name()` 函数（步骤 [5](#step_5)）中的 `dds_::Imu_` 类型修饰以及 DDS 线格式均通过 Fast-CDR 从此 POD 布局自动派生；无需维护单独的 IDL 定义。

---

## 步骤 3 - 注册 CDR 序列化  <span id='step_3'></span>

打开 [LibCarla/source/carla/ros2/types/CdrSerialization.h](https://github.com/OpenHUTB/hutb/blob/hutb/LibCarla/source/carla/ros2/types/CdrSerialization.h) 文件并添加：

1. 在文件顶部添加一个包含新头文件的 `#include` 语句。
2. 添加一个 `serialize_cdr` / `deserialize_cdr` 重载对。

**放置位置**：将重载添加到结构体所依赖的任何类型的重载之后（文件按依赖程度从低到高排序，以避免前向声明）。

**叶子类型示例**（仅限基本类型 - 使用 `cdr <<` / `cdr >>`）：

```cpp
inline void serialize_cdr(
    eprosima::fastcdr::Cdr& cdr, const msg::MyLeaf& m) {
  cdr << m.speed;
  cdr << m.count;
}

inline void deserialize_cdr(
    eprosima::fastcdr::Cdr& cdr, msg::MyLeaf& m) {
  cdr >> m.speed;
  cdr >> m.count;
}
```

**复合类型示例**（嵌套类型调用它们自己的重载；字符串和 `std::array` 通过 `cdr <<` 直接序列化）：

```cpp
inline void serialize_cdr(
    eprosima::fastcdr::Cdr& cdr, const msg::MyComposite& m) {
  serialize_cdr(cdr, m.header);   // 嵌套消息（msg::）类型
  cdr << m.frame_id;              // std::string
  serialize_cdr(cdr, m.velocity); // 嵌套消息（msg::）类型
  cdr << m.covariance;            // std::array<double, 9>
}

inline void deserialize_cdr(
    eprosima::fastcdr::Cdr& cdr, msg::MyComposite& m) {
  deserialize_cdr(cdr, m.header);
  cdr >> m.frame_id;
  deserialize_cdr(cdr, m.velocity);
  cdr >> m.covariance;
}
```

**序列示例**（`std::vector` 结构体 - 手动写入长度）：

```cpp
inline void serialize_cdr(
    eprosima::fastcdr::Cdr& cdr, const msg::MyList& m) {
  // 根据 DDS-XTypes 1.3 条款 7.4.1.1，CDR 序列长度为 uint32_t
  cdr << static_cast<uint32_t>(m.items.size());
  for (const auto& item : m.items) {
    serialize_cdr(cdr, item);
  }
}

inline void deserialize_cdr(
    eprosima::fastcdr::Cdr& cdr, msg::MyList& m) {
  uint32_t n{0u};
  cdr >> n;
  if (n > kMaxCdrSequenceElements) {
    throw eprosima::fastcdr::exception::BadParamException(
        "MyList::items length exceeds sane CDR sequence cap");
  }
  m.items.resize(static_cast<size_t>(n));
  for (auto& item : m.items) {
    deserialize_cdr(cdr, item);
  }
}
```

对于 `std::vector<uint8_t>`（字节数组，例如 `Image::data`），FastCDR 会自动处理长度前缀，只需使用 `cdr << m.data` 即可，无需手动循环。

---

## 步骤 4 - 计算 RIHS01 类型哈希  <span id='step_4'></span>

ROS 2 Iron 及更高版本会在两个节点相互发现时检查 DDS `USER_DATA` QoS 字段中的类型哈希。如果哈希不存在，则每个端点都会记录：

```
[WARN] [rmw_cyclonedds_cpp]: Failed to parse type hash for topic 'rt/...'
```

Carla 会在每种消息类型的 `CdrTopicInfo<T>::type_hash()` 函数中嵌入一个硬编码的 RIHS01 哈希值。使用 `Util/ros2/compute_type_hash.sh` 脚本可以获取特定类型的正确哈希值。此脚本仅需 Docker 容器，无需本地安装 ROS 2。

**标准 ROS 2 类型**（`.msg` 文件已安装在容器内）：

```sh
# 首先从容器中提取 Imu.msg，然后进行计算：
docker run --rm osrf/ros:jazzy-desktop \
    cat /opt/ros/jazzy/share/sensor_msgs/msg/Imu.msg > /tmp/Imu.msg

Util/ros2/compute_type_hash.sh sensor_msgs/msg/Imu /tmp/Imu.msg
# 输出: RIHS01_7d9a00ff...
```

**新增 `carla_msgs` 类型**（请提供您自己的 `.msg` 文件）：

```sh
Util/ros2/compute_type_hash.sh \
    carla_msgs/msg/CarlaSpeedometer \
    /path/to/carla_msgs/msg/CarlaSpeedometer.msg
# 输出: RIHS01_<64 hex chars>
```

该脚本向标准输出打印一行：

```
RIHS01_<64 lowercase hex digits>
```

将此值粘贴到步骤 [5](#step_5) 中的 `CdrTopicInfo.h` 文件中。

!!! 故障排除
    如果在 Docker 中构建 colcon（`colcon build`）失败，最常见的原因是缺少 `.msg` 依赖项，而该依赖项不在标准的 `jazzy` 安装包中。请将缺失的软件包添加到 `rosidl_generate_interfaces` 工作区，或者，对于最新版本的软件包，请切换到更新的 `osrf/ros` 标签。

---

## 步骤 5 - 在 `CdrTopicInfo.h` 中注册  <span id='step_5'></span>

向 [LibCarla/source/carla/ros2/types/CdrTopicInfo.h](https://github.com/OpenHUTB/hutb/blob/hutb/LibCarla/source/carla/ros2/types/CdrTopicInfo.h) 添加一个特化（specialization）：

```cpp
template<> struct CdrTopicInfo<msg::MyComposite> {
  static const char* type_name() {
    // DDS 名称混淆：<package>::msg::dds_::<TypeName>_
    return "my_pkg::msg::dds_::MyComposite_";
  }
  static const char* type_hash() {
    return "RIHS01_<hash from Step 4>";
  }
  static size_t max_serialized_size() { return <byte count>u; }
};
```

此外，请在 `CdrTopicInfo.h` 文件顶部添加新头文件的 `#include` 指令。

**`type_name()`:** 遵循 ROS 2 RMW 使用的 DDS 名称混淆约定：`<package>::msg::dds_::<TypeName>_`（注意末尾的下划线）。

**`type_hash()`:** REP-2011 类型哈希值，由所有写入器和读取器在 `USER_DATA` QoS 字段中发布（REP-2016 有效载荷 `typehash=RIHS01_<hex>;`）。对等 ROS 2 RMW 在发现过程中读取此哈希值，以执行基于类型哈希值的端点匹配，并且在 Jazzy 及更高版本中，用于抑制`Failed to parse type hash for topic ...`警告。

粘贴步骤 [4](#step_4) 中的  `RIHS01_...` 字符串。哈希值是按消息定义固定的；如果 `.msg` 定义发生更改，请更新它。

```cpp
// 典型案例：固定根据 .msg 定义计算出的哈希值
static const char* type_hash() {
  return "RIHS01_7d9a00ff...";  // “RIHS01_”之后的64个十六进制字符
}
```

仅当无法为该类型计算规范哈希值时（例如，没有对应 `.msg` 文件的自定义有效负载），才返回 `nullptr`。此时，中间件会为该端点发出一个空的 `USER_DATA` 有效负载；对等方会在 Jazzy 日志中记录缺失类型哈希值的警告，但连接仍然会建立。

```cpp
// 备用方案：此类型不存在规范的 .msg 文件
static const char* type_hash() {
  return nullptr;
}
```

**`max_serialized_size()`:** 预分配内存大小的提示（以字节为单位），不包括 4 字节的 DDS 封装头。对于固定长度类型，将所有字段的字节大小相加。对于可变长度类型，选择一个合理的上限值。这只是一个提示；实际有效载荷的大小是动态确定的。

快速大小调整指南：

- `bool`, `uint8`, `int8`: 1 字节
- `uint16`, `int16`: 2 字节
- `uint32`, `int32`, `float32`: 4 字节
- `uint64`, `int64`, `float64`, `double`: 8 字节
- `std::string`: 4（长度）+ 容量估计值（字节）
- `std::array<double, 9>`: 72 字节
- 嵌套结构体：递归地对其字段求和

---

## 步骤 6 - 添加测试  <span id='step_6'></span>

打开 [LibCarla/source/test/server/test_type_hash.cpp](https://github.com/OpenHUTB/hutb/tree/hutb/LibCarla/source/test/server) 文件并添加：

1. 在 `TEST(TypeHash, FormatAllTypes)` 函数内添加一个 `CHECK_HASH(MyComposite)` 调用。 
2. 在 `TEST(TypeHash, UniqueAcrossAllTypes)` 函数内，在哈希向量中添加一个 `CdrTopicInfo<msg::MyComposite>::type_hash()` 条目。

这两个测试验证哈希字符串是否符合 `RIHS01_<64 hex>` 格式，并且在所有已注册的类型中是唯一的。

---

## 步骤 7 - 构建并验证  <span id='step_7'></span>

```sh
docker exec carla-development-ue4-20.04 make LibCarla ARGS="--ros2"
docker exec carla-development-ue4-20.04 make check.LibCarla
```

所有测试必须通过。如果哈希值格式错误或重复，新的 `CHECK_HASH` 条目将失败。

---

## 常见问题解答

* **为什么哈希值是硬编码的？**

  Carla 在构建时没有运行 IDL 编译器（`rosidl`、`idlc`）。正确计算 RIHS01 哈希值需要 `rosidl_generator_type_description`，而该编译器只能在 ROS 2 构建环境中运行。从一次性 Docker 构建中硬编码值是零依赖且正确的，因为标准消息定义在每个发行版中都是稳定的。

* **Humble 和 Jazzy 上的哈希值相同吗？**

是的，对于两个发行版之间定义未更改的任何消息（`std_msgs`、`geometry_msgs`、`sensor_msgs`、`nav_msgs`、`builtin_interfaces`、`tf2_msgs`、`rosgraph_msgs`、`ackermann_msgs` 中的所有消息），哈希值相同。在 Jazzy 上计算哈希值，它在 Humble 上也会匹配。


* **什么是网络传输格式？**

  经典 CDR，编码版本 1，小端序 (CDR_LE)。定义于：

  - OMG DDSI-RTPS v2.5 第 10 节（封装头）
  - DDS-XTypes 1.3 第 7.4.1.1 条（序列/字符串编码）
  - [REP-2011](https://ros.org/reps/rep-2011.html) (RIHS01 哈希算法)
  - [REP-2016](https://ros.org/reps/rep-2016.html) (USER_DATA 键值格式)

---

## 参考资料

- [OMG DDSI-RTPS v2.5 规范（PDF）](https://www.omg.org/spec/DDSI-RTPS/2.5/PDF)
