## Repo Structure
Ansible is a config management tool, but in order to manage server config several things have to interact so we can track how servers are configured and changed over time.

#### Inventory
Config is managed through an inventory system that includes a hosts file, group variables and host variables. The Host file is a list of servers segmented into groups that ansible manages. Group variables are variables that are applied accross an entire group, this lets you change elements of a collection of hosts without having to update multiple variables. Host variables allow you to configure variables on a host level.

#### Roles
Ansible Roles are modules that configure an element of a server. They typically install and configure an element of server for example a web server. They are designed to be composable so they can be used together to create a complete environment. At Genesis we have two types of roles, external ones from the open source community and internal ones to configure our environments and deploy our applications.

#### Ansible Plays
Ansible plays are a collection of roles and tasks that run together to perform a task.

An example of this is the mycompanyname play which installs the our application, this includes our base server configuration role, external java and aerospike roles and our application role.


### Ad-hoc commands
To run plays agains specific targets (hosts,regions,etc):


  AWS create VPC
  --------------

  ansible-playbook plays/aws-vpc.yml -i localhost -e @"network_vars/vpc_clientname.yml"

  AWS Remediations
  ----------------

  ansible-playbook plays/aws-remediations.yml -i localhost -e "region=eu-west-1"
