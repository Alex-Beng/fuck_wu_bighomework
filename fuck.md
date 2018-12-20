# 思路
预计两分钟的 8h 延迟摄影视频

需 2400 左右张的图片。视频帧率 20 ，即需以 12s 为周期拍照片。

## 流程
### 过 wifi + adb 无线连接黑莓 priv 作为相机。
### 通过 adb 命令拍照，并删除图片，并传到电脑上。
### 通过 opencv 的 videocapture 拼接成视频

# 实现
### sdk.py 和 main.py 实现与流程分离
### in adk.py (做作业先不封装成类了...)
1. TakePhoto 用于执行拍照，
2. GetImgName 通过 ls + read 获得图片的名称，然后返回
3. GetImage 用于接受文件名读取手机的图片， pull 到本地，然后删除，并做异常处理 
4. ProcImage 用于 pull 下来的本地图片，并返回 
5. CheckStatus 检查 adb 连接状态，并尝试重连
6. SetIP 用于设置 device ip

### in main.py
工作流程，策略代码

----

## Update on 2018.12.09
1. 增加 main.py 工作流程的鲁棒性
2. 将 GetImgName 与 GetImage 合并，简化流程
3. 将保存图片到本地集成到 GetImage 中，减少 IO

----

## Update on 2018.13.20
1. 增加手动模式不并入 sdk.py, 独立成 image2video.py
2. image2video.py 中实现移动多个文件 & 通过日期获得相关图片