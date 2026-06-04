# 物理引擎


权衡：要么慢但硬（PhyX），要么快但软。

每个仿真步要解决的问题大致是:「这一瞬间，所有接触力、约束力、摩擦力应该是多少，才能满足物理定律？」如果按硬约束路线，这是个非凸的、棘手的 LCP 问题。MuJoCo 的高明之处，是通过把「硬接触」放松成「软接触」，把这个本来非凸的问题重新包装成了一个凸优化问题——变成了一个干净漂亮的碗，每一步都保证能滚到碗底。代价就是接触会显得软一点。


## Mujoco

软约束：把接触动力学硬塞进凸优化的框架里，将狰狞的物理约束统一表达为凸优化问题，这种设计带来了卓越的数值稳定性。

Mujoco 不准仅仅指的接触偏软。在接触刚度之外的几乎所有维度上，MuJoCo 反而是公认顶尖的：多关节刚体动力学算得非常精确，能量、动量守恒守得很好，积分稳定性强、长时间仿真不易漂移。相比之下，PhysX 在整体误差和**积分漂移**（和能量守恒）上往往更大。

## PhysX

硬约束。

PhysX 5.0 支持有限元（FEM）模型

UE4 使用 [PhysX 3.3](https://github.com/NVIDIAGameWorks/PhysX-3.4)

[UE5.0中禁用 Chaos 并使用 PhysX](https://github.com/MarkJGx/UnrealEngine/pull/1)

TODO: 支持 PhysX 5.1 GPU 的 UE4。



## Chaos

[此 PR](https://github.com/carla-simulator/carla/pull/8141) 更新了 VehiclePhysicsControl 相关代码，以反映从 PhysX 到 Chaos 的切换。


## 参考

* [UE4 Chaos基础使用及物理说明](https://zhuanlan.zhihu.com/p/506607859)

* [Jolt physics integration (Plugin) for Unreal Engine 5 (UE5)](https://github.com/Yadhu-S/UnrealJolt)

* [MuJoCo 和 PhyX 对比](https://zhuanlan.zhihu.com/p/2041670864731648529)

* [UE4 物理系统的调试](https://zhuanlan.zhihu.com/p/647129953)