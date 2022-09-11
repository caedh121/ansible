Role Name
=========

roles/aws-remediations

Requirements
------------

AWS Cli with configured credentials  
Python3

Role usage
----------

Edit the main.yml task file to include or ommit the desired remediation tasks

List of Tasks
-------------

snapshots_cleanup  - safely delete all unused snapshots in the specified region 

Role Variables
--------------

region=<value> (only 4 regions are allowed so far: us-east-1, sa-east-1, eu-west-1, eu-west-2)

Playbook
--------

plays/aws-remediations.yml


Ad-hoc command example
----------------------

sudo ansible-playbook plays/aws-remediations.yml -i localhost -e "region=eu-west-1"


Author Information
------------------

adrian.estrada@global
