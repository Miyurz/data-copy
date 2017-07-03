#!/bin/bash

download_location=$(pwd)

mkdir -p "/tmp"/{"node1","node2","node3","node4","node5"}

function downloadFromSlowSource() {

  fileSizeToDownload=10GB
  figlet Download Status
  wget  http://speedtest.tele2.net/"${fileSizeToDownload}".zip --directory-prefix=${download_location}
}


function copyPeerToPeer() {

 copyToNode=$1
 fromNode=$download_location
 figlet Copying Status from $fromNode to $copyToNode
 rsync -azPv ${download_location} ${copyToNode}/
 #rsync -a ~/dir1 username@remote_host:destination_directory

}

