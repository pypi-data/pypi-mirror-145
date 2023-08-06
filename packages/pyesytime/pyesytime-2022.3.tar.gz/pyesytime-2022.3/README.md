## PyesyTime

### A module to make time easier	一个让时间更好获取的模块

#### Notice:The lastest version is 2022.3	注意：最新版本2022.3

##### 0. Name	名称

Pyesytime

python easy time

##### 1.Download	下载

pip install pyesytime==2022.3

##### 2. Import Package	导入

import pyesytime

##### 3.What‘s New	更新内容

​	(1) You can enter a parameter in ONLY_HOUR_12_ENGLISH and ONLY_HOUR_12_CHINESE

​		 你可以在 ONLY_HOUR_12_ENGLISH 和 ONLY_HOUR_12_CHINESE中输入参数

​	(2) More functions have been added, as detailed below

​		 添加了更多函数，详情请见下方 

##### 4. Function	函数

​	(1) ALL_IN_ONE()

​		Return all the time like this:  2022-01-01 00:00:00

​		像这样显示所有时间：2022-01-01 00:00:00

​	(2)YEAR_MONTH_DAY_LINE()

​		Return the time like this: 2022-01-01

​		像这样显示所有时间：2022-01-01

​	(3)YEAR_MONTH_DAY_DIAGONAL()

​		Return the time like this: 2022/01/01

​		像这样显示所有时间：2022/01/01

​	(4)HOUR_MINUTE_SECOND_24_COLON()

​		Return the time like this: 13:00:00

​		像这样显示所有时间：13:00:00

​	(5)HOUR_MINUTE_SECOND_12_COLON_ENGLISH()

​		Return the time like this: 1:00:00 pm

​		像这样显示所有时间：1:00:00 pm

​	(6)HOUR_MINUTE_SECOND_12_COLON_ENGLISH()

​		Return the time like this: 下午 1:00:00

​		像这样显示所有时间：下午 1:00:00

​	(7)ONLY_HOUR_24()

​		Return the time like this: 13

​		像这样显示所有时间：13

​	(8)ONLY_HOUR_12_ENGLISH(hour)					（NEW!）

​		Return the time like this: 1 pm

​		像这样显示所有时间：1 pm

​		You can enter a time and change it into this.

​		你可以写入一个数字参数让函数来转换显示形式

​	(9)ONLY_HOUR_12_CHINESE(hour)					（NEW!）

​		Return the time like this: 下午1时

​		像这样显示所有时间：下午1时

​		You can enter a time and change it into this.

​		你可以写入一个数字参数让函数来转换显示形式

​	(10)ISO_STANDARD_CALENDAR_AS_TUPLE()					（NEW!）

​		Return the tuple of time as ISO standard calendar: (2022, 1, 1)

​		像这样以元组类型显示ISO标准日历时间：(2022, 1, 1)

​	(11)ISO_STANDARD_CALENDAR_AS_LIST()					（NEW!）

​		Return the list of time as ISO standard calendar: [2022, 1, 1]

​		像这样以列表类型显示ISO标准日历时间：[2022, 1, 1]

​	(12)NOW_WEEKDAY_ENGLISH()					（NEW!）

​		Return the weekday as English like this: Monday

​		像这样用英文返回今天的星期：Monday
