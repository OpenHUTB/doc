# 测试框架

HUTB 的测试框架目前只支持 Ubuntu 平台，执行命令`make smoke_tests`进行测试。

测试命令：
```shell
CarlaUE4.exe --carla-rpc-port=3654 --carla-streaming-port=0 -nosound
# -m (module)：以模块运行
# -v (verbose)：打印详细信息
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

测试每个搭载碰撞传感器的车辆与墙碰撞后能够收集到碰撞事件。

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


## 问题解决

测试失败：
```shell
python -m nose2 -v smoke.test_spawnpoints.TestSpawnpoints
python -m nose2 -v smoke.test_collision_sensor.TestCollisionSensor

smoke.test_sync.TestSynchronousMode
```
报错信息（Town03 中因为，无效的参与者描述符导致测试碰撞失败；smoke.test_spawnpoints.TestSpawnpoints 在生成位置的生成碰撞导致生成失败）：


调试：[虚幻编辑器中启动带参数的场景](../ue/unreal_editor.md)。

* `Spawn failed because of invalid actor description`

    报错信息：

    ```text
    2026-05-27T00:11:26.3312324Z ERROR: test_single_car (smoke.test_collision_sensor.TestCollisionSensor)
    2026-05-27T00:11:26.3313865Z ----------------------------------------------------------------------
    2026-05-27T00:11:26.3314303Z Traceback (most recent call last):
    2026-05-27T00:11:26.3315000Z   File "C:\actions-runner\_work\hutb\hutb\PythonAPI\test\smoke\test_collision_sensor.py", line 47, in test_single_car
    2026-05-27T00:11:26.3315776Z     event_list = self.run_collision_single_car_against_wall(bp_veh)
    2026-05-27T00:11:26.3316678Z   File "C:\actions-runner\_work\hutb\hutb\PythonAPI\test\smoke\test_collision_sensor.py", line 21, in run_collision_single_car_against_wall
    2026-05-27T00:11:26.3317486Z     vehicle = self.world.spawn_actor(bp_vehicle, veh_transf)
    2026-05-27T00:11:26.3318012Z RuntimeError: Spawn failed because of invalid actor description
    ```

    原因：mini-2 （没有）等车生成不了。原来有[41种车型](https://openhutb.github.io/doc/catalogue_vehicles/)，扩展到54种。
    ```shell
    python ..\examples\manual_control.py -p 3654 --filter vehicle.mini-2.mini-2
    ```

    解决：删除车辆工厂中没有资产的车辆。


* `The collision sensor have failed for the cars`

    报错信息：
    ```text
    FAIL: test_single_car (smoke.test_collision_sensor.TestCollisionSensor)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "D:\hutb\PythonAPI\test\smoke\test_collision_sensor.py", line 56, in test_single_car
        self.fail("The collision sensor have failed for the cars: %s" % cars_failing)
    AssertionError: The collision sensor have failed for the cars:  vehicle.byd-v2.byd-v2 vehicle.hq.hq
    ```

    原因：未产生碰撞事件。

    [解决](https://github.com/carla-simulator/carla/issues/7950#issuecomment-2696074565)：参考[碰撞检测器的必要配置](../ref_sensors.md#collision-detector)



* `Spawn failed because of collision at spawn position`

    报错信息：

    ```text
    2026-05-27T00:11:26.3319177Z FAIL: test_spawn_points (smoke.test_spawnpoints.TestSpawnpoints)
    2026-05-27T00:11:26.3319657Z ----------------------------------------------------------------------
    2026-05-27T00:11:26.3320023Z Traceback (most recent call last):
    2026-05-27T00:11:26.3320634Z   File "C:\actions-runner\_work\hutb\hutb\PythonAPI\test\smoke\test_spawnpoints.py", line 74, in test_spawn_points
    2026-05-27T00:11:26.3321283Z     if spawn_errors else "Spawn errors detected (no details)"
    2026-05-27T00:11:26.3321745Z AssertionError: True is not false : Spawn errors detected:
    2026-05-27T00:11:26.3322565Z   - idx=13, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(191.080,55.840,0.300), rot=(0.00,180.00,0.00), error=Spawn failed because of collision at spawn position
    ```

    原因：

    vehicle.bus-1.bus-1 车太大了，在生成点产生冲突。 

    解决：在车辆工厂中暂时移除。

---

* 内存泄漏

    vehicle.wuling-2.wuling-2（不确定） 会导致内存急剧（消耗了28G）上升直到场景出现 Out of video memory trying to allocate a rendering resource，注释了也没用。

    vehicle.bydsong-1、
    vehicle.volkswagen.t2_2021、vehicle.wj.wj、vehicle.hongqi-2.hongqi-2、vehicle.byd_bus.byd_bus、vehicle.mini-4.mini-4、hongqi-1、vehicle.bus-2.bus-2、

---

```
(hutb) D:\hutb\PythonAPI\test>python -m nose2 -v smoke.test_spawnpoints.TestSpawnpoints
test_spawn_points (smoke.test_spawnpoints.TestSpawnpoints) ... INFO:  Found the required file in cache!  Carla/Maps/Nav/Town03.bin
TestSpawnpoints.test_spawn_points
INFO:  Found the required file in cache!  Carla/Maps/Nav/Town03.bin
INFO:  Found the required file in cache!  Carla/Maps/Nav/Town03.bin
FAIL

======================================================================
FAIL: test_spawn_points (smoke.test_spawnpoints.TestSpawnpoints)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\hutb\PythonAPI\test\smoke\test_spawnpoints.py", line 70, in test_spawn_points
    self.assertFalse(
AssertionError: True is not false : Spawn errors detected:
  - idx=12, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-77.887,33.207,0.649), rot=(-0.35,-90.16,-0.00), error=Spawn failed because of collision at spawn position
  - idx=34, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-121.302,136.416,0.275), rot=(0.00,-0.60,0.00), error=Spawn failed because of collision at spawn position
  - idx=53, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(150.919,-162.626,4.518), rot=(0.00,91.00,0.00), error=Spawn failed because of collision at spawn position
  - idx=67, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-31.326,131.243,0.275), rot=(0.00,178.70,0.00), error=Spawn failed because of collision at spawn position
  - idx=76, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(154.558,-166.591,3.788), rot=(-2.32,-89.00,0.00), error=Spawn failed because of collision at spawn position
  - idx=118, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(1.673,79.557,0.275), rot=(0.00,-88.89,0.00), error=Spawn failed because of collision at spawn position
  - idx=157, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-59.361,135.467,0.275), rot=(0.00,-1.30,0.00), error=Spawn failed because of collision at spawn position
  - idx=177, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(2.295,176.878,0.275), rot=(0.00,-90.36,0.00), error=Spawn failed because of collision at spawn position
  - idx=201, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(107.897,62.557,0.275), rot=(0.00,-0.15,0.00), error=Spawn failed because of collision at spawn position
  - idx=202, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-9.262,155.709,0.275), rot=(0.00,89.64,0.00), error=Spawn failed because of collision at spawn position
  - idx=203, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-5.762,161.587,0.275), rot=(0.00,89.64,0.00), error=Spawn failed because of collision at spawn position
  - idx=216, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(234.770,3.551,0.275), rot=(0.00,91.39,0.00), error=Spawn failed because of collision at spawn position
  - idx=221, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(4.105,-46.116,0.275), rot=(0.00,-88.59,0.00), error=Spawn failed because of collision at spawn position
  - idx=228, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-42.351,-2.835,0.275), rot=(0.00,-179.71,0.00), error=Spawn failed because of collision at spawn position
  - idx=231, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-9.018,24.411,0.275), rot=(0.00,78.62,0.00), error=Spawn failed because of collision at spawn position
  - idx=244, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(37.282,3.424,0.275), rot=(0.00,-13.67,0.00), error=Spawn failed because of collision at spawn position
  - idx=245, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(16.031,10.789,0.275), rot=(0.00,-58.80,0.00), error=Spawn failed because of collision at spawn position
  - idx=257, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(-67.324,0.537,0.275), rot=(0.00,0.29,0.00), error=Spawn failed because of collision at spawn position

----------------------------------------------------------------------
Ran 1 test in 107.533s

FAILED (failures=1)
```


所有测试的52种车辆：
```
Testing collision sensor for 52 vehicles: 
vehicle.bydsong-1.bydsong-1, vehicle.mini-3.mini-3, vehicle.byd.seal, vehicle.kawasaki.ninja, vehicle.audi.a2, vehicle.nissan.micra, vehicle.su7.su7, vehicle.audi.tt, vehicle.mercedes.coupe_2020, vehicle.bmw.grandtourer, vehicle.harley-davidson.low_rider, vehicle.ford.ambulance, vehicle.micro.microlino, vehicle.carlamotors.carlacola, vehicle.ford.mustang, vehicle.chevrolet.impala, vehicle.lincoln.mkz_2020, vehicle.lixiang-1.lixiang-1, vehicle.citroen.c3, vehicle.dodge.charger_police, vehicle.nissan.patrol, vehicle.jeep.wrangler_rubicon, vehicle.mini.cooper_s, vehicle.mercedes.coupe, vehicle.dodge.charger_2020, vehicle.ford.crown, vehicle.seat.leon, vehicle.toyota.prius, vehicle.yamaha.yzf, vehicle.xiaopeng-1.xiaopeng-1, vehicle.bh.crossbike, vehicle.tesla.model3, vehicle.gazelle.omafiets, vehicle.tesla.cybertruck, vehicle.diamondback.century, vehicle.mercedes.sprinter, vehicle.audi.etron, vehicle.volkswagen.t2, vehicle.lincoln.mkz_2017, vehicle.dodge.charger_police_2020, vehicle.vespa.zx125, vehicle.mini.cooper_s_2021, vehicle.nissan.patrol_2021, vehicle.volkswagen.t2_2021, vehicle.wj.wj, vehicle.hongqi-2.hongqi-2, vehicle.byd_bus.byd_bus, vehicle.bus-1.bus-1, vehicle.mini-4.mini-4, vehicle.hongqi-1.hongqi-1, vehicle.wuling-1.wuling-1, vehicle.wuling-2.wuling-2
```


## CI/CD

参考 [链接](https://www.cnblogs.com/dotnet261010/p/11495762.html) 进行软件的安装。

