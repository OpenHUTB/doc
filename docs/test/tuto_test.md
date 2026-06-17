# 测试框架

HUTB 的测试框架目前只支持 Ubuntu 平台，执行命令`make smoke_tests`进行测试。

测试命令：
```shell
CarlaUE4.exe --carla-rpc-port=3654 --carla-streaming-port=0 -nosound
conda activate hutb_3.10
cd PythonAPI/test
# -m (module)：以模块运行
# -v (verbose)：打印详细信息
python -m nose2 -v smoke.test_spawnpoints.TestSpawnpoints
 >spawn.log
```

所有地图：
```text
AirSimAssets, AnnotationColorLandscape, HutbCarlaCity, Town01,
    Town01_Opt, Town02, Town02_Opt, Town03, Town03_Opt, Town04,
    Town04_Opt, Town05, Town05_Opt, Town06, Town06_Opt, Town07,
    Town07_Opt, Town10HD, Town10HD_Opt, Town11, Town12, Town13,
    Town15, Trees, baidutest2test, light.
```





## vscode 调试环境搭建

点击菜单的`Run -> Add Configuration`（或打开`launch.json`），配置运行的是模块`module`而不是程序、当前路径`cwd`、运行指定的测试`args`：
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Current File with Arguments",
            "type": "debugpy",
            "request": "launch",
            // "program": "${file}",
            "module": "nose2",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/PythonAPI/test/",
            "args": [
                "-v", "smoke.test_spawnpoints.TestSpawnpoints"
            ]
        }
    ]
}
```


## [pypi 本地服务搭建](https://www.cnblogs.com/phyger/p/19180033)

```bat
rem https://github.com/pypiserver/pypiserver
pip install pypiserver
cd Build\dependencies\pypi
pypi-server.exe
rem 准备包
pip download  simplejson
rem pip download -i https://pypi.tuna.tsinghua.edu.cn/simple simplejson
rem 从本地源搜索
rem Note that pip search does not currently work with the /simple/ endpoint.
rem pip search -i http://localhost:8080 simplejson
rem 安装前检查包是否存在
pip show simplejson
pip install -i http://localhost:8080/simple simplejson
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


* 调试生成点冲突的问题：

虚幻编辑器跳转到指定位置（位置单位为米，打印出来的冲突点需要乘以100）：
```
bugitgo 0 0 0 0 0 0
```

高度需要调低，否则会碰到树产生冲突。
方向也要和道路的方向一致。

将VehicleSpawnPoint{ID}从000进行编号命名，报错信息中的idx即为编辑器中 VehicleSpawnPoint{ID} 后的ID。
```
  - idx=69, bp=vehicle.bydsong-1.bydsong-1, actor_id=0, loc=(298.919,-359.228,156.824), rot=(-0.16,-170.40,0.00), error=Spawn failed because of collision at spawn position
```


验证在所有生成点生成车辆，他们之间是否会产生冲突；冲突的原因有：距离太近、车辆太大、生成点太高导致生成时就发生碰撞等。

* 生成车辆的位置和车辆的位置发生偏差。
```text
  File "D:\hutb\PythonAPI\test\smoke\test_spawnpoints.py", line 132, in test_spawn_points
    self.assertAlmostEqual(
AssertionError: 896.038818359375 != 896.6028442382812 within 2 places (0.56402587890625 difference) : X position mismatch.
actor_id=309
x: expected=896.0388, got=896.6028, diff=0.5640
```
**调试**：确定发生偏差的生成点：这个actor_id并不是从0开始，调试 ids 发现：开始的 204 对应的是生成点 000，所以309对应的是 105。
如果是后面的车辆测试时候失败，对应的生成点 id = 报错的id - ids的偏置 - 总生成点数 * 前面测试成功的车辆数 = actor_id - 204 - 319 * 2

**解决**：调整生成点的方向、降低高度会缩小偏差

已知问题：编辑器独立模式运行Town03、Town15测试生成点会导致内存溢出（63GB机器）、打包后的场景并不会出现内存溢出。


生成点的旋转中的 Y 不为0度会报生成车的俯仰角和生成点的俯仰角不一致的错：
```
AssertionError: -3.3536911010742188 != -3.3598382472991943 within 2 places (0.006147146224975586 difference) : Pitch mismatch.
actor_id=2627
pitch: expected=-3.3537, got=-3.3598, diff=0.0061
```
地面不平的话，生成点的Y（俯仰有一定角度）设置为地面（got）的俯仰角。expected为生成点的俯仰角、got为地面的俯仰角。

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


* Town03 测试时发现先显示第一视角的VR模式，然后再切换到 Air 模式

---


测试失败：
```shell
conda activate hutb
cd PythonAPI/test
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
    ...
    "C:\actions-runner\_work\hutb\hutb\PythonAPI\test\smoke\test_spawnpoints.py", line 74, in test_spawn_points
    2026-05-27T00:11:26.3321283Z     if spawn_errors else "Spawn errors detected (no details)"
    2026-05-27T00:11:26.3321745Z AssertionError: True is not false : Spawn errors detected:
    2026-05-27T00:11:26.3322565Z   - idx=13, bp=vehicle.bus-2.bus-2, actor_id=0, loc=(191.080,55.840,0.300), rot=(0.00,180.00,0.00), error=Spawn failed because of collision at spawn position
    ```

    原因：

    vehicle.bus-2.bus-2、vehicle.bus-1.bus-1 车太大了，在生成点产生冲突。

    解决：在车辆工厂中暂时移除。

---

* 内存泄漏

    vehicle.wuling-2.wuling-2（不确定） 会导致内存急剧（消耗了28G）上升直到场景出现 Out of video memory trying to allocate a rendering resource，注释了也没用。

    vehicle.bydsong-1、
    vehicle.volkswagen.t2_2021、vehicle.wj.wj、vehicle.hongqi-2.hongqi-2、vehicle.byd_bus.byd_bus、vehicle.mini-4.mini-4、hongqi-1、vehicle.bus-2.bus-2、

    使用LOD技术：Level of Detail (LOD) 技术可以根据距离摄像机的远近来加载不同精细程度的模型和纹理，从而降低GPU和内存的负担。

    解决：打包后不会出现内存爆炸的问题。

* Python 3.9 报错：TypeError: dataclass() got an unexpected keyword argument 'slots'

    复现：pip install --force-reinstall  hutb/hutb/Build/UE4Carla/ce082bb54/WindowsNoEditor/PythonAPI/carla/dist/hutb-2.9.16-cp39-cp39-win_amd64.whl
    ```shell
    # 安装的是 pip-26.1.1-pyhc872135_0，最新的为：26.5.0
    conda create -n hutb_3.9 python=3.9 --yes
    conda deactivate && conda remove -n hutb_3.9 --all --yes
    ```

    报错信息：
    ```text
    (hutb_3.9) D:\hutb\PythonAPI\examples\air>pip --version
    ...
        from pip._internal.models.scheme import SCHEME_KEYS, Scheme
    File "D:\hutb\Build\dependencies\prerequisites\miniconda3\envs\hutb_3.9\lib\site-packages\pip\_internal\models\scheme.py", line 13, in <module>
        @dataclass(frozen=True, slots=True)
    TypeError: dataclass() got an unexpected keyword argument 'slots'
    ```

    [原因](https://github.com/sgl-project/sglang/pull/8396)：类的装饰器中移除slots=True参数，因为 [slots参数是在 Python 3.10 中引入的](https://docs.python.org/3/library/dataclasses.html)。

    解决：
    ```shell
    python -m pip install --upgrade pip
    ```
    D:\hutb\Build\dependencies\prerequisites\miniconda3\envs\hutb_3.9\lib\site-packages\pip\_internal\models\scheme.py
    D:\hutb\Build\dependencies\prerequisites\miniconda3\envs\hutb_3.9\lib\site-packages\pip\_internal\models\release_control.py
    D:\hutb\Build\dependencies\prerequisites\miniconda3\envs\hutb_3.9\lib\site-packages\pip\_internal\models\selection_prefs.py

---



```shell
python -m nose2 -v smoke.test_sync.TestSynchronousMode
```

## CI/CD

参考 [链接](https://www.cnblogs.com/dotnet261010/p/11495762.html) 进行软件的安装。

