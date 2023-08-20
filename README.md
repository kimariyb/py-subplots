# pySubplots

pySubplots 是 Kimariyb 开发的一款绘制多子图的开源 Python 脚本。主要使用了 Python 中的 Matplotlib 和 Proplot 库。

## 安装

**推荐！** 我们推荐使用 **_anaconda_** 虚拟环境进行安装，方便对包进行管理，同时也不会影响其他项目的环境。

如果没有安装 Python，可以不用安装 Python，直接前往 anaconda 官网下载 anaconda 最新版本。安装并配置好以后，使用 anaconda 新建一个环境。

```shell
conda create -n subplots python=3.8.13
```

激活名为 kimaridraw 的 conda 环境：

```shell
conda activate subplots
```

使用 pip 工具安装 pySubplots

```shell
pip install pysubplots
```

同时需要安装 pySubplots 运行所依靠的包和模块

```shell
pip install pandas==1.4.3 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install numpy==1.23.5 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install proplot==0.9.5 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install matplotlib==3.4.3 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install toml==0.10.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install wxpython==4.2.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install openpyxl==3.1.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用

**请注意：在正式运行前，请确保已经安装了 pySubplots 所需要的模块和包，以免程序报错！**

运行 pySubplots 需要准备一个 toml 文件以及 Multiwfn 或者其他程序生成的记载 x、y 数据的 txt 文件或者 xlsx 文件。

```toml
[[file]]
# Multiwfn 输出的 txt 文件路径
path = "CH3CHO.txt"
# 绘制曲线颜色，可以为一个字符串，也可以是一个保存字符串的 list 集合
colors = "pink9"
# 绘制曲线风格，可以为一个字符串，也可以是一个保存字符串的 list 集合，也可以是一个元组集合
styles = "-"
# 图例的文本，可以为一个字符串，也可以是一个保存字符串的 list 集合
legend = "Acetaldehyde"
# x 轴的最小值、最大值以及间距，必须是一个三个 float 值组成的 list 集合
xlim = [0, 4000, 500]
# y 轴的最小值、最大值以及间距，必须是一个三个 float 值组成的 list 集合
ylim = [0, 3000, 1000]
# x 轴的标签，必须是一个字符串
xlabel = "Frequency (in cm^-1)"
# y 轴的标签，必须是一个字符串
ylabel = "Absorption (in L/mol/cm)"
# 标题，必须是一个字符串
title = ""
# 是否开启 zero 轴，可以选择 0 False；1 True
iszero = 0
# 是否显示图例，可以选择 0 False；1 True
islegend = 1

[[file]]
# Multiwfn 输出的 txt 文件路径
path = "CH3CO2CH3.txt"
# 绘制曲线颜色，可以为一个字符串，也可以是一个保存字符串的 list 集合
colors = "blue9"
# 绘制曲线风格，可以为一个字符串，也可以是一个保存字符串的 list 集合，也可以是一个元组集合
styles = "-"
# 图例的文本，可以为一个字符串，也可以是一个保存字符串的 list 集合
legend = "Methyl acetate"
# x 轴的最小值、最大值以及间距，必须是一个三个 float 值组成的 list 集合
xlim = [0, 4000, 500]
# y 轴的最小值、最大值以及间距，必须是一个三个 float 值组成的 list 集合
ylim = [0, 3000, 1000]
# x 轴的标签，必须是一个字符串
xlabel = "Frequency (in cm^-1)"
# y 轴的标签，必须是一个字符串
ylabel = "Absorption (in L/mol/cm)"
# 标题，必须是一个字符串
title = ""
# 是否开启 zero 轴，可以选择 0 False；1 True
iszero = 0
# 是否显示图例，可以选择 0 False；1 True
islegend = 1

[[file]]
# Multiwfn 输出的 txt 文件路径
path = "CH3COCH3.txt"
# 绘制曲线颜色，可以为一个字符串，也可以是一个保存字符串的 list 集合
colors = "teal9"
# 绘制曲线风格，可以为一个字符串，也可以是一个保存字符串的 list 集合，也可以是一个元组集合
styles = "-"
# 图例的文本，可以为一个字符串，也可以是一个保存字符串的 list 集合
legend = "Acetone"
# x 轴的最小值、最大值以及间距，必须是一个三个 float 值组成的 list 集合
xlim = [0, 4000, 500]
# y 轴的最小值、最大值以及间距，必须是一个三个 float 值组成的 list 集合
ylim = [0, 3000, 1000]
# x 轴的标签，必须是一个字符串
xlabel = "Frequency (in cm^-1)"
# y 轴的标签，必须是一个字符串
ylabel = "Absorption (in L/mol/cm)"
# 标题，必须是一个字符串
title = ""
# 是否开启 zero 轴，可以选择 0 False；1 True
iszero = 0
# 是否显示图例，可以选择 0 False；1 True
islegend = 1

[[file]]
# Multiwfn 输出的 txt 文件路径
path = "CH3CONHCH3.txt"
# 绘制曲线颜色，可以为一个字符串，也可以是一个保存字符串的 list 集合
colors = "grape9"
# 绘制曲线风格，可以为一个字符串，也可以是一个保存字符串的 list 集合，也可以是一个元组集合
styles = "-"
# 图例的文本，可以为一个字符串，也可以是一个保存字符串的 list 集合
legend = "N-Methylacetamide"
# x 轴的最小值、最大值以及间距，必须是一个三个 float 值组成的 list 集合
xlim = [0, 4000, 500]
# y 轴的最小值、最大值以及间距，必须是一个三个 float 值组成的 list 集合
ylim = [0, 3000, 1000]
# x 轴的标签，必须是一个字符串
xlabel = "Frequency (in cm^-1)"
# y 轴的标签，必须是一个字符串
ylabel = "Absorption (in L/mol/cm)"
# 标题，必须是一个字符串
title = ""
# 是否开启 zero 轴，可以选择 0 False；1 True
iszero = 0
# 是否显示图例，可以选择 0 False；1 True
islegend = 1
```

如果使用 pip 安装了 pySubplots，可以直接在终端中运行 pySubplots

```shell
pysub
```

接着程序显示程序头以及提示你要你选择一个 toml 文件，所有的指令和提示非常清晰，比如输入 q 可以直接退出，按空格可以使用 GUI 选择 toml 文件。

```shell
pySubplots -- A python script for plotting multiple subplots.
Version: v1.0.0, release date: Aug-21-2023
Developer: Kimariyb, Ryan Hsiun
Address: XiaMen University, School of Electronic Science and Engineering
KimariDraw home website: https://github.com/kimariyb/py-subplots

(Copyright 2023 Kimariyb. Currently timeline: Aug-21-2023, 00:45:21)

Input toml file path, for example E:\Hello\World.toml
Hint: Press ENTER button directly can select file in a GUI window. If you want to exit the program, simply type the letter "q" and press Enter. 
```

输入 toml 文件之后就可以进入主程序页面，接着可以输入命令，每一个命令的含义都在屏幕上显示的非常清楚。假如想直接看看默认的绘图效果，可以输入 0。当然大部分情况下，默认的设置都不太可能满足用户的需求，这时候可以输入其他命令修改绘图的设置。最后可以使用命令 1 保存图片。

```shell
 "q": Exit program gracefully    "r": Load a new file
********************************************************
****************** Main function menu ******************
********************************************************
-4 Set figure layout of subplots, current: auto
-3 Showing the serial of subplots, current: True
-2 Set whether to share axis ticks , current: True
-1 Set whether to share axis labels, current: True
0 Plot spectrum! But the effect of direct drawing is very poor, please save directly!
1 Save graphical file of the spectrum in current folder
2 Set font family of the spectrum, current: Arial
3 Set font size of the spectrum, current: [10.5, 12, 14]
4 Set figure size of spectrum file, current: auto
5 Set format of saving spectrum file, current: png
6 Set dpi of saving spectrum, current: 300
```

假如想要修改多子图的排版可以输入 `-4 Set figure layout of subplots`，这里我们选择输入 `4,1`。

接着选择 `4 Set figure size of spectrum file`，输入 `6,6`。

最后直接输入 `1 Save graphical file of the spectrum in current folder`。就可以在当前文件夹下找到一个名为 `figure.png` 的文件。

<img src="figure/figure.png">

## 许可证

pySubplots 基于 MIT 许可证开源。这意味着您可以自由地使用、修改和分发代码。


