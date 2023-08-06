# Install and Execution
There are two options to install this script. (a) As a program run by a local user and (b) installed as a dedicated service
### Generic Steps (needed for both installation methods)
- Install system requirements
  - `sudo apt update && sudo apt full-upgrade`
  - `sudo apt-get install xvfb python3 python3-pip`
- Install chrome
  - `wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`
  - `sudo dpkg -i google-chrome-stable_current_amd64.deb`
  - `sudo apt --fix-broken install`
  - `rm google-chrome-stable_current_amd64.deb`

### Install for a local user
- Move/Clone the tool into the users home folder
- Move into tool folder
  - `cd sso-analysis-tool`
- Install python requirements
  - `pip3 install .`
- Run the program
  - Daemon mode: `python3 AnalysisDaemon.py --name <name>`
  - Dedicated analysis: `python3 NGLoginAndSSOCollector run_analysis -i <id> -t <token> (--dev-mode)`
  - Local analysis run: `python3 NGLoginAndSSOCollector run_analysis_local --local-run-sites <inputlist> --local-run-results <outputcsv> (--headless)`
  - Login Path Detection `python3 NGLoginAndSSOCollector login_path_detection -t <token> (--dev-mode) (-rr/-rb/-b <lower> <upper>)`
  
### Install as a dedicated service
The installation path for this instructions is `/opt/ssoworker/sso-analysis-tool/`. If you want to choose another path, please change it in the commands
- Create new user 
  - `sudo useradd -m -d /opt/ssoworker/ sso-worker`
- Move/Clone tool into `/opt/ssoworker/`
  - V1: Create ssh access for pushing tool via scp 
    ```
    sudo mkdir /opt/ssoworker/.ssh && \
    sudo chmod 700 /opt/ssoworker/.ssh && \
    sudo touch /opt/ssoworker/.ssh/authorized_keys && \
    sudo chmod 600 /opt/ssoworker/.ssh/authorized_keys && \
    sudo chown -R sso-worker:sso-worker /opt/ssoworker/.ssh && \
    sudo nano /opt/ssoworker/.ssh/authorized_keys
    ```
- Install requirements for new user 
  - `sudo runuser -l sso-worker -c 'pip3 install -r /opt/ssoworker/sso-analysis-tool/requirements.txt'`
- Create Log File 
  - `sudo touch /var/log/sso-worker.log /var/log/sso-worker.err`
- Change permissions 
  - `sudo chown sso-worker:sso-worker /var/log/sso-worker.log /var/log/sso-worker.err`  
- Create service file with the following content (be sure to change the path to the tool if neccessary and `<name>` at ExecStart)
  - `sudo nano /etc/systemd/system/ssoworker.service`
    ```
    [Unit]
    Description=SSO Worker for scanning sso supported websites
    After=network.target
    StartLimitIntervalSec=0
  
    [Service]
    Environment=PYTHONUNBUFFERED=1
    Type=simple
    User=sso-worker
    ExecStart=/usr/bin/python3 /opt/ssoworker/sso-analysis-tool/AnalysisDaemon.py --name <name>
    StandardOutput=append:/var/log/sso-worker.log
    StandardError=append:/var/log/sso-worker.err
    KillSignal=SIGINT
  
    [Install]
    WantedBy=multi-user.target
    ```
- Reload services and run service
  - `sudo systemctl daemon-reload && sudo systemctl start ssoworker.service`
- Enable service at startup 
  - `sudo systemctl enable ssoworker.service`