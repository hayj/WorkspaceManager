# Requirements: you need to setup the venv of your project on the remote server
# Also install pipsi and pew and then run a pew command to init it
# sudo pip install pipsi
# sudo pipsi install pew
# pew ls

# Getting the current dir:
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Getting the conf path:
confFile=$DIR"/conf.json"
# Getting the server adress in the conf:
function getJson()
{
    data=$(jq ."$1" $2)
    data=${data#"\""}
    data=${data%"\""}
    echo $data
}
adress=$(getJson "adress" $confFile)
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
# We set the default path:
if [ "$path" == "null" ]
then
    path="/home/"$user
fi
# Echo infos:
echo "rsyncing dists at "$adress" in "$venv
# Create the directory:
wmDistTmp=$path"/wm-dist-tmp/"$project
ssh "$user"@$adress mkdir -p $wmDistTmp
# Rsync all:
rsync -a $DIR/* $user@$adress:$wmDistTmp
# Check whether workspacemanager is installed:
regex='workspacemanager'
sshResult=$(ssh "$user"@$adress 'pip freeze')
if ! [[ $sshResult =~ $regex ]]
then
	echo "Installing workspacemanager on the remote server..."
	ssh -t $user@$adress 'sudo pip install workspacemanager'
fi
# Check wheteher the venv exists:
sshResult=$(ssh "$user"@$adress 'pew ls')
if ! [[ $sshResult =~ $venv ]]
then
	echo "Creating the venv..."
	if [ "pythonPath" == "null" ]
    then
        ssh $user@$adress "pew new -d $venv"
    else
        ssh $user@$adress "pew new -p $pythonPath -d $venv"
    fi
fi
# Install all files:
for current in $DIR/*.gz; do
	bName=$(basename $current)
	current=$wmDistTmp"/"$bName
	 # Pew is not found by ssh, so we need the full path, you can edit this line if pew is at an other place
    package=$(echo $bName | perl -nle 'm/(.*)-(?:\d.)+\d.tar.gz/; print $1')
	ssh $user@$adress "/usr/bin/yes | pew in $venv pip uninstall $package"
	ssh $user@$adress "pew in $venv pip install $current"
done




