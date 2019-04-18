1.安装物理环境(安装文档及安装说明)
    	miniconda2.7  ---> python环境
	Chrome        ---> 浏览器
	driver	      ---> 浏览器驱动器

	链接：https://pan.baidu.com/s/1ivQXGjUwV1EDxFrlnmKfCg 
提取码：aici 


2.安装三方库
	pip install -r requirements.txt

3.修改配置文件（nike.conf）

	[user]  用户信息读取文本路径
	[url] product  需要抢购鞋的链接，可以给多个
	[size]  鞋码数，可以给多个
	[address]  自动配送地址
	[regist]   注册信息的名和姓
	[email]   邮件信息，主要更改发送者和接受者


4.根据需要点击运行脚本
	windows_run 下面

	例如：点击  nike_buy.bat 文件，即开启抢购


注意：
	conf/下面含有一个用户信息文件，里面存入了账号密码信息，用于登录