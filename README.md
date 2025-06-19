Atlassian Agent Web - обёртка над atlassian agent, позволяющая получать ключи плагинов через веб-интерфейс. Сервис принимает код плагина, подставляет его в исполняемую команду, выполняет её на сервере и отображает полученный результат  

Установка:  
Создайте пользователя и поместите в нужные группы
```
sudo adduser atlassian_agent_web
sudo usermod -aG docker atlassian_agent_web
sudo su atlassian_agent_web
cd
```

Клонируйте репозиторий и установите зависимости  
```
git clone https://github.com/DorofD/atlassian_agent_web
mv atlassian_agent_web app && cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```  

Скопируйте настройки  
```cp settings.json.example settings.json```  
В файле settings.json в объект "exec_command" вставьте свою команду по типу:  
```/usr/bin/docker exec CONTAINER_NAME java -jar /var/agent/atlassian-agent.jar -d -p 'PLUGIN_CODE' -m test@test.test -n test@test.test -o some_company -s XXXX-XXXX-XXXX-XXXX```  
При исполнении команды подстрока PLUGIN_CODE в ней автоматически изменяется на введённый через веб-интерфейс код плагина. Поэтому команда исполнения может быть любой, важно только наличие подстроки PLUGIN_CODE  


Создайте службу, скорректируйте необходимые настройки (например, порт или пользователя) на своё усмотрение  
```
sudo nano /etc/systemd/system/atlassian_agent_web.service

[Unit]
Description=Atlassian Agent Web
After=network.target docker.service
Requires=docker.service

[Service]
User=atlassian_agent_web
Group=docker
WorkingDirectory=/home/atlassian_agent_web/app
ExecStart=/home/atlassian_agent_web/app/venv/bin/python /home/atlassian_agent_web/app/run.py --port 8085
Environment="PATH=/home/atlassian_agent_web/app/venv/bin"
Restart=always

[Install]
WantedBy=multi-user.target
```

Запустите и проверьте состояние службы  
```
sudo systemctl daemon-reload
sudo systemctl enable atlassian_agent_web.service
sudo systemctl start atlassian_agent_web.service
sudo systemctl status atlassian_agent_web.service
```

При корректном запуске веб-интерфейс будет доступен по http://<адрес вашего сервера>:8085   
Сервис может быть доступен на другом порту, если вы изменили его в аргументах запуска
