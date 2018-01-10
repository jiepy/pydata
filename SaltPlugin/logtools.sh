#!/bin/bash
##################################################
# Filename: ngxlog.sh
# Date : 2018/01/09
# Desc : 计算每台服务器上nginx 日志的499,5xx总和
#
##################################################

# Define color
red() {
  echo -e "\033[31m$1 \033[0m"
}
green() {
  echo -e "\033[32m$1 \033[0m"
}
yellow() {
  echo -e "\033[33m $1 \033[0m"
}



groupRun() {

    green "[Info] Start sync modules..."
    salt -N $1 saltutil.sync_modules
    echo
    green "[Info] Start logcheck..."
    salt -N $1 logcount.main logfile=$2 min=$3 --output=txt
    echo
    green "[Info] check result: "
    salt -N $1 logcount.main logfile=$2 min=$3 --output=txt|awk -F ",|:" '{print $3,$5}'|sed -e 's/\}//'\
    |awk '{ x += $1 } { y += $2} END { print "Result: [499: "x " | 5xx: "y"]" }'

    # salt -N $1 logcount.main logfile=$2 min=$3 --output=txt|awk -F , '{print $3,$4}'|sed -e 's/\}//'\
    # |awk '{ x += $2 } { y += $4} END { print "Result: [499: "x " | 5xx: "y"]" }'

}

help() {
    echo
    echo -e " Usage: bash `basename $0` {module_id}  [timeRange]"
    echo -e "\t--------------------------"
    echo -e "\tid   module_name  Desc"
    echo -e "\t[1]  test         测试模块"
    echo -e "\t--------------------------"
    echo
    yellow  "\tmodule_id : 以上模块的id [ * 必选参数 ]"
    yellow  "\ttimeRange : 默认查找10分钟内日志[ 可选参数 ]"

}

TimeRange="10"
[[ $# -eq 2 ]] && TimeRange=$2

case "$1" in
  1)
  host="ngxlogt"
  logfile="test.log"
  groupRun $host $logfile $TimeRange
  ;;
  stop)
  stop
  ;;
  status)
  status
  ;;
  *)
  help
  ;;
esac