# awd-frame
ctf awd framework,没有啥牛逼的功能，只是简单的将比赛过程中手动的工作半自动化，省的比赛的时候手忙脚乱，毁了思路。

## 使用
`python awd-frame.py`

## 实现功能
* 批量登陆ssh，修改ssh密码/执行ssh命令
* 实现半自动化批量攻击，需要指定payload,以及一句话木马
* 通过webshell在同目录下种植指定的木马，xnianq.txt中为内存马。
* 获取到的flag进行提交

由于每次比赛的主办方采用的配置不太相同，所以在提交flag这一模块没有实现的很好，不过还能凑合用.:)
半自动化攻击时，可以使用GET/POST两种方法进行提交payload。

## 依赖
`pip install -r Requirement.txt `
