/*
参考链接
https://www.dandelioncloud.cn/article/details/1441297852441153537
https://www.bilibili.com/read/cv12294853
https://blog.csdn.net/leixiaohua1020/article/details/39803457
*/

#include <stdio.h>

// ffmpeg都是c接口
#ifdef __cplusplus
extern "C" {
#endif
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/avutil.h>
#include <libavutil/opt.h>
#ifdef __cplusplus
}
#endif

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

    int videoStreamIndex = -1; // 视频流在是序列中的索引
    int ret = 0; // 默认返回值
    AVFormatContext* ifmtCtx = NULL;
    AVFormatContext* ofmtCtx = NULL;
    AVPacket* yuv420pkt = NULL;
    AVPacket* h264pkt = NULL;
    // 编码器
    AVCodecContext* h264CodecCtx = NULL;
    AVCodec* h264Codec = NULL;

    do
    {
        //============================= 创建输入流Context ====================================//
        //分配一个AVFormatContext，FFMPEG所有的操作都要通过这个AVFormatContext来进行
        ifmtCtx = avformat_alloc_context();
        //==================================== 打开文件 ======================================//
        // 打开一个stream读取header，把封装信息读进fmtCtx
        if ((ret = avformat_open_input(&ifmtCtx, filename, NULL, NULL)) != 0)
        {
            printf("cannot open video file\n");
            break;
        }
        //=================================== 获取视频流信息 =================================//
        // avformat_alloc_context会填充fmtCtx中AVStream字段的部分信息（就是后文用到的fmtCtx->stream）
        // avformat_find_stream_info会取流中的packets来进一步填充里面的关键信息
        if((ret = avformat_find_stream_info(ifmtCtx, NULL)) < 0)
        {
            printf("cannot retrive video info\n");
            break;
        }
        //循环查找视频中包含的流信息，直到找到视频类型的流（一般视频中又视频流、音频流、字幕流等多种流）
        //将其记录下来 保存到videoStreamIndex变量中
        for (unsigned int i = 0; i < ifmtCtx->nb_streams; i++)
        {
            if (ifmtCtx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO)
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
        av_dump_format(ifmtCtx, 0, filename, 0);
    
        //=================================  查找编码器 ===================================//
        h264Codec = avcodec_find_encoder(AV_CODEC_ID_H264);
        if (h264Codec == NULL)
        {
            printf("cannot find encoder\n");
            break;
        }
        
        //================================  打开解码器 ===================================//
        // 设置参数
        h264CodecCtx = avcodec_alloc_context3(h264Codec);
        h264CodecCtx->codec_id = AV_CODEC_ID_H264;
        h264CodecCtx->codec_type = AVMEDIA_TYPE_VIDEO;
        h264CodecCtx->pix_fmt = AV_PIX_FMT_YUV420P;
        h264CodecCtx->width = ifmtCtx->streams[videoStreamIndex]->codecpar->width;
        h264CodecCtx->height = ifmtCtx->streams[videoStreamIndex]->codecpar->height;
        // num为分子，den为分母，1/25表示一秒25帧
        h264CodecCtx->time_base.num = 1;
        h264CodecCtx->time_base.den = 25;
        // 设置比特率
        h264CodecCtx->bit_rate = 400000;
        h264CodecCtx->gop_size = 100;
        // 质量设置等等参数
        h264CodecCtx->qmin = 10;
        h264CodecCtx->qmax = 50;
        
        //================================  创建输出流Context =============================//
        // 使用rtsp封装
        if ((ret = avformat_alloc_output_context2(&ofmtCtx, nullptr, "rtsp", outfilename)) < 0)
        {
            printf("Could not create output context\n");
        }
        // 使用tcp传输
        av_opt_set(ofmtCtx->priv_data, "rtsp_transport", "tcp", 0);
        // 赋值输入流的每一个信息到输出流
        for (int i = 0; i < ifmtCtx->nb_streams; i++)
        {
            AVStream* inStream = ifmtCtx->streams[i];
            AVCodecParameters* in_codecpar = inStream->codecpar;

            AVStream* outStream = avformat_new_stream(ofmtCtx, NULL);
            if (!outStream)
            {
                printf("Failed allocating output stream\n");
                break;
            }
            
            if (avcodec_parameters_copy(outStream->codecpar, in_codecpar) < 0)
            {
                printf("Failed to copy codec parameters\n");
                break;
            }
            
            // 不知道这个干啥的
            outStream->codecpar->codec_tag = 0;
        }
        // 打印输出流信息
        av_dump_format(ofmtCtx, 0, outfilename, 1);
        //==================================== 打开输出流 ================================//
        if (!(ofmtCtx->flags & AVFMT_NOFILE))
        {
            
            if ((ret = avio_open(&ofmtCtx->pb, outfilename, AVIO_FLAG_WRITE)) < 0)
            {
                printf("%d", ret);
                printf("FFMPEG: Could not open\n");
                break;
            }
        }
        // 写容器头
        if((ret = avformat_write_header(ofmtCtx, NULL)) < 0)
        {
            printf("FFMPEG: avformat_write_header error!\n");
            break;
        }
        //============================= 分配AVPacket结构体 ===============================//
        yuv420pkt = av_packet_alloc();
        h264pkt = av_packet_alloc();
        
        //================================  读取视频信息 =================================//
        while (av_read_frame(ifmtCtx, yuv420pkt) >= 0) // 读取视频的一帧，数据存入一个AVPacket的结构中
        {
            if (yuv420pkt->stream_index == videoStreamIndex)
            {
                // 往编码码器发送一个packet进行编码
                if (avcodec_send_packet(h264CodecCtx, yuv420pkt) == 0)
                {
                    // 等待解码完成，接收一个编码后的packet
                    while(avcodec_receive_packet(h264CodecCtx, h264pkt) == 0)
                    {
                        // 转换输入输出时间基
                        
                        av_packet_rescale_ts(h264pkt, 
                            ifmtCtx->streams[yuv420pkt->stream_index]->time_base,
                            ofmtCtx->streams[yuv420pkt->stream_index]->time_base);
                    }
                    // h264pkt->pos = -1;
                    // packet写到输出流
                    if (av_interleaved_write_frame(ofmtCtx, h264pkt) < 0)
                    {
                        printf("Error muxing packet\n");
                        break;
                    }
                }
            }
            // 将缓存空间的引用计数-1，并将Packet中的其他字段设为初始值
            av_packet_unref(h264pkt);
            av_packet_unref(yuv420pkt);
        }
    } while (0);
    //================================ 释放所有指针 ===================================//
    // av_packet_free(&pkt);
    // avcodec_close(codecCtx);
    // avcodec_parameters_free(&avCodecPara);
    // avformat_close_input(&ifmtCtx);
    // avformat_free_context(ifmtCtx);
    // av_frame_free(&frame);

    return 0;
}