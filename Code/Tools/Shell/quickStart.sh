#!/bin/bash
# encoding: utf-8.0

array=(20 60)
for element in ${array[*]}
do
  if [ $element == 20 ]; then
    echo "20为年轻人"
  elif [ $element == 60 ]; then
    echo "60为老年人"
  fi
done

echo -n "请输入你的年龄: "
read age

if [ $age -gt 120 ] || [ $age -lt 0 ]; then
  echo "请输出一个合法的年龄"
  exit
fi

function parse_age() {
  case $1 in
  20)
    echo "年轻人"
    ;;
  60)
    echo "老年人"
  echo "不知道"
  esac
}

parse_age $age

