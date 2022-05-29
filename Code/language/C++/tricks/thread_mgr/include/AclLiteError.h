/*
 * @Author       : wanhui
 * @Date         : 2022-05-26 22:13:09
 * @LastEditTime : 2022-05-26 22:27:13
 * @FilePath     : \Brainpower\Code\language\C++\tricks\thread_mgr\include\int.h
 * @Description  : 
 * 
 * Copyright (c) 2022 by willw/vastai, All Rights Reserved. 
 */
#pragma once
#include <unistd.h>

const int ACLLITE_OK = 0;
const int ACLLITE_ERROR = 1;
const int ACLLITE_ERROR_DEST_INVALID = 10;
const int ACLLITE_ERROR_INITED_ALREADY = 11;
const int ACLLITE_ERROR_ENQUEUE = 12;
const int ACLLITE_ERROR_THREAD_ABNORMAL = 14;
const int ACLLITE_ERROR_START_THREAD = 15;