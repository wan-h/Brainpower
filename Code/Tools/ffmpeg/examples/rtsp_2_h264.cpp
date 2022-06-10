/*
* 操作基本和mp4_2_yuv420.cpp一致
* 如果只是保存h264对于不用的codec代码可以删除，这里时没有删除的
* AVDictionary相对于解mp4多出来的设置，是为了解决rtsp掉帧的问题，可以进一步研究
*/

#include <stdio.h>

// ffmpeg都是c接口
#ifdef __cplusplus
extern "C" {
#endif
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/avutil.h>
#ifdef __cplusplus
}
#endif

#define FRAME_END 200

int main(int argc, char** argv)
{
    const char* filename;
    const char* outfilename;
    // 解析参数
    if(argc < 2)
    {
        fprintf(stderr, "Usage: %s <input file> <output file>\n", argv[0]);
        exit(0);
    }
    filename = argv[1];
    outfilename = argv[2];

    FILE* fp = fopen(outfilename, "w+b");
    if (fp == NULL)
    {
        printf("Cannot open file.\n");
        return -1;
    }
    int videoStreamIndex = -1; // 视频流在是序列中的索引
    int ret = 0; // 默认返回值
    // ffmpeg相关变量初始化
    AVFormatContext* fmtCtx = NULL;
    AVPacket* pkt = NULL;
    AVCodecContext* codecCtx = NULL;
    AVCodecParameters* avCodecPara = NULL;
    AVCodec* codec = NULL;
    AVFrame* frame = av_frame_alloc(); 

    do
    {
        //=========================== 创建AVFormatContext结构体 ===============================//
        //分配一个AVFormatContext，FFMPEG所有的操作都要通过这个AVFormatContext来进行
        fmtCtx = avformat_alloc_context();
        //==================================== 打开文件 ======================================//
        // 一下设置是为了防止解码掉帧的设置
        AVDictionary *options = NULL;
        av_dict_set(&options, "buffer_size", "1024000", 0); //设置缓存大小,1080p可将值跳到最大
        av_dict_set(&options, "rtsp_transport", "tcp", 0); //以tcp的方式打开,
        av_dict_set(&options, "stimeout", "5000000", 0); //设置超时断开链接时间，单位us
        av_dict_set(&options, "max_delay", "500000", 0); //设置最大时延
        // 打开一个stream读取header，把封装信息读进fmtCtx
        if ((ret = avformat_open_input(&fmtCtx, filename, NULL, &options)) != 0)
        {
            printf("cannot open video file\n");
            break;
        }
        //=================================== 获取视频流信息 =================================//
        // avformat_alloc_context会填充fmtCtx中AVStream字段的部分信息（就是后文用到的fmtCtx->stream）
        // avformat_find_stream_info会取流中的packets来进一步填充里面的关键信息
        if((ret = avformat_find_stream_info(fmtCtx, NULL)) < 0)
        {
            printf("cannot retrive video info\n");
            break;
        }
        //循环查找视频中包含的流信息，直到找到视频类型的流（一般视频中又视频流、音频流、字幕流等多种流）
        //将其记录下来 保存到videoStreamIndex变量中
        for (unsigned int i = 0; i < fmtCtx->nb_streams; i++)
        {
            if (fmtCtx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO)
            {
                videoStreamIndex = i;
                break;
            }
        }
        // 如果videoStreamIndex为-1说明没有找到
        if (videoStreamIndex == -1)
        {
            printf("cannot find video stream\n");
            break;
        }
        //打印输入和输出信息：长度 比特率 流格式等
        av_dump_format(fmtCtx, 0, filename, 0);
        //=================================  查找解码器 ===================================//
        avCodecPara = fmtCtx->streams[videoStreamIndex]->codecpar;
        // 通过解析原视频的解码器参数来寻找对应的解码器
        codec = avcodec_find_decoder(avCodecPara->codec_id);
        if (codec == NULL)
        {
            printf("cannot find decoder\n");
            break;
        }
        //根据解码器参数来创建解码器内容
        codecCtx = avcodec_alloc_context3(codec);
        avcodec_parameters_to_context(codecCtx, avCodecPara);
        if (codecCtx == NULL) {
            printf("Cannot alloc context.");
            break;
        }
        //================================  打开解码器 ===================================//
        if ((ret = avcodec_open2(codecCtx, codec, NULL) < 0))
        {   
            printf("cannot open decoder\n");
            break;
        }
        int width = codecCtx->width; // 视频宽度
        int height = codecCtx->height; // 视频高度
        //============================= 分配AVPacket结构体 ===============================//
        pkt = av_packet_alloc();
        // 调整packet的数据空间大小
        // 这个size时预估的，只要能装下一个编码前的一帧数据就可以了，最大也就 width * height * 1.5 (YUV数据需要的Bits)
        av_new_packet(pkt, width * height); 
        //================================  读取视频信息 =================================//
        int frame_cnt = 0;
        while (av_read_frame(fmtCtx, pkt) >= 0) // 读取视频的一帧，数据存入一个AVPacket的结构中
        {
            if (pkt->stream_index == videoStreamIndex)
            {
                // 往解码器发送一个packet进行解码
                if (avcodec_send_packet(codecCtx, pkt) == 0)
                {
                    frame_cnt += 1;
                    printf("Decode frame: %d\n", frame_cnt);
                    // 等待解码完成，接收一个解码后的frame
                    while(avcodec_receive_frame(codecCtx, frame) == 0)
                    {
                        // yuv数据写入文件
                        // fwrite(frame->data[0], 1, width * height, fp); // Y
                        // fwrite(frame->data[1], 1, width * height / 4, fp); // U
                        // fwrite(frame->data[2], 1, width * height / 4, fp); // V
                        fwrite(pkt->data, 1, pkt->size, fp);
                    }
                    if (frame_cnt >= FRAME_END)
                    {
                        break;
                    }
                }
                // 将缓存空间的引用计数-1，并将Packet中的其他字段设为初始值
                av_packet_unref(pkt);
            }
        }
    } while (0);
    //================================ 释放所有指针 ===================================//
    fclose(fp);
    av_packet_free(&pkt);
    avcodec_close(codecCtx);
    avcodec_parameters_free(&avCodecPara);
    // avformat_close_input(&fmtCtx);
    // avformat_free_context(fmtCtx);
    av_frame_free(&frame);

    return 0;
}