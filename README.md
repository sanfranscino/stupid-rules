规则怪谈 Galgame
一个用 Python Tkinter 制作的规则怪谈视觉小说小游戏。

玩家会在荒诞的校园规则中做出选择：顺从规则，或者坚持自己的判断。游戏包含怒气值系统、多段剧情推进、普通结局和特殊剧情结局。

游戏特色
视觉小说式剧情推进
9 个校园规则场景
双选项分支
怒气值系统
普通结局与特殊剧情结局
支持自定义背景图和人物立绘
运行方式
先确认电脑已经安装 Python 3。

在 PowerShell 或命令行中运行：

python rule_galgame.py
如果你的电脑使用 py 启动 Python，也可以运行：

py rule_galgame.py
素材放置
游戏会自动读取 assets 文件夹中的图片素材：

assets/
  background.png
  character.png
其中：

background.png 是教室背景图
character.png 是人物立绘图
也支持 .jpg、.jpeg、.webp、.gif 格式。只要文件名是 background 或 character，游戏就会自动加载。

推荐项目结构
rule-galgame/
  rule_galgame.py
  README.md
  assets/
    background.png
    character.png
依赖
游戏主体使用 Python 标准库中的 Tkinter。

如果安装了 Pillow，游戏会使用 Pillow 对图片进行更好的缩放；如果没有安装，也可以使用 Tkinter 支持的图片格式运行。

安装 Pillow：

pip install pillow
说明
这个项目目前是一个单文件小游戏，适合继续扩展：

增加更多角色立绘
给不同场景设置不同背景
添加背景音乐和音效
增加存档/读档功能
把剧情文本拆分到独立文件中
License
本项目仅供学习和个人创作使用。素材版权请根据实际来源自行确认。
