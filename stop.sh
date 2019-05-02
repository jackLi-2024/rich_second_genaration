ps -ef|grep nike | awk '{print $2}' | xargs kill -9


ps -ef|grep run_login.py | awk '{print $2}' | xargs kill -9
ps -ef|grep run_address.py | awk '{print $2}' | xargs kill -9
ps -ef|grep run_order.py | awk '{print $2}' | xargs kill -9
ps -ef|grep run_register.py | awk '{print $2}' | xargs kill -9
ps -ef|grep run_buy.py | awk '{print $2}' | xargs kill -9
ps -ef|grep run_buy_and_order.py | awk '{print $2}' | xargs kill -9
ps -ef|grep buy_and_order | awk '{print $2}' | xargs kill -9

ps -ef|grep chrome | awk '{print $2}' | xargs kill -9
