# Installation and Usage

There are two options to install and use this tool. (a) As a program run by a local user or (b) installed as a dedicated
service

## A: Installation and usage for a local user

- Install system requirements
  ```shell
    sudo apt update && sudo apt full-upgrade
    sudo apt-get install xvfb python3 python3-pip
  ```
- Install chrome
  ```shell
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb
    rm google-chrome-stable_current_amd64.deb
  ```
- Install worker
  ```shell
    pip3 install sso-analysis-worker
  ```
- Run the program
  > Daemon mode: `sso-daemon --name <name>`  
  > Dedicated analysis: `sso-worker run_analysis -i <id> -t <token> (--dev-mode)`  
  > Local analysis run: `sso-worker run_analysis_local --local-run-sites <inputlist> --local-run-results <outputcsv> (--headless)`  
  > Login Path Detection `sso-worker login_path_detection -t <token> (--dev-mode) (-rr/-rb/-b <lower> <upper>)`  

## B: Installation as a dedicated service

### Automatic approach 

To install the analysis worker as a dedicated service an [installation script](./sso-worker-setup.sh) is provided by the
brain. You can run this with the following command
```shell
  curl -s https://sso-scanner-mgmt.it.hs-heilbronn.de/client/sso-worker-setup.sh | sudo bash
```

If you want to change the name or parameters (e.g. server host / port) of the worker afterwards, you can use the following commands and change it inside the systemd service
```shell
  sudo nano /etc/systemd/system/ssoworker.service && sudo systemctl daemon-reload && sudo systemctl start ssoworker
```

### Manual Approach

You can also install it manually by following the installation steps below:

The installation path for this instructions is `/opt/ssoworker/sso-analysis-tool/`. If you want to choose another path,
please change it in the commands

- Install system requirements
  ```shell
    sudo apt update && sudo apt full-upgrade
    sudo apt-get install xvfb python3 python3-pip
  ```
- Install chrome
  ```shell
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb
    rm google-chrome-stable_current_amd64.deb
  ```
- Create new user
  ```shell
    sudo useradd -m -d /var/ssoworker/ ssoworker
  ```
- Install worker
  ```shell
    sudo runuser -l ssoworker -c 'pip3 install sso-analysis-worker
  ```
- Create Log File
  ```shell
    sudo touch /var/log/ssoworker.log /var/log/ssoworker.err
  ```
- Change permissions
  ```shell
    sudo chown ssoworker:ssoworker /var/log/ssoworker.log /var/log/ssoworker.err
  ```
- Create service file with the following content (be sure to change the path to the tool if neccessary and `<name>` at
  ExecStart)
  ```commandline
    sudo nano /etc/systemd/system/ssoworker.service
  ```
  ```ini
    [Unit]
    Description=SSO Worker for scanning sso supported websites
    After=network.target
    StartLimitIntervalSec=0
  
    [Service]
    Environment=PYTHONUNBUFFERED=1
    Type=simple
    User=sso-worker
    ExecStart=/var/ssoworker/.local/bin/sso-daemon --name <name>
    StandardOutput=append:/var/log/sso-worker.log
    StandardError=append:/var/log/sso-worker.err
    KillSignal=SIGINT
  
    [Install]
    WantedBy=multi-user.target
    ```
- Reload services and run service
  ```shell
    sudo systemctl daemon-reload && sudo systemctl start ssoworker.service
  ```
- Enable service at startup
  ```shell
    sudo systemctl enable ssoworker.service
  ```

### Update new version at PyPi

1. Change version number in `ssoanalysisworker/__version__.py`
2. Build release
   ```shell
    python3 setup.py sdist
   ```
3. Upload release
   ```shell
    twine upload dist/sso-analysis-worker-x.x.x.tar.gz
   ```
4. Build brain with maven to distribute new version
   ```shell
    mvn clean package -Pproduction -Prelease -Pdc
   ```
5. Deploy new brain to production server
6. Update all clients
   ```
    sudo runuser -l ssoworker -c 'pip3 install sso-analysis-worker -U' && sudo systemctl restart ssoworker
   ``` 
