## 测试框架

HUTB 的测试框架目前只支持 Ubuntu 平台，执行命令`make smoke_tests`进行测试。


### Windows 平台

脚本`src\test>check.bat`用于启动windows平台下的测试，运行的第一个测试用例为：
```shell
python -m nose2 -v smoke.test_sync smoke.test_sensor_determinism smoke.test_collision_determinism smoke.test_props_loading smoke.test_sensor_tick_time smoke.test_map smoke.test_snapshot smoke.test_lidar smoke.test_streamming smoke.test_spawnpoints smoke.test_blueprint smoke.test_collision_sensor smoke.test_world smoke.test_geoconversion
```
整个脚本会依次运行 [smoke_test_list.txt](https://github.com/OpenHUTB/doc/blob/master/src/test/smoke_test_list.txt) 文件中的所有测试用例。


测试失败：
```shell
smoke.test_spawnpoints.TestSpawnpoints
```


```text
ERROR: test_spawn_points (smoke.test_spawnpoints.TestSpawnpoints)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\work\workspace\doc\src\test\smoke\test_spawnpoints.py", line 48, in test_spawn_points
    response = self.client.apply_batch_sync(batch, False)
RuntimeError: time-out of 120000ms while waiting for the simulator, make sure the simulator is ready and connected to localhost:2000

======================================================================
FAIL: test_load_all_maps (smoke.test_map.TestMap)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\work\workspace\doc\src\test\smoke\test_map.py", line 32, in test_load_all_maps
    self._check_map(m)
  File "D:\work\workspace\doc\src\test\smoke\test_map.py", line 37, in _check_map
    self.assertIsNotNone(waypoint)
AssertionError: unexpectedly None
```

## CI/CD

参考 [链接](https://www.cnblogs.com/dotnet261010/p/11495762.html) 进行软件的安装。

