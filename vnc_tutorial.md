# Connnecting to VM using VNC Tutorial

This guide provides a concise and reliable method to connect to a virtual machine (VM) using VNC.
After reviewing multiple inconsistent tutorials, Team Shunya has compiled the exact steps required—without unnecessary details or ambiguity.

Follow the instructions below to establish a successful VNC connection to your VM.

- #### Note :  Server means VM , Host Machine means your System!!!!



- #### We will use tigervnc to access ( It's Best for ubuntu 22.04/24.04)

## Setup commands which you have to do on your VM (Server) !!

#### Start with downloading the xfec4 and related Packages

```bash
# Update & Upgrade the packages
sudo apt update sudo apt upgrade -y
# Install XFCE -- A light weight Desktop Environment 
sudo apt install xfce4 xfce4-goodies dbus-x11 xterm -y
```
```bash
# Install tigervnc sevrver
sudo apt install tigervnc-standalone-server tigervnc-common -y
sudo apt install tigervnc-tools
```
```bash
# Set a password for remote access
vncpasswd
```

 Now Open the Configuration File Using 
  ```
  nano /root/.vnc/xstartup
  ```

 Copy paste the below contents in it 
 ```
#!/bin/bash
xrdb $HOME/.Xresources
export XDG_SESSION_TYPE=x11
export DISPLAY=:1
exec dbus-launch --exit-with-session startxfce4
```
Make sure to make it executable 
```
chmod +x /root/.vnc/xstartup
```
Then Launch the Server Using 

``` bash
# Launch the server
vncserver
```
- Look for the port it opens for connection (Generally :5901)
 <img width="985" height="118" alt="image" src="https://github.com/user-attachments/assets/ff295b30-20d7-4fbf-943a-672820ebda43" />


- If you wish to kill any Port then use 

```
vncserver -kill :1
```


## NeXt steps for your host Machine
- Make sure that your server is on i.e vncserver is active


- #### Download a VNC Viewer from this link   [VncViewer For Linux](https://www.realvnc.com/en/connect/download/viewer/linux/)

- You will see a interface like this 
<img width="500" height="320" alt="image" src="https://github.com/user-attachments/assets/ed0fddac-588e-4e54-a18e-cc86f991ba5a" />

- In the Blank Area put the address like this
  ``` bash
  # [Husarnet_Connection_address]:port_number  , e.g
  [fc94:7fde:f6cb:bb3f:5a15:44aa:xxxx:xxxx]:5901
  ```

#### BOOM Just authenticate using the password which you kept on you server while configuring and there you go , now you can see the VM through your host machine!!!
