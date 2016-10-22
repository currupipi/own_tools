#! /usr/bin/env bash
#Script to encriypt decrypt files or directories

#Ceck directory exists 
function check_files {
	
	directory=$1
	tarfile=$1.tar.gz
	hidden=".$tarfile"
	encrypted=$hidden.gpg

#	if [ ! -d "$directory" ]; then
#		echo -e  "\t$directory is not a directory on the filesystem"
#		exit 10

	if [ -f "$tarfile" ]; then
		echo -e "\t$tarfile tar file exists for that directory already"
		echo -e "\tconsider to fix that issue manually"
		exit 11

	elif [ -f "$hidden" ]; then
		echo -e "\t$hidden hidden tar file exists already"
		echo -e "\tconsider to fix that issue manually"
		exit 12

	elif [ -e "$encrypted" ]; then
		echo -e "\t[!]WARNING: There is an encrypted file already for that file/directory called $encrypted"
		echo -e "\t At this point you can:"
		echo -e "\t * DELETE the current encrypted file $encrypted if you are confident the content is obsolete (a backup will be done)"
		echo -e "\t * DECRYPT $encrypted to $directory (a backup will be done if needed)"
		echo -e "\t * QUIT to exit"
		while true; do
			read -p "Type 'delete', 'decrypt' or 'quit': >> " choice
			case $choice in
			'delete')
				cp $encrypted ${encrypted}_$(date -I).backup
				if [ $? -ne 0 ]; then
					echo "Can not ensure backup of $encrypted before deleting it"
					exit 13
				fi
				rm $encrypted; exit;; 
			'decrypt')
				if [ -e $directory ]; then
					echo -e "\t[+]INFO: Backing up old $directory befor decrypting $encrypted"
					cp -R $directory ${directory}_$(date -I).backup
					if [ $? -ne 0 ]; then
						echo -e "\t[-]ERROR: Can not ensure backup of $directory before deleting it"
						exit 14
					fi
				fi
				decrypt $directory; exit;;
			'quit') 
				echo "Good bye! :-) "; exit;;
			*)
				echo "Please type in 'delete' or 'decrypt' or 'quit' : ";;
			esac
		done
	fi

	return 0
}

function encrypt {

	directory=$1
	tar_file="$1.tar.gz"

	if [ ! -d "$directory" ]; then
		echo -e  "\t$directory is not a directory on the filesystem"
		exit 10
	fi

	
	echo -e "\t[+]INFO: Creating tar from directory"
	tar czvf $tar_file $directory
	
	if [ $? -ne 0 ]; then
		echo -e "\t[-]ERROR: Fail to create $tar_file from $1"
		exit 20
	
	else
		echo -e "\t[+]INFO: Hiding the tar file"
		mv $tar_file ".$tar_file"
			if [ $? -ne 0 ]; then
				echo -e "\t[-]ERROR: Error hiding the $tar_file"
				exit 21
			else
				echo -e "\t[+]INFO: Encrypting the directory"
				gpg -c ".$tar_file"
				if [ $? -ne 0 ]; then
					echo -e "\t[-]ERROR: Error encrypting the .$tar_file"
					exit 22
				fi
				echo -e "\t[+]INFO: Removing tar hidden file .$tar_file"
				rm ".$tar_file"
				if [ $? -ne 0 ]; then
					echo -e "[-]ERROR: Could not delete the .$tar_file"
					exit 23
				fi
				echo -e "\t[+]INFO: Delete the $directory"
				rm -rf $directory
				if [ $? -ne 0 ]; then
					echo -e "\t[-]ERROR: Can not delte the $directory"
					exit 24
				fi			

			fi 
	fi

	return 0
}

function decrypt {

	directory=$1
	tarfile=$1.tar.gz
	hidden=".$tarfile"
	encrypted=$hidden.gpg

	if [ ! -e "$encrypted" ]; then
		echo -e "\t[-]ERROR: $encrypted file does not exist"
		echo -e "\tSeems like there is no encrypted file for this $directory yet"
		echo -e "\tPlease ensure the name of the file or directory is ok and try it again"
		exit 30
	fi

	echo -e "\t[+]INFO: Decripting $encrypted"
	gpg --output $tarfile --decrypt $encrypted

	if [ $? -ne 0 ]; then
		echo -e "\t[-]ERROR: Can not decrypt $encrypted"
		exit 31
	else 
		echo -e "\t[+]INFO: Untar $tarfile"
		tar xzvf $tarfile
		if [ $? -ne 0 ]; then
			echo -e "\t[-]ERROR: Can not untar $tarfile"
			exit 32
		fi
		echo -e "\t[+]INFO: Removing $tarfile"
		rm $tarfile
	fi

	return 0	
}


echo "Enter full path of the directory: "
read directory
check_files $directory

while true; do
	read -p "Do you want to Encrypt [type 'e'] or decryt [type 'd']?: >> " choice
	case $choice in
		e|E)
			encrypt $directory; break;;
		d|D) 
			decrypt $directory; break;;
		*)
			echo "Please answer 'e' or 'd'";;
	esac
done

