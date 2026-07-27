<!--- 

The images in this document were captured using the following settings in Carla:

Town: Town 10

Vehicle location: Transform(Location(x=-46.885479, y=20.083447, z=-0.002633), Rotation(pitch=-0.000034, yaw=141.974243, roll=0.000000))

Camera location, small vehicles: Transform(Location(x=-47.696186, y=24.049326, z=1.471929), Rotation(pitch=-10.843717, yaw=-77.215683, roll=0.000139))
Camera location, standard vehicles: Transform(Location(x=-48.672256, y=24.830288, z=1.722733), Rotation(pitch=-13.396630, yaw=-75.692039, roll=0.000119))
Camera location, large vehicles: Transform(Location(x=-49.470921, y=27.835310, z=2.931721), Rotation(pitch=-13.396630, yaw=-75.691978, roll=0.000119))

The weather settings are: 

weather.sun_altitude_angle = 50
weather.sun_azimuth_angle = 260
weather.wetness = 10
weather.precipitation = 10
weather.scattering_intensity = 5
weather.mie_scattering_scale = 0.5
weather.rayleigh_scattering_scale = 0.1

Camera settings:

camera_bp = bp_lib.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '1920')
camera_bp.set_attribute('image_size_y', '1080')
camera_bp.set_attribute('fstop', '6.0')

Vehicle settings:

control = vehicle.get_control()
control.steer = -0.25
vehicle.apply_control(control)

--->

# 车辆目录

## 第 2 代

* __车__
	* [__道奇__ - Charger 2020](#dodge-charger-2020)
	* [__道奇__ - Police Charger 2020](#dodge-police-charger-2020)
	* [__福特__ - 皇冠（出租车）](#ford-crown-taxi)
	* [__林肯__ - MKZ 2020](#lincoln-mkz-2020)
	* [__梅赛德斯__ - Coupe 2020](#mercedes-coupe-2020)
	* [__迷你__ - Cooper S 2021](#mini-cooper-s-2021)
	* [__尼桑__ - Patrol 2021](#nissan-patrol-2021)
* __卡车__
	* [__Carla Motors__ - 欧洲 HGV（驾驶室位于发动机上方）](#carla-motors-european-hgv-cab-over-engine-type)
	* [__Carla Motors__ - 消防车](#carla-motors-firetruck)
	* [__特斯拉__ - Cybertruck](#tesla-cybertruck)
* __面包车__
	* [__福特__ - 救护车](#ford-ambulance)
	* [__梅赛德斯__ - Sprinter](#mercedes-sprinter)
	* [__大众__ - T2 2021](#volkswagen-t2-2021)
* __巴士__
	* [__三菱__ - Fusorosa](#mitsubishi-fusorosa)


## 第一代

* __车__
	* [__奥迪__ - A2](#audi-a2)
	* [__奥迪__ - E-Tron](#audi-e-tron)
	* [__奥迪__ - TT](#audi-tt)
	* [__宝马__ - 多功能旅行车](#bmw-gran-tourer)
	* [__雪佛兰__ - Impala](#chevrolet-impala)
	* [__雪铁龙__ - C3](#citroen-c3)
	* [__道奇__ - Police Charger](#dodge-police-charger)
	* [__福特__ - Mustang](#ford-mustang)
	* [__吉普车__ - Wrangler Rubicon](#jeep-wrangler-rubicon)
	* [__林肯__ - MKZ 2017](#lincoln-mkz-2017)
	* [__梅赛德斯__ - Coupe](#mercedes-coupe)
	* [__微型车__ - Microlino](#micro-microlino)
	* [__迷你__ - Cooper S](#mini-cooper-s)
	* [__尼桑__ - Micra](#nissan-micra)
	* [__尼桑__ - Patrol](#nissan-patrol)
	* [__Seat__ - Leon](#seat-leon)
	* [__特斯拉__ - Model 3](#tesla-model-3)
	* [__Toyota__ - Prius](#toyota-prius)
* __卡车__
	* [__Carla Motors__ - CarlaCola](#carla-motors-carlacola)
* __面包车__
	* [__大众__ - T2](#volkswagen-t2)
* __摩托车__
	* [__哈雷戴维森__ - Low Rider](#harley-davidson-low-rider)
	* [__Kawasaki__ - Ninja](#kawasaki-ninja)
	* [__Vespa__ - ZX 125](#vespa-zx-125)
	* [__Yamaha__ - YZF](#yamaha-yzf)
* __自行车__
	* [__BH__ - 越野自行车](#bh-crossbike)
	* [__大名自行车__ - Century](#diamondback-century)
	* [__Gazelle__ - Omafiets](#gazelle-omafiets)


---

## 检查模拟器中的车辆

要检查目录中的车辆，请使用以下代码，从下面的车辆详细信息中检索蓝图 ID 并将其粘贴到行中`bp_lib.find('blueprint.id.goes_here')`：

```py
client = carla.Client('localhost', 2000)
world = client.get_world()
bp_lib = world.get_blueprint_library()
spectator = world.get_spectator()

# 设置车辆变换
vehicle_loc = carla.Location(x=-46.9, y=20.0, z=0.2)
vehicle_rot = carla.Rotation(pitch=0.0, yaw=142.0, roll=0.0)
vehicle_trans = carla.Transform(vehicle_loc,vehicle_rot)

# 在这里粘贴蓝图 ID
vehicle_bp = bp_lib.find('vehicle.lincoln.mkz_2020') 

# 设置视角变换
camera_loc = carla.Location(x=-48.7, y=24.8, z=1.7)
camera_rot = carla.Rotation(pitch=-13.4, yaw=-75.7, roll=0.0)
camera_trans = carla.Transform(camera_loc,camera_rot)

# 生成车辆
vehicle = world.spawn_actor(vehicle_bp, vehicle_trans)

# 移动观察者
spectator.set_transform(camera_trans)
```

在尝试生成另一辆车之前，不要忘记销毁该车辆以避免碰撞：

```py
vehicle.destroy()
```

---

## 车

### mini-3

![audi_a2](./img/catalogue/vehicles/vehicle.mini-3.mini-3.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mini-3.mini-3<span>

* __基本类型__: 小汽车


### 小米 su7

![audi_a2](./img/catalogue/vehicles/vehicle.su7.su7.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.su7.su7<span>

* __基本类型__: 小汽车

### 比亚迪大巴

![audi_a2](./img/catalogue/vehicles/vehicle.byd_bus.byd_bus.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.byd_bus.byd_bus<span>

### mini-4

![audi_a2](./img/catalogue/vehicles/vehicle.mini-4.mini-4.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mini-4.mini-4<span>




### 比亚迪宋

![audi_a2](./img/catalogue/vehicles/vehicle.bydsong-1.bydsong-1.jpg)

* __制造商__: 比亚迪
* __型号__: 宋
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.bydsong-1.bydsong-1<span>

* __基本类型__: 小汽车


### 比亚迪海豹

![audi_a2](./img/catalogue/vehicles/vehicle.byd.seal.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mini-3.mini-3<span>

* __基本类型__: 小汽车


### 理想

![audi_a2](./img/catalogue/vehicles/vehicle.lixiang-1.lixiang-1.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.lixiang-1.lixiang-1<span>

* __基本类型__: 小汽车


<!-- 
### 小鹏

![audi_a2](./img/catalogue/vehicles/vehicle.xiaopeng-1.xiaopeng-1.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.xiaopeng-1.xiaopeng-1<span>

* __基本类型__: 小汽车

-->

<!-- 
### 红旗

![audi_a2](./img/catalogue/vehicles/vehicle.hongqi-2.hongqi-2.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.hongqi-2.hongqi-2<span>

* __基本类型__: 小汽车

-->


<!-- 
### 红旗1

![audi_a2](./img/catalogue/vehicles/vehicle.hongqi-1.hongqi-1.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.hongqi-1.hongqi-1<span>

* __基本类型__: 小汽车

-->

### wj

![audi_a2](./img/catalogue/vehicles/vehicle.wj.wj.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.wj.wj<span>

* __基本类型__: 小汽车


### wuling-1

![audi_a2](./img/catalogue/vehicles/vehicle.wuling-1.wuling-1.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.wuling-1.wuling-1<span>

* __基本类型__: 小汽车


<!-- 
### vehicle.wuling-2.wuling-2

![audi_a2](./img/catalogue/vehicles/vehicle.wuling-2.wuling-2.jpg)

* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.wuling-2.wuling-2<span>

* __基本类型__: 小汽车

-->









### 奥迪 - A2

![audi_a2](./img/catalogue/vehicles/audi_a2.webp)


* __制造商__: 奥迪
* __型号__: A2
* __类别__: 紧凑型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.audi.a2<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 奥迪 - E-Tron

![audi_etron](./img/catalogue/vehicles/audi_etron.webp)


* __制造商__: 奥迪
* __型号__: E-Tron
* __类别__: SUV
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.audi.etron<span>

* __基本类型__: 小汽车

* __特殊类型__: 电动

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 奥迪 - TT

![audi_tt](./img/catalogue/vehicles/audi_tt.webp)


* __制造商__: 奥迪
* __型号__: TT
* __类别__: 标准
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.audi.tt<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 宝马 - 多功能旅行车

![bmw_grandtourer](./img/catalogue/vehicles/bmw_grandtourer.webp)


* __制造商__: 宝马
* __型号__: 多功能旅行车
* __类别__: 紧凑型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.bmw.grandtourer<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 雪佛兰 - Impala

![chevrolet_impala](./img/catalogue/vehicles/chevrolet_impala.webp)


* __制造商__: 雪佛兰
* __型号__: Impala
* __类别__: 标准
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.chevrolet.impala<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 雪铁龙 - C3

![citroen_c3](./img/catalogue/vehicles/citroen_c3.webp)


* __制造商__: 雪铁龙
* __型号__: C3
* __类别__: 紧凑型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.citroen.c3<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 道奇 - Charger 2020

![dodge_charger_2020](./img/catalogue/vehicles/dodge_charger_2020.webp)


* __制造商__: 道奇
* __型号__: Charger 2020
* __类别__: 标准
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.dodge.charger_2020<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 道奇 - Police Charger

![dodge_charger_police](./img/catalogue/vehicles/dodge_charger_police.webp)


* __制造商__: 道奇
* __型号__: Police Charger
* __类别__: 标准
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.dodge.charger_police<span>

* __基本类型__: 小汽车

* __特殊类型__: 救险车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 道奇 - Police Charger 2020

![dodge_charger_police_2020](./img/catalogue/vehicles/dodge_charger_police_2020.webp)


* __制造商__: 道奇
* __型号__: Police Charger 2020
* __类别__: 标准
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.dodge.charger_police_2020<span>

* __基本类型__: 小汽车

* __特殊类型__: 救险车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 福特 - 皇冠（出租车）

![ford_crown](./img/catalogue/vehicles/ford_crown.webp)


* __制造商__: 福特
* __型号__: 皇冠（出租车）
* __类别__: 标准
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.ford.crown<span>

* __基本类型__: 小汽车

* __特殊类型__: taxi

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 福特 - Mustang

![ford_mustang](./img/catalogue/vehicles/ford_mustang.webp)


* __制造商__: 福特
* __型号__: Mustang
* __类别__: 标准
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.ford.mustang<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 吉普车 - Wrangler Rubicon

![jeep_wrangler_rubicon](./img/catalogue/vehicles/jeep_wrangler_rubicon.webp)


* __制造商__: 吉普车
* __型号__: Wrangler Rubicon
* __类别__: 紧凑型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.jeep.wrangler_rubicon<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 林肯 - MKZ 2017

![lincoln_mkz_2017](./img/catalogue/vehicles/lincoln_mkz_2017.webp)


* __制造商__: 林肯
* __型号__: MKZ 2017
* __类别__: 标准
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.lincoln.mkz_2017<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 林肯 - MKZ 2020

![lincoln_mkz_2020](./img/catalogue/vehicles/lincoln_mkz_2020.webp)


* __制造商__: 林肯
* __型号__: MKZ 2020
* __类别__: 标准
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.lincoln.mkz_2020<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 梅赛德斯 - Coupe

![mercedes_coupe](./img/catalogue/vehicles/mercedes_coupe.webp)


* __制造商__: 梅赛德斯
* __型号__: Coupe
* __类别__: 标准
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mercedes.coupe<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 梅赛德斯 - Coupe 2020

![mercedes_coupe_2020](./img/catalogue/vehicles/mercedes_coupe_2020.webp)


* __制造商__: 梅赛德斯
* __型号__: Coupe 2020
* __类别__: 标准
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mercedes.coupe_2020<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 微型车 - Microlino

![micro_microlino](./img/catalogue/vehicles/micro_microlino.webp)


* __制造商__: 微型车
* __型号__: Microlino
* __类别__: 微型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.micro.microlino<span>

* __基本类型__: 小汽车

* __特殊类型__: 电动

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 迷你 - Cooper S

![mini_cooper_s](./img/catalogue/vehicles/mini_cooper_s.webp)


* __制造商__: 迷你
* __型号__: Cooper S
* __类别__: 紧凑型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mini.cooper_s<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 迷你 - Cooper S 2021

![mini_cooper_s_2021](./img/catalogue/vehicles/mini_cooper_s_2021.webp)


* __制造商__: 迷你
* __型号__: Cooper S 2021
* __类别__: 标准
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mini.cooper_s_2021<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 尼桑 - Micra

![nissan_micra](./img/catalogue/vehicles/nissan_micra.webp)


* __制造商__: 尼桑
* __型号__: Micra
* __类别__: 紧凑型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.nissan.micra<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 尼桑 - Patrol

![nissan_patrol](./img/catalogue/vehicles/nissan_patrol.webp)


* __制造商__: 尼桑
* __型号__: Patrol
* __类别__: SUV
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.nissan.patrol<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 尼桑 - Patrol 2021

![nissan_patrol_2021](./img/catalogue/vehicles/nissan_patrol_2021.webp)


* __制造商__: 尼桑
* __型号__: Patrol 2021
* __类别__: SUV
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.nissan.patrol_2021<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### Seat - Leon

![seat_leon](./img/catalogue/vehicles/seat_leon.webp)


* __制造商__: Seat
* __型号__: Leon
* __类别__: 紧凑型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.seat.leon<span>

* __基本类型__: 小汽车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 特斯拉 - Model 3

![tesla_model3](./img/catalogue/vehicles/tesla_model3.webp)


* __制造商__: 特斯拉
* __型号__: Model 3
* __类别__: 标准
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.tesla.model3<span>

* __基本类型__: 小汽车

* __特殊类型__: 电动

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### Toyota - Prius

![toyota_prius](./img/catalogue/vehicles/toyota_prius.webp)


* __制造商__: Toyota
* __型号__: Prius
* __类别__: 紧凑型车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.toyota.prius<span>

* __基本类型__: 小汽车

* __特殊类型__: 电动

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

---

## 卡车
### Carla Motors - CarlaCola

![carlamotors_carlacola](./img/catalogue/vehicles/carlamotors_carlacola.webp)


* __制造商__: Carla Motors
* __型号__: CarlaCola
* __类别__: 卡车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.carlamotors.carlacola<span>

* __基本类型__: 卡车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### Carla Motors - 欧洲 HGV（驾驶室位于发动机上方）

![carlamotors_european_hgv](./img/catalogue/vehicles/carlamotors_european_hgv.webp)


* __制造商__: Carla Motors
* __型号__: 欧洲 HGV（驾驶室位于发动机上方）
* __类别__: 卡车
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.carlamotors.european_hgv<span>

* __基本类型__: 卡车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### Carla Motors - Firetruck

![carlamotors_firetruck](./img/catalogue/vehicles/carlamotors_firetruck.webp)


* __制造商__: Carla Motors
* __型号__: Firetruck
* __类别__: 卡车
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.carlamotors.firetruck<span>

* __基本类型__: 卡车

* __特殊类型__: 救险车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 特斯拉 - Cybertruck

![tesla_cybertruck](./img/catalogue/vehicles/tesla_cybertruck.webp)


* __制造商__: 特斯拉
* __型号__: Cybertruck
* __类别__: 卡车
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.tesla.cybertruck<span>

* __基本类型__: 卡车

* __特殊类型__: 电动

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

---

## 面包车
### 福特 - 救护车

![ford_ambulance](./img/catalogue/vehicles/ford_ambulance.webp)


* __制造商__: 福特
* __型号__: 救护车
* __类别__: 面包车
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.ford.ambulance<span>

* __基本类型__: 面包车

* __特殊类型__: 救险车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 梅赛德斯 - Sprinter

![mercedes_sprinter](./img/catalogue/vehicles/mercedes_sprinter.webp)


* __制造商__: 梅赛德斯
* __型号__: Sprinter
* __类别__: 面包车
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mercedes.sprinter<span>

* __基本类型__: 面包车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

### 大众 - T2

![volkswagen_t2](./img/catalogue/vehicles/volkswagen_t2.webp)


* __制造商__: 大众
* __型号__: T2
* __类别__: 标准
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.volkswagen.t2<span>

* __基本类型__: 面包车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 大众 - T2 2021

![volkswagen_t2_2021](./img/catalogue/vehicles/volkswagen_t2_2021.webp)


* __制造商__: 大众
* __型号__: T2 2021
* __类别__: 面包车
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.volkswagen.t2_2021<span>

* __基本类型__: 面包车

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#99c635;">True<span>

---

## 巴士
### 三菱 - Fusorosa

![mitsubishi_fusorosa](./img/catalogue/vehicles/mitsubishi_fusorosa.webp)


* __制造商__: 三菱
* __型号__: Fusorosa
* __类别__: 巴士
* __世代__: 2
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.mitsubishi.fusorosa<span>

* __基本类型__: 巴士

* __有灯__: <span style="color:#99c635;">True<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

---

## 摩托车
### 哈雷戴维森 - Low Rider

![harley-davidson_low_rider](./img/catalogue/vehicles/harley-davidson_low_rider.webp)


* __制造商__: 哈雷戴维森
* __型号__: Low Rider
* __类别__: 摩托车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.harley-davidson.low_rider<span>

* __基本类型__: 摩托车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### Kawasaki - Ninja

![kawasaki_ninja](./img/catalogue/vehicles/kawasaki_ninja.webp)


* __制造商__: Kawasaki
* __型号__: Ninja
* __类别__: 摩托车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.kawasaki.ninja<span>

* __基本类型__: 摩托车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### Vespa - ZX 125

![vespa_zx125](./img/catalogue/vehicles/vespa_zx125.webp)


* __制造商__: Vespa
* __型号__: ZX 125
* __类别__: 摩托车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.vespa.zx125<span>

* __基本类型__: 摩托车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### Yamaha - YZF

![yamaha_yzf](./img/catalogue/vehicles/yamaha_yzf.webp)


* __制造商__: Yamaha
* __型号__: YZF
* __类别__: 摩托车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.yamaha.yzf<span>

* __基本类型__: 摩托车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

---

## 自行车
### BH - 越野自行车

![bh_crossbike](./img/catalogue/vehicles/bh_crossbike.webp)


* __制造商__: BH
* __型号__: 越野自行车
* __类别__: 自行车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.bh.crossbike<span>

* __基本类型__: 自行车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### 大名自行车 - Century

![diamondback_century](./img/catalogue/vehicles/diamondback_century.webp)


* __制造商__: 大名自行车
* __型号__: Century
* __类别__: 自行车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.diamondback.century<span>

* __基本类型__: 自行车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

### Gazelle - Omafiets

![gazelle_omafiets](./img/catalogue/vehicles/gazelle_omafiets.webp)


* __制造商__: Gazelle
* __型号__: Omafiets
* __类别__: 自行车
* __世代__: 1
* __蓝图 ID__: <span style="color:#00a6ed;">vehicle.gazelle.omafiets<span>

* __基本类型__: 自行车

* __有灯__: <span style="color:#f16c6c;">False<span>

* __有打开的门__: <span style="color:#f16c6c;">False<span>

---

