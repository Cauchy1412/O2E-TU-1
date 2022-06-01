## 前端部署

拉取仓库后，安装依赖包并构建静态文件：

```bash
$ npm install
$ npm run build
$ npm install -g serve
```

创建 systemd 服务单元：

```ini
# /etc/systemd/system/ote-admin.service
[Unit]
Description=o2e admin server
After=network.target nss-lookup.target

[Service]
ExecStart=serve -l tcp://0.0.0.0:10516 /root/O2E-TU-1/admin/dist

[Install]
WantedBy=multi-user.target
```

加载并启动系统服务：


```shell
# systemctl daemon-reload
# systemd enable --now ote-admin.service
```

## 后端部署

拉取仓库后，创建虚拟环境并安装依赖包：

```bash
$ python -m venv venv
$ . venv/bin/activate
$ pip install -r requirements
$ pip install gunicorn
```

创建 systemd 服务单元：

```ini
# /etc/systemd/system/ote-backend.service
[Unit]
Description=o2e backend
After=network.target nss-lookup.target

[Service]
WorkingDirectory=/root/O2E-TU-1/backend
ExecStart=/root/venv/bin/gunicorn backend.wsgi -w 1 --bind=0.0.0.0:80 --timeout 300

[Install]
WantedBy=multi-user.target
```

加载并启动系统服务：


```shell
# systemctl daemon-reload
# systemd enable --now ote-backend.service
```
