# enviroment Setup on Linux


<https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server>



```bash

sudo apt-get install python3.8
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y python3.8-venv
```

```bash
python3 -m venv deep_racer_env
source deep_racer_env/bin/activate
```



```bash

pip3 install -r requirements.txt

```