#!/bin/bash

download_location=$(pwd)

mkdir -p "/tmp"/{"node1","node2","node3","node4","node5"}
fileSizeToDownload=10GB

function downloadFromSlowSource() {

  echo Download Status
  rm -rf ${fileSizeToDownload}.*
  wget --no-verbose http://speedtest.tele2.net/"${fileSizeToDownload}".zip --directory-prefix=${download_location}
}


function copyPeerToPeer() {

 copyToNode=$1
 fromNode=$download_location
 echo Copying Status for $(basename $copyToNode)
 rsync -azPv ${download_location}/${fileSizeToDownload}.zip  ${copyToNode}/
 #rsync -a ~/dir1 username@remote_host:destination_directory

}

