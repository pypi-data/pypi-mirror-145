# StarWorldCoreLib3
> 一个简单的数据处理模块<br>
>当前版本：1.7.1

例示代码
```python
import StarWorldCoreLib as sw
rstr = sw.rstring("HelloWorld")
print(sw.string(rstr.reverse()))
#输出 "dlroWolleH"
print(sw.string(rstr.upset()))
#输出 "HelloWorld" 打乱后的文字
#如 edWrolHlol
```

StarWorldCoreLib.rstring 介绍
> 用法：rstring("文本") -> rstring<br>
> 动作：<br>
>>reverse函数 reverse() -> rstring：用来反转rstring内容<br>
>>upset函数 upset() -> rstring：用来打乱rstring内容<br>
>>replace函数 replace(rstring("需要替换的文本"),rstring("替换后的文本")) -> rstring：用来替换rstring的内容<br>
>>split函数 split(rstring("分割的文本")) -> list：用来把rstring文本按参数分割成列表<br>
>>toString函数与下面StarWorldCoreLib.string函数相同

StarWorldCoreLib.rclipboard 介绍
> 用法：rclipboard() -> rclipboard<br>
> 动作：<br>
>> read函数 read() -> rstring：读取粘贴板的rstring类型
>> write函数 write(rstring("写入到粘贴板的内容")) -> rstring：写入内容到粘贴板


StarWorldCoreLib.string 介绍
> 用法：string(rstring("一个rstring内容")) -> str<br>
> 介绍：将rstring内容转换为str内容

更多内容请自己研究