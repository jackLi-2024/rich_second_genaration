Linux环境（linux_enviroment）：
	step1	.环境安装：
		命令行执行以下命令：
			pip install -r requirements.txt  (安装Python环境包)
			deploy --docker-install  (安装docker)
			deploy --docker-start     (启动docker服务)
	step2	.启动浏览器：
		命令行执行以下命令：
			docker pull selenium/standalone-chrome  (拉取官方浏览器镜像)
			docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome  (注意这里的第一个4444是端口号，后面会用到)

	step3 	.修改配置文件：
		命令行执行以下命令：
			vim conf/nike_conf.txt   ----->  保存(:wq)

			work_num: 1   // 进程数
			regist_num: 1  // 需要注册的用户数
			browser_type: Remote-Chrome   // 使用Chrome远程浏览器
			executable_path: http://167.179.97.68:4444/wd/hub  // 微浏览器的地址，4444与上面一致

			[user]   //  这里面的参数是用户信息文件，根据需要改动

			product: ["https://www.nike.com/cn/launch/t/air-max-98-white-teal/"]   // 修改为你要抢购的鞋的链接，可以给多个
			size: ["39"]	  // 这里修改为你需要的鞋码，可以给多个

			[address]   //  这里是修改配送地址，注意地址一定要存在，否则无法修改
			firstname: li
			lastname: jiacai
			province: 黑龙江省
			city: 绥化市
			district: 安达市
			addressinfo: 详细地址
			phone: 18404983790

			[email]    // 这里是检查排队成功与否，即看订单，排队成功与否都将返回信息
			email_smtpserver: smtp.qq.com
			email_port: 465
			email_sender: 546501664@qq.com    //  修改你的邮箱
			email_password: agixaxvdxwupbcjb
			email_receiver: ["1050518702@qq.com"]    //  发送目的邮箱
			email_subject: SNKRS订单

	step4	.抢购等
		命令行执行以下命令：
			cd linux_run
			sh nike_buy.sh  (抢购)
			sh nike_address.sh  (运行修改地址)
			sh nike_order.sh    (检查订单)
			sh nike_register.sh (注册nike用户)

		最终结果按文件类型保存在data/nike/目录下



Windows环境：
        (百度网盘下载enviroment_package   链接：https://pan.baidu.com/s/1Eq7f0QjSMI_LPAkC4eMsUA 提取码：ud7p)
	step1	.环境安装：
		命令行执行以下命令：
			1.下载Miniconda2.7对用系统版本，并安装，注意需要加入环境变量
			2.pip install -r requirements.txt  (安装Python环境包)

	step2 	.安装Chrome浏览器驱动
			1.用户自己安装Chrome浏览器
			2.将enviroment_package下的chromedriver.exe拷贝到Miniconda2.7目录下，想详细教程按word文档操作

	step3 	.修改配置文件：
		打开conf/nike_conf.txt   ----->  保存

			work_num: 1   // 进程数
			regist_num: 1  // 需要注册的用户数
			browser_type: Chrome   // 使用Chrome本地浏览器
			executable_path: None  // 微浏览器的地址，4444与上面一致

			[user]   //  这里面的参数是用户信息文件，根据需要改动

			product: ["https://www.nike.com/cn/launch/t/air-max-98-white-teal/"]   // 修改为你要抢购的鞋的链接，可以给多个
			size: ["39"]	  // 这里修改为你需要的鞋码，可以给多个

			[address]   //  这里是修改配送地址，注意地址一定要存在，否则无法修改
			firstname: li
			lastname: jiacai
			province: 黑龙江省
			city: 绥化市
			district: 安达市
			addressinfo: 详细地址
			phone: 18404983790

			[email]    // 这里是检查排队成功与否，即看订单，排队成功与否都将返回信息
			email_smtpserver: smtp.qq.com
			email_port: 465
			email_sender: 546501664@qq.com    //  修改你的邮箱
			email_password: agixaxvdxwupbcjb
			email_receiver: ["1050518702@qq.com"]    //  发送目的邮箱
			email_subject: SNKRS订单

	step4	.抢购等
			进入windows_run
			点击 nike_buy.bat  (抢购)
			点击 nike_address.bat  (运行修改地址)
			点击 nike_order.bat    (检查订单)
			点击 nike_register.bat (注册nike用户)

		最终结果按文件类型保存在data/nike/目录下



