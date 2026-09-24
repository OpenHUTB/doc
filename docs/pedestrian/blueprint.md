## 行人的实现分析

## 调用过程

使用 [manual_control.py](https://github.com/OpenHUTB/hutb/blob/3cc9770572f1b531f0eed69a5dc3e0e4f186a876/PythonAPI/examples/manual_control.py#L257) 生成行人：
```python
self.world.try_spawn_actor()(blueprint, spawn_point)
```

[hutb/PythonAPI/carla/source/libcarla/World.cpp](https://github.com/OpenHUTB/hutb/blob/3cc9770572f1b531f0eed69a5dc3e0e4f186a876/PythonAPI/carla/source/libcarla/World.cpp#L331) 中定义了 try_spawn_action() 调用 TrySpawnActor。

```cpp
.def("try_spawn_actor", SPAWN_ACTOR_WITHOUT_GIL(TrySpawnActor))
```

___

然后调用 **LibCarla**/source/carla/client/World.cpp 的 [TrySpawnActor()](https://github.com/OpenHUTB/hutb/blob/3cc9770572f1b531f0eed69a5dc3e0e4f186a876/LibCarla/source/carla/client/World.cpp#L136) ：
```cpp
SharedPtr<Actor> World::TrySpawnActor(
    ...
    return SpawnActor(blueprint, transform, parent_actor, attachment_type, socket_name);
    ...
}
```
然后调用 World.cpp 的 [SpawnActor()](https://github.com/OpenHUTB/hutb/blob/3cc9770572f1b531f0eed69a5dc3e0e4f186a876/LibCarla/source/carla/client/World.cpp#L127) ：
```cpp
SharedPtr<Actor> World::SpawnActor(
  ...
  return _episode.Lock()->SpawnActor(blueprint, transform, parent_actor, attachment_type, GarbageCollectionPolicy::Inherit, socket_name);
}
```
调用了 client/detail/EpisodeProxy.cpp 的 Lock()，返回 EpisodeProxyImpl
```cpp
template <typename T>
typename EpisodeProxyImpl<T>::SharedPtrType EpisodeProxyImpl<T>::Lock() const {
  auto ptr = Load(_simulator);
  if (ptr == nullptr) {
    throw_exception(std::runtime_error(
        "trying to operate on a destroyed actor; an actor's function "
        "was called, but the actor is already destroyed."));
  }
  return ptr;
}
```
获得模拟器 _simulator 的指针。并调用 client/detail/Simulator.cpp 的 SpawnActor() 
```cpp
SharedPtr<Actor> Simulator::SpawnActor(
  const ActorBlueprint &blueprint,
  const geom::Transform &transform,
  Actor *parent,
  rpc::AttachmentType attachment_type,
  GarbageCollectionPolicy gc,
  const std::string& socket_name) {
        rpc::Actor actor;
        if (parent != nullptr) {
          actor = _client.SpawnActorWithParent(
              blueprint.MakeActorDescription(),
              transform,
              parent->GetId(),
              attachment_type,
              socket_name);
        } else {
          actor = _client.SpawnActor(
              blueprint.MakeActorDescription(),
              transform);
        }
        ...
```


___

调用 **CarlaUE4** Server 模块的 [CarlaServer.cpp](https://github.com/OpenHUTB/hutb/blob/3cc9770572f1b531f0eed69a5dc3e0e4f186a876/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Server/CarlaServer.cpp#L731) 的：
```cpp
BIND_SYNC(spawn_actor) << [this](
    cr::ActorDescription Description,
    const cr::Transform &Transform) -> R<cr::Actor>
{
  REQUIRE_CARLA_EPISODE();

  auto Result = Episode->SpawnActorWithInfo(Transform, std::move(Description));
  ...
```


调用 Game 模块的 CarlaEpisode.h 中的 [SpawnActor()](https://github.com/OpenHUTB/hutb/blob/3cc9770572f1b531f0eed69a5dc3e0e4f186a876/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/CarlaEpisode.h#L235) ：
```cpp
UFUNCTION(BlueprintCallable)
AActor *SpawnActor(
    const FTransform &Transform,
    FActorDescription ActorDescription)
{
  return SpawnActorWithInfo(Transform, std::move(ActorDescription)).Value->GetActor();
}
```

调用 CarlaEpisode.cpp 中的 [SpawnActorWithInfo()](https://github.com/OpenHUTB/hutb/blob/3cc9770572f1b531f0eed69a5dc3e0e4f186a876/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/CarlaEpisode.cpp#L464) ：
```cpp
TPair<EActorSpawnResultStatus, FCarlaActor*> UCarlaEpisode::SpawnActorWithInfo(
    const FTransform &Transform,
    FActorDescription thisActorDescription,
    FCarlaActor::IdType DesiredId)
{
  ...
  auto result = ActorDispatcher->SpawnActor(LocalTransform, thisActorDescription, DesiredId);
```

ActorDispatcher 的声明位于 CarlaEpisode.h
```cpp
UPROPERTY(VisibleAnywhere)
UActorDispatcher *ActorDispatcher = nullptr;
```




## 行人蓝图

所有行人相关的蓝图都位于虚幻编辑器`内容浏览器`中的`内容/Carla/Blueprints/Walkers/`目录下。
每个蓝图都是一个**胶囊体组件(CollisionCylinder)** ，即一个 [圆柱碰撞几何体](https://ww2.mathworks.cn/help/nav/ref/collisioncylinder.html) ，该集合体与其固定身体框架的 z 轴对齐，并且固定身体框架的原点位于圆柱体的中心。

