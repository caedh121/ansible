Set-DefaultAWSRegion -Region eu-west-1
(Get-EC2Instance).Instances | ` # Get EC2 instances and pass to pipeline
ForEach-Object -Process {
    # Get the "Customer", "Name" and "Environment" tags of the current instance ID; Amazon.EC2.Model.Tag is in the Instances object
    $instanceCustomer = $_.Tags | Where-Object -Property Key -EQ "Customer" | Select-Object -ExpandProperty Value
    $instanceName = $_.Tags | Where-Object -Property Key -EQ "Name" | Select-Object -ExpandProperty Value
    $instanceEnv = $_.Tags | Where-Object -Property Key -EQ "Environment" | Select-Object -ExpandProperty Value
    $_.BlockDeviceMappings | ` # Pass all the current block device objects down the pipeline
    ForEach-Object -Process {
        $volumeid = $_.ebs.volumeid # Retrieve current volume id for this BDM in the current instance
        # Get the current volume's Customer tag
        $volumeCustomerTag = Get-EC2Tag -Filter @(@{ name = 'tag:Customer'; values = "*" }; @{ name = "resource-type"; values = "volume" }; @{ name = "resource-id"; values = $volumeid }) | Select-Object -ExpandProperty Value
        $volumeNameTag = Get-EC2Tag -Filter @(@{ name = 'tag:Name'; values = "*" }; @{ name = "resource-type"; values = "volume" }; @{ name = "resource-id"; values = $volumeid }) | Select-Object -ExpandProperty Value
        $volumeEnvTag = Get-EC2Tag -Filter @(@{ name = 'tag:Environment'; values = "*" }; @{ name = "resource-type"; values = "volume" }; @{ name = "resource-id"; values = $volumeid }) | Select-Object -ExpandProperty Value       
     if (-not $volumeCustomerTag) # Replace the tag in the volume if it is blank
        {
            New-EC2Tag -Resources $volumeid -Tags @{ Key = "Customer"; Value = $instanceCustomer } # Add volume Customer tag that matches Instance Customer Tag
            
        } 
     if (-not $volumeNameTag) # Replace the tag in the volume if it is blank
        {
            New-EC2Tag -Resources $volumeid -Tags @{ Key = "Name"; Value = $instanceName } # Add volume Name tag that matches Instance Name Tag
            
        } 
     if (-not $volumeEnvTag) # Replace the tag in the volume if it is blank
        {
            New-EC2Tag -Resources $volumeid -Tags @{ Key = "Environment"; Value = $instanceEnv } # Add volume Environment tag that matches Instance Environment Tag
            
        } 
            New-EC2Tag -Resources $volumeid -Tags @{ Key = "Taggedby"; Value = "Adrian" } # Add Taggedby tag value = Adrian to all Volumes tagged by the script
    }
}
