# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ncg/trusty64"
  config.ssh.forward_agent = true

  config.vm.network "forwarded_port", guest: 8100, host: 8100
  config.vm.network "forwarded_port", guest: 8101, host: 8101


  config.vm.provision :ansible do |ansible|
    ansible.playbook = "deployment/playbook.yml"
    ansible.skip_tags = ['git',]
    ansible.groups = {
      "tag_Project_Safebee" => ['default'],
      "tag_Environment_Vagrant" => ['default'],
      "tag_Layer_Admin" => ['default'],
      #"tag_Layer_Webapp" => ['default'],
      "tag_Layer_Varnish" => ['default'],
      "vagrant" => ['default'],
    }

  end
end
