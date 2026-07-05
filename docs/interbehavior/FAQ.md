# 常见问题

DReyeVR 安装和使用的大多数问题都列在这里。如果这份文档不是最新的，请查看我们的 [GitHub 问题](https://github.com/OpenHUTB/hutb/issues) 页面，如果你遇到新的问题，可以创建一个新问题。

***

## 什么是自车和自车传感器？

我们使用 [自车](../tuto_G_retrieve_data.md#set-the-ego-vehicle) 的概念来区分 AI 控制的车辆和玩家驾驶的车辆。当你第一次启动 VRD 时，你会在世界中生成一辆车，这就是自我车辆。

Like [Carla](https://carla.readthedocs.io/en/0.9.13/tuto_G_retrieve_data/#set-the-ego-vehicle), we use the notion of "ego-vehicle" to differentiate the AI-controlled vehicles from the player-driven vehicle. When you first start DReyeVR, you spawn in the world in a vehicle, this is the [`EgoVehicle`](https://github.com/HARPLab/DReyeVR/blob/main/DReyeVR/EgoVehicle.cpp). 

In addition to the EgoVehicle, we use a "DReyeVR-sensor" which we call the [`EgoSensor`](https://github.com/HARPLab/DReyeVR/blob/main/DReyeVR/EgoSensor.cpp) that inherits from a [Carla sensor](https://carla.readthedocs.io/en/0.9.13/ref_sensors/) but with features specific for DReyeVR. Our Ego-sensor tracks data such as user-inputs (keyboard/mouse/steering wheel), VR HMD orientation and location (6 dof), first-person camera frame captures, and of course the eye-tracker sensor. The underlying data structures used throughout the EgoSensor are defined in [DReyeVRData.h](https://github.com/HARPLab/DReyeVR/blob/main/Carla/Sensor/DReyeVRData.h), specifically in `struct DReyeVR::AggregateData`.

TL;DR: The **EgoVehicle** is the player-controlled vehicle, the **EgoSensor** is a sensor that contains all the core DReyeVR data we care about tracking in real time. 

***



## What CARLA features are working in DReyeVR?

<details>
<summary> Show answer </summary>

Since the DReyeVR `EgoVehicle` inherits from an [`ACarlaWheeledVehicle`](https://github.com/carla-simulator/carla/blob/master/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vehicle/CarlaWheeledVehicle.h), most of the standard CARLA vehicle features work out of the box. We needed to modify the recorder/replayer so all features of our `EgoSensor` are accurately recorder/replayed (such as HMD location/rotation, eye tracker data, user inputs, etc.). 

However, main assumption used throughout DReyeVR is that that there is **only ever one EgoVehicle in the world at a time**. This is because each EgoVehicle will compete for the VR HMD system, eye tracker, and is a highly expensive Actor (eg. real-time mirrors). Therefore, we do not permit spawning new EgoVehicle actors from the PythonAPI, if you want to access the EgoVehicle, we built a mechanism for you to do so with [DReyeVR_utils.py](https://github.com/HARPLab/DReyeVR/blob/main/PythonAPI/DReyeVR_utils.py) as follows:

```python
from DReyeVR_utils import find_ego_vehicle
...

world = client.get_world()
...

DReyeVR_vehicle = find_ego_vehicle(world)
```

Summary of supported CARLA features.

| Feature | Supported? | Notes |
| --- | --- | --- |
| Keyboard manual control | :heavy_check_mark: | |
| Wheel manual control | :heavy_check_mark: | |
| World record/replay | :heavy_check_mark: | |
| EgoSensor record/replay | :heavy_check_mark: | Specific for DReyeVR |
| EgoSensor PythonAPI streaming | :heavy_check_mark: | Specific for DReyeVR |
| Switching maps at runtime | :heavy_check_mark: | |
| Changing weather | :heavy_check_mark: | |
| Spawning EgoVehicle | :x: | Supposed to be already-spawned in map. Persistence. |
| Destroying EgoVehicle | :x: | Supposed to always be alive in map. Persistence. |
| EgoVehicle Carla AI Autopilot | :heavy_check_mark: | |
| ScenarioRunner `--route` | :heavy_check_mark: | The way we've been using ScenarioRunner so far |
| ScenarioRunner `--scenario` | :x: | Not implemented yet |
| ScenarioRunner `--agent` | :x: | Not implemented yet |


***
</details>

## What PythonAPI scripts have been tested with DReyeVR?

<details>
<summary> Show answer </summary>

The following `PythonAPI` scripts have been tested and should work with DReyeVR:

(:heavy_check_mark: = YES, :white_check_mark: = sort of, :grey_question: = Unsure, :x: = NO)

| Script | Supported? | Notes |
| --- | --- | --- |
| `DReyeVR_AI.py` | :heavy_check_mark: | Example with the DReyeVR autopilot |
| `DReyeVR_logging.py` | :heavy_check_mark: | Log the DReyeVR EgoSensor data in real time |
| `schematic_mode.py` | :heavy_check_mark: | Like `no_rendering_mode.py` but with EyeTracker visualization |
| `schematic_mode.py` | :heavy_check_mark: | Like `no_rendering_mode.py` but with EyeTracker visualization |
| `scenario_runner.py --route` | :heavy_check_mark: | |
| `scenario_runner.py --scenario` | :x: | Not implemented |
| `scenario_runner.py --agent` | :x: | Not implemented |
| `show_recorder_collisions.py` | :heavy_check_mark: | |
| `show_recorder_file_info.py` | :heavy_check_mark: | |
| `start_recording.py` | :heavy_check_mark: | |
| `start_replaying.py` | :heavy_check_mark: | |
| `dynamic_weather.py` | :heavy_check_mark: | |
| `no_rendering_mode.py` | :white_check_mark: | should instead use `schematic_mode.py` which is our DReyeVR wrapper around `no_rendering_mode.py` |
| `show_recorder_actors_blocked.py` | :white_check_mark: | |
| `automatic_control.py` | :x: | Use `DReyeVR_AI.py` |
| `client_bounding_boxes.py` | :grey_question: | |
| `draw_skeleton.py` | :grey_question: | |
| `generate_traffic.py` | :grey_question: | |
| `lidar_to_camera.py` | :grey_question: | |
| `manual_control.py` | :x: | should never need this, manual control is done through the server |
| `manual_control_carsim.py` | :x: | |
| `manual_control_chrono.py` | :x: | |
| `manual_control_steeringwheel.py` | :x: | |
| `open3d_lidar.py` | :grey_question: | |
| `sensor_synchronization.py` | :grey_question: | |
| `synchronous_mode.py` | :grey_question: | |
| `tutorial.py` | :x: | Spawns another EgoVehicle |
| `vehicle_gallery.py` | :x: | |
| `vehicle_physics.py` | :grey_question: | |
| `visualize_multiple_sensors.py` | :grey_question: | |


***
</details>

## How do I change the ego-vehicle mesh?

<details>
<summary> Show answer </summary>

Currently we use the `BP_TeslaM3` mesh provided by Carla for our EgoVehicle because the mesh has highly detailed internals and has good proportions for our use case. 

However there is no reason for the EgoVehicle to *have* to be a Tesla, in fact it does not even need to be a Car, it could be a (motor)cyclist, firetruck, or other Actor inheriting from `ACarlaWheeledVehicle`. 

We do not currently have updated documentation for changing the EgoVehicle mesh, but it should be fairly self-explanatory from [some earlier guides](https://github.com/GustavoSilvera/VR-Carla-Docs/blob/main/VRPlayer.md) where we first designed the EgoVehicle and decided on a mesh. Since the `AEgoVehicle` is a blueprint class in CPP, any Carla blueprint can be fitted to reparent this class and inherit all its functionality. 

However, you will need to modify some soft-coded defaults that we tuned for our particular mesh. For instance, the locations of the driver's seat head position, steering wheel, dashboard, mirrors, etc. will all be relative to your mesh, so you will need to adjust these accordingly. 

**NOTE:** Unlike those earlier tutorials, don't worry about adding the UCameraComponent to the Blueprint, since this is handled with the `DReyeVR_Pawn`. 

***

</details>

## How do I change the DReyeVR files once installed?

<details>
<summary> Show answer </summary>

Once DReyeVR is installed (see [`make install`](https://github.com/HARPLab/DReyeVR/tree/main/Scripts#make-install)), it lives in your CARLA directory as source files that work nicely with CARLA & UE4. 

You can find where the files in this DReyeVR repo are placed in the CARLA repo by reading our [correspondences files](https://github.com/HARPLab/DReyeVR/tree/main/Scripts/Paths).

For example, if I wanted to edit the `EgoVehicle.cpp` file, I would do so in `/PATH/TO/CARLA/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoVehicle.cpp`. Ignore any intermediate or generated files as those are effectively cached and will be regenerated. 

This is the same procedure for any files, including the DReyeVR [params](https://github.com/HARPLab/DReyeVR/blob/main/Configs/DReyeVRConfig.ini), PythonAPI files, ScenarioRunner, etc.

Another option is simply to modify all the DReyeVR files in the DReyeVR repo itself, then run `make install` again to overwrite the old files.

***

</details>


## Having problems with logitech hardware...

<details>
<summary> Show answer </summary>

First, you should verify that your logitech racing hardware is supported by the [LogitechWheelPlugin](https://github.com/HARPLab/LogitechWheelPlugin) we use (Supported devices denoted in the README). 

Now that you've verified you have supposedly compatible hardware, we recommend using the [Logitech G Hub](https://www.logitechg.com/en-us/innovation/g-hub.html) and ensuring your hardware is detected by the OS.

If your hardware is doing something wrong when in DReyeVR (or seemingly nothing at all) then try enabling the Logitech-verbose-logging mode in the UE4 editor by modifying the param `LogUpdates` to `True` (in the `[Hardware]` section of the [config file](https://github.com/HARPLab/DReyeVR/blob/main/Configs/DReyeVRConfig.ini)).

With this verbose-logging enabled, run `make launch` again to open Carla in the UE4-editor. Open `Window -> Developer Tools -> Output Log` to see all the logs from the level. Run the level and ensure one of these strings are printed:
```
# is detected
Found a Logitech device (XYZ) connected on input 0

# not detected
Could not find Logitech device connected on input 0
```

You should also read the logs which now will print on every tick whether or not it detects a state change such as a button press, axis rotation, or pedal depression. If those are still detected but the system is not responding, make an issue and let us know :)

***

</details>

## `ModuleNotFoundError: No module named 'DReyeVR_utils'`

<details>
<summary> Show answer </summary>

This happens when running DReyeVR-specific `PythonAPI` scripts and your Python install can't find [`DReyeVR_utils.py`](https://github.com/HARPLab/DReyeVR/blob/main/PythonAPI/DReyeVR_utils.py)

We can fix this by adding `PythonAPI/examples` to the PYTHONPATH as follows:

```bash
# on Linux/MacOS
export CARLA_ROOT=/PATH/TO/carla/
export SCENARIO_RUNNER_ROOT=/PATH/TO/scenario_runner/
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg                                           
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/agents
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/examples # <-- make sure examples is present
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI

# on Windows x64 Visual C++ Toolset
set CARLA_ROOT=C:PATH\TO\carla\
set SCENARIO_RUNNER_ROOT=C:PATH\TO\scenario_runner\
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\carla\dist\carla-0.9.13-py3.7-win-amd64.egg
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\carla\agents
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\examples # <-- make sure examples is present
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\carla
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI
```

Note that adding these paths to the PYTHONPATH might be different if you're using `conda`. If so, check out [`Install.md#using-conda-for-pythonapi`](https://github.com/HARPLab/DReyeVR/blob/main/Docs/Install.md#optionalusing-conda-for-the-pythonapi).

Related issue(s): [#16](https://github.com/HARPLab/DReyeVR/issues/16)

***

</details>

## `make: *** No rule to make target 'install'.  Stop.`

<details>
<summary> Show answer </summary>

This is likely the case if you are running `make install` from inside the `Carla` directory. 

The `make install` command is only defined when invoked from the `DReyeVR` directory. 

Related issue(s): [#7](https://github.com/HARPLab/DReyeVR/issues/7).

***

</details>

## `Assertion failed: px != 0, file shared_ptr.hpp`

<details>
<summary> Show answer </summary>

This might show up when you are running a `PythonAPI` script after installing DReyeVR if you haven't re-run the `make PythonAPI` command.

After installing DReyeVR to Carla, you also need to rebuild the PythonAPI (which also rebuilds LibCarla) for all the DReyeVR-PythonAPI compatibility to work.

```bash
# after installing DReyeVR to carla
cd /PATH/TO/DReyeVR
make install CARLA=/PATH/TO/CARLA SR=/PATH/TO/SR

# now back in Carla, need to rebuild both PythonAPI & CarlaUE4
make PythonAPI && make launch
```

Related issues(s): [#12](https://github.com/HARPLab/DReyeVR/issues/12)  

***

</details>

## `error: invalid command 'bdist_wheel'`

<details>
<summary> Show answer </summary>

This occurs when you are building PythonAPI and the output contains:

```
error: invalid command 'bdist_wheel'

-[BuildPythonAPI]: Carla lib for python has been successfully installed in "..."!
```

Although the log `[BuildPythonAPI]` says "successfuly installed", this is a (carla) bug and the installation actually failed as described with `error` above. You should make sure no error messages have occured in your build log.

(Thanks to [@SteadyBits](https://github.com/SteadyBits) for the answer!) You should ensure `wheel` is installed via `pip install wheel`. You can check the `PYTHONPATH` to see if the `wheel` package is installed. 

Then rebuilding the PythonAPI (`make PythonAPI`) should succeed without the `error: invalid command` message.

Related issue(s): [#19](https://github.com/HARPLab/DReyeVR/issues/19#issuecomment-1118695739)

***
</details>
