# Requirements:
# Create all confile file you want "conf-*.json"
# Default: the script take all confs, or you can give a conf file name in params
# install jq:
#  * sudo apt-get install jq
# install pipsi and pew and then run a pew command to init it:
#  * sudo pip install pipsi
#  * sudo pipsi install pew
#  * pew ls

# Vars to set:
packagePrefix="hj" # TODO use package_prefix of the workspace conf

# We get the conf file:
if [ -z "$1" ]
then
    allConfs=$(find ./ -name "conf-*.json" -print0 | xargs -0 ls)
else
    allConfs=$1
fi
# For all conf file:
for confName in $allConfs
do
    # Getting the current dir:
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    # Getting the conf path:
    confFile=$DIR"/$confName"
    # Getting the server address in the conf:
    function getJson()
    {
        data=$(jq ."$1" $2)
        data=${data#"\""}
        data=${data%"\""}
        echo $data
    }
    # Getting all addresses (addresses are separated by a space):
    addresses=($(jq -r '.address' $confFile))
    # Getting the venv name in the conf:
    venv=$(getJson "venv" $confFile)
    # Getting the user name in the conf:
    user=$(getJson "user" $confFile)
    # Getting the project name in the conf:
    project=$(getJson "project" $confFile)
    # Getting the path name in the conf:
    path=$(getJson "path" $confFile)
    # Getting the path name in the conf:
    pythonPath=$(getJson "pythonPath" $confFile)
    # Getting the port in the conf:
    port=$(getJson "port" $confFile)
    # Getting the removeTargetDist in the conf:
    removeTargetDist=$(getJson "removeTargetDist" $confFile)
    # We delete the target dist package because we don't want to install it (just all dependencies):
    if [ "$removeTargetDist" == "null" ] || [ $removeTargetDist == true ]
    then
        # Warning, if your target package doesn't match this pattern, you have to make your own:
        targetDistPattern="*"$(echo "$project" | tr '[:upper:]' '[:lower:]')"-*.tar.gz"
        rm $DIR/$targetDistPattern 2> /dev/null
    fi
    # For each address:
    for var in "${addresses[@]}"
    do
        # Getting the current address:
        address="${var}"
        # We first check if the host is reachable:
        status=$(ssh -o BatchMode=yes -o ConnectTimeout=10 -p "$port" "$user"@"$address" echo "_CONNEXION_SUCCESS_" 2>&1)
        if [[ $status = *"_CONNEXION_SUCCESS_"* ]]
        then
            echo "==> The host $address is reachable <=="
            # We set the default path:
            if [ "$path" == "null" ]
            then
                path="/home/"$user
            fi
            # Echo infos:
            echo "rsyncing dists at "$address" in "$venv
            # Create the directory:
            wmDistTmp=$path"/wm-dist-tmp/"$project
            ssh -p $port "$user"@$address mkdir -p $wmDistTmp
            # We delete all tar.gz:
            ssh -p $port "$user"@$address rm $wmDistTmp/*-*.tar.gz
            # Rsync all:
            rsync -e "ssh -p $port" -a $DIR/* $user@$address:$wmDistTmp
            # Check whether workspacemanager is installed:
            # regex='workspacemanager'
            # sshResult=$(ssh -p $port "$user"@$address 'pip freeze')
            # if ! [[ $sshResult =~ $regex ]]
            # then
            #     echo "Installing workspacemanager on the remote server..."
            #     ssh -p $port -t $user@$address 'sudo pip install workspacemanager'
            # fi
            # Check wheteher the venv exists:
            sshResult=$(ssh -p $port "$user"@$address 'pew ls')
            if ! [[ $sshResult =~ $venv ]]
            then
                echo "Creating the venv..."
                if [ "$pythonPath" == "null" ]
                then
                    ssh -p $port $user@$address "pew new -d $venv"
                else
                    ssh -p $port $user@$address "pew new -p $pythonPath -d $venv"
                fi
            fi
            # Install all files:
            for current in $DIR/*.gz; do
                bName=$(basename $current)
                current=$wmDistTmp"/"$bName
                # Pew is not found by ssh, so we need the full path, you can edit this line if pew is at an other place
                package=$(echo $bName | perl -nle 'm/(.*)-(?:\d+.)+\d+.tar.gz/; print $1')
                echo "==> Uninstalling $package... <=="
                uninstallResult=$(ssh -p $port $user@$address "/usr/bin/yes | pew in $venv pip uninstall $package" 2>&1)
                if [[ $uninstallResult = *"Cannot uninstall"* ]]; then
                    ssh -p $port $user@$address "/usr/bin/yes | pew in $venv pip uninstall $packagePrefix$package"
                fi
                ssh -p $port $user@$address "pew in $venv pip install $current"
            done
        else
            echo "==> The host $address is unreachable <=="
        fi
    done # End for each address
done