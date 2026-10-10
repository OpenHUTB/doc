# 目录
- [1. 概述](#1-概述)
- [2. 核心函数说明](#2-核心函数说明)
  - [2.1 BuildMeshDescriptionFromData](#21-buildmeshdescriptionfromdata)
  - [2.2 CreateMesh](#22-createmesh)
  - [2.3 GetTransversemercProjection](#23-gettransversemercprojection)
  - [2.4 辅助函数](#24-辅助函数)
- [3. 关键数据结构](#3-关键数据结构)
  - [FProceduralCustomMesh](#fproceduralcustommesh)
- [4. 使用示例](#4-使用示例)
- [5. 注意事项](#5-注意事项)
  - [性能优化](#性能优化)
  - [错误处理](#错误处理)
  - [坐标系统](#坐标系统)
- [6. 扩展建议](#6-扩展建议)

# 1. 概述
UMapGenFunctionLibrary 是用于 Carla 地图生成的核心工具类，提供网格构建、资源管理、坐标投影等功能。
主要功能：

* 将自定义网格数据转换为 Unreal Engine 的 FMeshDescription。

* 创建并保存静态网格资源（UStaticMesh）。

* 执行墨卡托投影转换（地理坐标→引擎坐标）。

* 辅助渲染命令与资源清理。

# 2. 核心函数说明

## 2.1 BuildMeshDescriptionFromData

功能：将自定义网格数据转换为 FMeshDescription，包含顶点、三角形、法线、UV 等信息。
参数：
```shell
Data (FProceduralCustomMesh): 输入网格数据（顶点、三角形、UV 等）。

ParamTangents (TArray<FProcMeshTangent>): 顶点切线数据。

MaterialInstance (UMaterialInstance*): 材质实例。
```


返回值：
```shell
FMeshDescription: 构建的网格描述对象，用于后续生成静态网格。
```


!!! 注意事项

    若 ParamTangents 数量与顶点数不匹配，切线数据将无法正确设置。
    
    UV 通道默认填充为 (0,0)，需确保输入 UV 数据正确。


## 2.2 CreateMesh

功能：基于 FMeshDescription 创建并保存静态网格资源（.uasset）。

参数：
```shell
Data (FProceduralCustomMesh): 输入网格数据。

ParamTangents (TArray<FProcMeshTangent>): 顶点切线数据。

MaterialInstance (UMaterialInstance*): 材质实例。

MapName (FString): 地图名称，用于资源路径。

FolderName (FString): 资源存储文件夹。

MeshName (FName): 网格资源名称。
```


返回值：
```shell
UStaticMesh*: 生成的静态网格资源指针，失败返回 nullptr。
```


关键流程：

* 构建资源包路径（如 /Game/CustomMaps/MapName/Static/FolderName/MeshName）。

* 调用 BuildMeshDescriptionFromData 生成网格描述。

* 创建 UStaticMesh 对象并设置材质、碰撞体等属性。

* 保存资源并通知资源管理器。

!!! 注意事项

    目录创建逻辑被注释（PlatformFile.CreateDirectory），需手动启用。
    
    需确保材质实例有效，否则记录错误日志。

## 2.3 GetTransverseMercProjection
功能：将经纬度坐标转换为引擎内的平面墨卡托投影坐标（单位：厘米）。
示例：
```cpp
FVector2D Position = UMapGenFunctionLibrary::GetTransverseMercProjection(39.9, 116.4, 39.9, 116.4);  
// 输出: (0, 0)（原点坐标） 
```

## 2.4 辅助函数
```shell
SetThreadToSleep
功能：使当前线程休眠指定秒数。
参数：
- Seconds (float)：休眠时间，单位秒。


FlushRenderingCommandsInBlueprint
功能：强制刷新渲染命令队列，确保图形操作完成。

CleanupGEngine
功能：执行垃圾回收并清理编辑器事务（仅编辑器模式下生效）。
```


# 3. 关键数据结构
成员：

- `Vertices` (`TArray<FVector>`)：顶点坐标数组，引擎坐标系（单位：厘米）。
- `Triangles` (`TArray<int32>`)：三角形索引数组，顶点顺序为顺时针时代表正面。
- `Normals` (`TArray<FVector>`)：逐顶点法线，应与 `Vertices` 一一对应。
- `UV0` (`TArray<FVector2D>`)：第一套 UV 坐标，每个元素为 `(U, V)`，范围通常为 `[0, 1]`。

注意事项：

- `UV0` 使用 `FVector2D` 而非 `FVector`，传入 `FVector` 将导致编译错误。
- `Normals` 数组若为空，网格描述仍可生成，但光照结果可能异常，建议始终填充。
```


# 4. 使用示例
生成静态网格
cpp
 // 1. 准备数据
FProceduralCustomMesh Data;   
Data.Vertices = { FVector(0,0,0), FVector(100,0,0), FVector(0,100,0) };  
Data.Triangles = { 0, 1, 2 };   
Data.Normals = { FVector(0,0,1), FVector(0,0,1), FVector(0,0,1) };   

// 2. 创建材质实例    
UMaterialInstance* Material = LoadObject<UMaterialInstance>(
    nullptr, 
    TEXT("/Game/Materials/MI_Road.MI_Road") // 替换为实际材质路径
); 

// 3. 生成网格  
UStaticMesh* Mesh = UMapGenFunctionLibrary::CreateMesh(  
    Data,  
    TArray<FProcMeshTangent>(),  
    Material,  
    "TestMap",  
    "Roads",  
    "RoadMesh"  
);
```

# 5. 注意事项
* 性能优化

    避免频繁调用 CreateMesh，建议批量生成后统一保存。
    
    启用异步加载（AsyncLoading）减少主线程卡顿。

* 错误处理

    检查 MaterialInstance 是否有效，否则触发 UE_LOG 错误。
    
    确保输入数据（如顶点数、三角形索引）合法。

* 坐标系统

    引擎使用左手坐标系，Y 轴反向（投影函数中 -(y - y0) 处理）。

# 6. 扩展建议

动态LOD：根据视距动态调整网格细节。

异步生成：将 CreateMesh 移至后台线程，避免阻塞游戏逻辑。 

错误恢复：添加资源创建失败时的回滚机制。 
