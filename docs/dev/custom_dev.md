
# 自定义开发

- [__同步 ue4_dev 分支__](#sync_ue4_dev)
- [__合并某个提交__](#cherry_pick)
- [__冲突解决__](#apply_reject)
- [__Beyond Compare对比相同文件仍显示红色__](#same_red)
- [__获取某一行代码相关的所有提交记录__](#git_blame)
- [__其他__](#others)
- [__参考__](#references)



## 同步 [ue4_dev 分支](https://github.com/carla-simulator/carla/commits/ue4-dev/)  <span id="sync_ue4_dev"></span>

1.在需要合并 [提交](https://github.com/carla-simulator/carla/commit/cf17eb576e866404eabac0c93af3558da0d91be3) 的地址栏中页面地址后添加`.patch`，下载对应提交的补丁。

2.检查patch是否能正常打入:
```shell
git apply --check 【path/to/xxx.patch】
```

3.如果检查能够正常打入（第2步没有任何输出），则执行：
```shell
git apply 【path/to/xxx.patch】
```
如果有冲突则按行进行合并。


## 合并某个提交  <span id="cherry_pick"></span>

```shell
git checkout sync
git log --oneline -3
# 记下最左侧的提交{commit_id}
git checkout hutb
# 从sync分支摘取提交到hutb分支
git cherry-pick {commit_id}
```


## 冲突解决 <span id="apply_reject"></span>

[open3d_lidar.py](../../../carla/PythonAPI/examples/open3d_lidar.py)
强制打补丁
```shell
git apply --reject xxx.patch
```
加入这个选项能够将能打上的补丁先打上，冲突的文件生成*.rej文件


注意：如果强行打补丁后，文件内容修改了，但是git没跟踪到修改记录，则需要启用稀疏检出（允许检出仓库中需要的部分内容）：
```shell
git config core.sparsecheckout true
```

## Beyond Compare对比相同文件仍显示红色 <span id="same_red"></span>

解决：[Beyond Compare对比相同文件仍显示红色怎么办](https://www.beyondcompare.cc/wenti/xianshi-hongse.html)




## 保存到Gitlab
```shell
git remote add xj http://172.20.46.154:8090/traffic/carla.git
git push xj
```

报错：`remote: GitLab: LFS objects are missing. Ensure LFS is properly set up or try a manual "git lfs push --all".`

> 原因：GitLab启用了大文件。
> 
> 解决：在gitlab项目设置中禁用Git大型文件存储(LFS)。
> 
> 设置>通用>可见性、项目特性、权限>展开> Git大型文件存储(LFS)

报错：
```shell
Uploading LFS objects:   0% (0/1), 0 B | 0 B/s, done.
batch response: Repository or object not found: http://172.20.46.154:8090/traffic/carla.git/info/lfs/objects/batch
Check that it exists and that you have proper access to it
error: failed to push some refs to 'http://172.20.46.154:8090/traffic/carla.git'
```
> 原因：可能其他分支包含大文件
> 
> 解决：只推送当前分支
> ```shell
> git push xj -u OpenHUTB
> # 推送到github
> git push origin OpenHUTB:OpenHUTB
> ```

## 同步bitbucket资产

1.打开对应修改的资产

2.打开页面右边`...`中的`Open in Source`

3.在新页面中的`...`中打开`Open raw`

4.下载并覆盖本地的文件


## 使用dev分支开发

### 删除dev分支

```shell
:: 位于dev分支，切换到其他分支
git checkout hutb
:: 删除dev分支
git branch -d dev
:: 删除远程分支
git push origin --delete dev
git push hutb --delete dev
:: 更新最新的修改
git pull origin hutb:hutb --rebase
git push hutb
:: 新建dev分支
git checkout -b dev
git push hutb
```

## 获取某一行代码相关的所有提交记录 <span id="git_blame"></span>

通过网页的 `git blame` 操作来完成：

1.在网页中选中某一行代码左侧的行号的左边，会出现三个点的下拉菜单；

2.选中下拉菜单中的`View git blame`，比如[虚幻引擎的ImportAssetsInternal这一行的提交历史](https://github.com/EpicGames/UnrealEngine/blame/release/Engine/Source/Developer/AssetTools/Private/AssetTools.cpp#L2980)，在弹出的页面中搜索`ImportAssetsInternal`，大致可以定位到想查看的[历史](https://github.com/EpicGames/UnrealEngine/commit/9e1786b97b3e986a4034cf5d3aeeeeb0cd028fb4)。


## 其他 <span id="others"></span>

##### [获取公众号的主页链接](https://www.zhihu.com/question/51987041/answer/3059575358)

1. 复制文章的链接，在电脑端浏览器打开。

2. 查看网页源代码。在浏览器打开文章之后，鼠标右键单击，并选择【查看页面源代码】。

3. 查找Biz 值：在页面源代码界面，按住ctrl+F 快捷键，搜索Biz, 找到如下的位置，并复制图中这个双引号里面的信息： MzI2ODk5MzE5Ng==

4. 将前面复制的Biz 值，放入下面这个链接里面正确的位置就好了。

万能公式：
```shell
https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=替换biz的值&scene=124#wechat_redirect
```

所以获得的 OpenHUTB 公众号链接就是：
```shell
https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI2ODk5MzE5Ng==&scene=124#wechat_redirect
```

5. 在微信中打开公众号链接（注意不能在电脑浏览器中打开）。



##### [修改commit的记录](https://blog.csdn.net/zi__li/article/details/106604872)
如果要只是要修改上一次commit的信息，如果是用TortoiseGit，在Commit界面选择Amend Last Commit即可修改。

##### 使用旧仓库存放新的提交记录
> 1.删除所有文件
> 
> 2.复制新的仓库文件到旧仓库（包括.git文件夹）
> 
> 3.修改.git/config文件，指向旧仓库的地址

##### 补充

[持续集成](cicd.md)



## 参考  <span id="references"></span>

[git 生成补丁文件及打补丁](https://blog.csdn.net/xiewenhao12/article/details/117923288)



