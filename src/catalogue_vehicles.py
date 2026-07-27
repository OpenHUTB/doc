import carla

client = carla.Client('localhost', 2000)
world = client.get_world()
bp_lib = world.get_blueprint_library()
spectator = world.get_spectator()

vehicles = world.get_actors().filter('vehicle.*')
# 删除所有车辆
for vehicle in vehicles:
    vehicle.destroy()

# 获取所有支持的车辆蓝图
vehicle_blueprints = bp_lib.filter('vehicle.*')
print("Supported vehicle blueprints:")
for blueprint in vehicle_blueprints:
    print(blueprint)

# ActorBlueprint(id=vehicle.bydsong-1.bydsong-1,tags=[vehicle, bydsong-1])
# ActorBlueprint(id=vehicle.mini-3.mini-3,tags=[vehicle, mini-3])
# ActorBlueprint(id=vehicle.byd.seal,tags=[vehicle, byd, seal])
# ActorBlueprint(id=vehicle.kawasaki.ninja,tags=[vehicle, kawasaki, ninja])
# ActorBlueprint(id=vehicle.audi.a2,tags=[vehicle, audi, a2])
# ActorBlueprint(id=vehicle.nissan.micra,tags=[vehicle, nissan, micra])
# ActorBlueprint(id=vehicle.su7.su7,tags=[vehicle, su7])
# ActorBlueprint(id=vehicle.audi.tt,tags=[vehicle, audi, tt])
# ActorBlueprint(id=vehicle.mercedes.coupe_2020,tags=[vehicle, mercedes, coupe_2020])
# ActorBlueprint(id=vehicle.bmw.grandtourer,tags=[vehicle, bmw, grandtourer])
# ActorBlueprint(id=vehicle.harley-davidson.low_rider,tags=[vehicle, harley-davidson, low_rider])
# ActorBlueprint(id=vehicle.ford.ambulance,tags=[vehicle, ford, ambulance])
# ActorBlueprint(id=vehicle.carlamotors.firetruck,tags=[vehicle, carlamotors, firetruck])
# ActorBlueprint(id=vehicle.micro.microlino,tags=[vehicle, micro, microlino])
# ActorBlueprint(id=vehicle.carlamotors.carlacola,tags=[vehicle, carlamotors, carlacola])
# ActorBlueprint(id=vehicle.carlamotors.european_hgv,tags=[vehicle, carlamotors, european_hgv])
# ActorBlueprint(id=vehicle.ford.mustang,tags=[vehicle, ford, mustang])
# ActorBlueprint(id=vehicle.chevrolet.impala,tags=[vehicle, chevrolet, impala])
# ActorBlueprint(id=vehicle.lincoln.mkz_2020,tags=[vehicle, lincoln, mkz_2020])
# ActorBlueprint(id=vehicle.lixiang-1.lixiang-1,tags=[vehicle, lixiang-1])
# ActorBlueprint(id=vehicle.citroen.c3,tags=[vehicle, citroen, c3])
# ActorBlueprint(id=vehicle.dodge.charger_police,tags=[vehicle, dodge, charger_police])
# ActorBlueprint(id=vehicle.nissan.patrol,tags=[vehicle, nissan, patrol])
# ActorBlueprint(id=vehicle.jeep.wrangler_rubicon,tags=[vehicle, jeep, wrangler_rubicon])
# ActorBlueprint(id=vehicle.mini.cooper_s,tags=[vehicle, mini, cooper_s])
# ActorBlueprint(id=vehicle.mercedes.coupe,tags=[vehicle, mercedes, coupe])
# ActorBlueprint(id=vehicle.dodge.charger_2020,tags=[vehicle, dodge, charger_2020])
# ActorBlueprint(id=vehicle.ford.crown,tags=[vehicle, ford, crown])
# ActorBlueprint(id=vehicle.seat.leon,tags=[vehicle, seat, leon])
# ActorBlueprint(id=vehicle.toyota.prius,tags=[vehicle, toyota, prius])
# ActorBlueprint(id=vehicle.yamaha.yzf,tags=[vehicle, yamaha, yzf])
# ActorBlueprint(id=vehicle.xiaopeng-1.xiaopeng-1,tags=[vehicle, xiaopeng-1])
# ActorBlueprint(id=vehicle.bh.crossbike,tags=[vehicle, bh, crossbike])
# ActorBlueprint(id=vehicle.mitsubishi.fusorosa,tags=[vehicle, mitsubishi, fusorosa])
# ActorBlueprint(id=vehicle.tesla.model3,tags=[vehicle, tesla, model3])
# ActorBlueprint(id=vehicle.gazelle.omafiets,tags=[vehicle, gazelle, omafiets])
# ActorBlueprint(id=vehicle.tesla.cybertruck,tags=[vehicle, tesla, cybertruck])
# ActorBlueprint(id=vehicle.diamondback.century,tags=[vehicle, century, diamondback])
# ActorBlueprint(id=vehicle.mercedes.sprinter,tags=[vehicle, mercedes, sprinter])
# ActorBlueprint(id=vehicle.audi.etron,tags=[vehicle, audi, etron])
# ActorBlueprint(id=vehicle.volkswagen.t2,tags=[vehicle, volkswagen, t2])
# ActorBlueprint(id=vehicle.lincoln.mkz_2017,tags=[vehicle, lincoln, mkz_2017])
# ActorBlueprint(id=vehicle.dodge.charger_police_2020,tags=[vehicle, dodge, charger_police_2020])
# ActorBlueprint(id=vehicle.vespa.zx125,tags=[vehicle, zx125, vespa])
# ActorBlueprint(id=vehicle.mini.cooper_s_2021,tags=[vehicle, mini, cooper_s_2021])
# ActorBlueprint(id=vehicle.nissan.patrol_2021,tags=[vehicle, patrol_2021, nissan])
# ActorBlueprint(id=vehicle.volkswagen.t2_2021,tags=[vehicle, t2_2021, volkswagen])
# ActorBlueprint(id=vehicle.wj.wj,tags=[vehicle, wj])
# ActorBlueprint(id=vehicle.hongqi-2.hongqi-2,tags=[vehicle, hongqi-2])
# ActorBlueprint(id=vehicle.byd_bus.byd_bus,tags=[vehicle, byd_bus])
# ActorBlueprint(id=vehicle.mini-4.mini-4,tags=[vehicle, mini-4])
# ActorBlueprint(id=vehicle.hongqi-1.hongqi-1,tags=[vehicle, hongqi-1])
# ActorBlueprint(id=vehicle.wuling-1.wuling-1,tags=[vehicle, wuling-1])
# ActorBlueprint(id=vehicle.wuling-2.wuling-2,tags=[vehicle, wuling-2])

# 设置车辆变换
vehicle_loc = carla.Location(x=-46.9, y=20.0, z=0.2)
vehicle_rot = carla.Rotation(pitch=0.0, yaw=142.0, roll=0.0)
vehicle_trans = carla.Transform(vehicle_loc,vehicle_rot)

# 在这里粘贴蓝图 ID
# vehicle_bp = bp_lib.find('vehicle.lincoln.mkz_2020')
# 国产车
# vehicle.bydsong-1.bydsong-1
# vehicle.mini-3.mini-3
# vehicle.byd.seal
# vehicle.su7.su7
# vehicle.lixiang-1.lixiang-1
# vehicle.xiaopeng-1.xiaopeng-1
# vehicle.wj.wj
# vehicle.hongqi-2.hongqi-2
# vehicle.byd_bus.byd_bus
# vehicle.mini-4.mini-4
# vehicle.hongqi-1.hongqi-1
# vehicle.wuling-1.wuling-1
# vehicle.wuling-2.wuling-2
vehicle_bp = bp_lib.find('vehicle.wuling-2.wuling-2')
# print(vehicle_bp)


# 设置视角变换
camera_loc = carla.Location(x=-48.7, y=24.8, z=1.7)
camera_rot = carla.Rotation(pitch=-13.4, yaw=-75.7, roll=0.0)
camera_trans = carla.Transform(camera_loc,camera_rot)

# 生成车辆
vehicle = world.spawn_actor(vehicle_bp, vehicle_trans)

# 移动观察者
spectator.set_transform(camera_trans)


# vehicle.destroy()
print("end")

