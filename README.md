### Ad-hoc commands
To run plays agains specific targets (hosts,regions,etc):


  AWS create VPC
  --------------

  ansible-playbook plays/aws-vpc.yml -i localhost -e @"network_vars/vpc_clientname.yml"

  AWS Remediations
  ----------------

  ansible-playbook plays/aws-remediations.yml -i localhost -e "region=eu-west-1"
