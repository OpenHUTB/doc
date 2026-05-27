# 测试框架

HUTB 的测试框架目前只支持 Ubuntu 平台，执行命令`make smoke_tests`进行测试。

测试命令：
```shell
CarlaUE4.exe --carla-rpc-port=3654 --carla-streaming-port=0 -nosound
python -m nose2 -v smoke.test_spawnpoints.TestSpawnpoints
```


## 测试内容

### 冒烟测试

#### 同步模式 [smoke.test_sync](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/test/smoke/test_sync.py)

测试在同步模式下各种功能能否正常工作

1. 验证世界重载功能 ([test_reloading_map](https://github.com/OpenHUTB/hutb/blob/9bd0e8e6d790bfe6ecc3fefbc9033fab2275accb/PythonAPI/test/smoke/test_sync.py#L23))

    * 测试在同步模式下连续重载世界地图 4 次

    * 确保每次重载后都能正确应用同步模式设置（固定时间步长 0.05 秒）

    * 包含内存清理等待时间，避免 UE4 资源冲突

2. 验证相机同步 ([_test_camera_on_synchronous_mode](https://github.com/OpenHUTB/hutb/blob/9bd0e8e6d790bfe6ecc3fefbc9033fab2275accb/PythonAPI/test/smoke/test_sync.py#L35))
测试 RGB 相机在同步模式下的数据一致性

    验证内容：

    * 每一帧的帧号是否正确递增（+1）

    * 相机图像的帧号是否与世界快照的帧号一致

    * 相机所获取图像的时间戳`image.timestamp`是否与模拟时间`world.get_snapshot().timestamp.elapsed_seconds`匹配

3. 验证多传感器变换同步 ([test_sensor_transform_on_synchronous_mode](https://github.com/OpenHUTB/hutb/blob/9bd0e8e6d790bfe6ecc3fefbc9033fab2275accb/PythonAPI/test/smoke/test_sync.py#L64))

    * 测试多种传感器（LIDAR、GNSS、雷达、IMU）在车辆移动时的数据同步

    * 验证要点：

    * 所有传感器在同一帧内都能收到数据

    * 传感器数据中的变换矩阵与实际传感器变换一致

    * 队列中没有数据积压或丢失

    * 传感器数据帧号与世界快照帧号匹配

4. 验证批量命令同步 ([test_apply_batch_sync](https://github.com/OpenHUTB/hutb/blob/9bd0e8e6d790bfe6ecc3fefbc9033fab2275accb/PythonAPI/test/smoke/test_sync.py#L171))

    测试 apply_batch_sync API 在不同时序下的行为

    三种测试场景：

    * 立即执行：在同一帧内生成车辆（帧号不变）

    * 下一帧执行：在下一帧生成车辆（帧号 +1）

    * 手动触发：批量命令后手动 tick（帧号 +1）


#### 传感器 smoke.test_sensor_determinism

测试传感器数据确定性的验证工具，确保在相同输入条件下，传感器产生的数据是完全可重复的。

#### 碰撞

smoke.test_collision_determinism 

#### 道具加载
smoke.test_props_loading

#### 传感器节拍时间
smoke.test_sensor_tick_time 
#### 地图
smoke.test_map 
#### 快照
smoke.test_snapshot 
#### 雷达
smoke.test_lidar 
#### 流
smoke.test_streamming
#### 生成点
smoke.test_spawnpoints 
#### 蓝图
smoke.test_blueprint 
#### 碰撞传感器
smoke.test_collision_sensor 
#### 世界
smoke.test_world 
#### 几何变换
smoke.test_geoconversion



### Windows 平台

脚本`src\test>check.bat`用于启动windows平台下的测试，运行的第一个测试用例为：
```shell
python -m nose2 -v smoke.test_sync smoke.test_sensor_determinism smoke.test_collision_determinism smoke.test_props_loading smoke.test_sensor_tick_time smoke.test_map smoke.test_snapshot smoke.test_lidar smoke.test_streamming smoke.test_spawnpoints smoke.test_blueprint smoke.test_collision_sensor smoke.test_world smoke.test_geoconversion
```
整个脚本会依次运行 [smoke_test_list.txt](https://github.com/OpenHUTB/doc/blob/master/src/test/smoke_test_list.txt) 文件中的所有测试用例。


测试失败：
```shell
smoke.test_spawnpoints.TestSpawnpoints
smoke.test_collision_sensor.TestCollisionSensor

smoke.test_sync.TestSynchronousMode
```
报错信息（Town03 中因为，无效的参与者描述符导致测试碰撞失败；在生成位置的生成碰撞导致生成失败）：
```text
2026-05-27T00:11:26.3311632Z ======================================================================
2026-05-27T00:11:26.3312324Z ERROR: test_single_car (smoke.test_collision_sensor.TestCollisionSensor)
2026-05-27T00:11:26.3313865Z ----------------------------------------------------------------------
2026-05-27T00:11:26.3314303Z Traceback (most recent call last):
2026-05-27T00:11:26.3315000Z   File "C:\actions-runner\_work\hutb\hutb\PythonAPI\test\smoke\test_collision_sensor.py", line 47, in test_single_car
2026-05-27T00:11:26.3315776Z     event_list = self.run_collision_single_car_against_wall(bp_veh)
2026-05-27T00:11:26.3316678Z   File "C:\actions-runner\_work\hutb\hutb\PythonAPI\test\smoke\test_collision_sensor.py", line 21, in run_collision_single_car_against_wall
2026-05-27T00:11:26.3317486Z     vehicle = self.world.spawn_actor(bp_vehicle, veh_transf)
2026-05-27T00:11:26.3318012Z RuntimeError: Spawn failed because of invalid actor description
2026-05-27T00:11:26.3318412Z 
2026-05-27T00:11:26.3318593Z ======================================================================
2026-05-27T00:11:26.3319177Z FAIL: test_spawn_points (smoke.test_spawnpoints.TestSpawnpoints)
2026-05-27T00:11:26.3319657Z ----------------------------------------------------------------------
2026-05-27T00:11:26.3320023Z Traceback (most recent call last):
2026-05-27T00:11:26.3320634Z   File "C:\actions-runner\_work\hutb\hutb\PythonAPI\test\smoke\test_spawnpoints.py", line 74, in test_spawn_points
2026-05-27T00:11:26.3321283Z     if spawn_errors else "Spawn errors detected (no details)"
2026-05-27T00:11:26.3321745Z AssertionError: True is not false : Spawn errors detected:
2026-05-27T00:11:26.3322565Z   - idx=13, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(191.080,55.840,0.300), rot=(0.00,180.00,0.00), error=Spawn failed because of collision at spawn position
```





## CI/CD

参考 [链接](https://www.cnblogs.com/dotnet261010/p/11495762.html) 进行软件的安装。

