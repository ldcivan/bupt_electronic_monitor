# bupt_electronic_monitor
基于python的北京邮电大学宿舍电费监控程序

# 因开发者已毕业，无法继续获取有效token来继续开发，本项目基本失效，谢谢一直以来的支持。

## 用法
elec_id_get用来获取宿舍id号。将id与要发送的邮箱以`[{"dromNumber": 100000000000, "mailto": "1234567890@mail.com"}, ...]`的格式置于同级文件夹中的data.json后运行elec_monitor即可。

缺少依赖请自行安装。不需要mysql储存可以注释掉相关内容。

## 备用方式（Proxy）
使用代理，代理通道及方式来自[ProxyPool](https://github.com/jhao104/proxy_pool)的demo，请不要滥用

## Demo
懒得搭建monitor的同学，您可以登录 https://pro-ivan.com/api/elec_monitor/index.php 获取说明并使用监控功能。
