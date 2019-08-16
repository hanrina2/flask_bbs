# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_COMMAND = ARGV[0]

Vagrant.configure("2") do |config|
  # root 登陆
  config.ssh.username = 'root'
  if VAGRANT_COMMAND == "up"
    config.ssh.username = 'vagrant'
  end

  # 虚拟机镜像名字
  config.vm.box_url = "https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cloud-images/bionic/20181212/bionic-server-cloudimg-amd64-vagrant.box"
  config.vm.box = "ubuntu/bionic"

  # 映射文件夹
  config.vm.synced_folder ".", "/var/www/flask_bbs"

  # 桥接网络
  config.vm.network "public_network"

  # 脚本
  config.vm.provision "shell", inline: <<-SHELL
    # 换成 root 用户
    sudo su
    # 之后 ssh 都用 root
    cp -f /home/vagrant/.ssh/authorized_keys /root/.ssh/authorized_keys
    bash /var/www/flask_bbs/mirror.sh
    bash /var/www/flask_bbs/deploy.sh
  SHELL

end
