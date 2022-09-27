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

    // ffmpeg相关变量初始化
    AVFormatContext* inFmtCtx = NULL;
    AVFormatContext* outFmtCtx = NULL;
    int inVStreamIndex = -1; // 视频流在序列中的索引

    //======================输入部分============================//
    // 打开h264输入文件
    if (avformat_open_input(&inFmtCtx, filename, NULL, NULL) < 0) {
        printf("Cannot open input file.\n");
        return;
    }
    // 查找输入文件的流
    if (avformat_find_stream_info(inFmtCtx, NULL) < 0) {
        printf("Cannot find stream info in input file.\n");
        return;
    }
    //查找视频流在文件中的位置
    for (unsigned int i = 0; i < inFmtCtx->nb_streams; i++) {
        if (inFmtCtx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO) {
            inVStreamIndex = i;
            break;
        }
    }
    if (inVStreamIndex == -1){
        printf("cannot find video stream\n");
        return;
    }
    //输入视频流的编码参数
    AVCodecParameters *codecPara = inFmtCtx->streams[inVStreamIndex]->codecpar;
    printf("===============Input information========>\n");
    av_dump_format(inFmtCtx, 0, filename, 0);

    //=====================输出部分=========================//
    //打开输出文件并填充格式数据
    if(avformat_alloc_output_context2(&outFmtCtx, NULL, NULL, outfilename)<0){
        printf("Cannot alloc output file context.\n");
        return;
    }
    //打开输出文件并填充数据
    if(avio_open(&outFmtCtx->pb, outfilename, AVIO_FLAG_READ_WRITE)<0){
        printf("output file open failed.\n");
        return;
    }
    //在输出的mp4文件中创建一条视频流
    AVStream *outVStream = avformat_new_stream(outFmtCtx, NULL);
    if(!outVStream){
        printf("Failed allocating output stream.\n");
        return;
    }
    outVStream->time_base.den = 25;
    outVStream->time_base.num = 1;
    int outVStreamIndex = outVStream->index;

    //查找编码器
    AVCodec *outCodec = avcodec_find_encoder(codecPara->codec_id);
    if(outCodec==NULL){
        printf("Cannot find any encoder.\n");
        return;
    }
    //从输入的h264编码器数据复制一份到输出文件的编码器中
    AVCodecContext *outCodecCtx=avcodec_alloc_context3(outCodec);
    AVCodecParameters *outCodecPara = outFmtCtx->streams[outVStream->index]->codecpar;
    if(avcodec_parameters_copy(outCodecPara, codecPara)<0){
        printf("Cannot copy codec para.\n");
        return;
    }
    if(avcodec_parameters_to_context(outCodecCtx, outCodecPara)<0){
        printf("Cannot alloc codec ctx from para.\n");
        return;
    }
    outCodecCtx->time_base.den=25;
    outCodecCtx->time_base.num=1;
    //打开输出文件需要的编码器
    if(avcodec_open2(outCodecCtx,outCodec,NULL)<0){
        printf("Cannot open output codec.\n");
        return;
    }
    printf("============Output Information=============>\n");
    av_dump_format(outFmtCtx, 0, outfilename, 1);

    //写入文件头
    if(avformat_write_header(outFmtCtx,NULL)<0) {
        printf("Cannot write header to file.\n");
        return -1;
    }
    //===============编码部分===============//
    AVStream *inVStream = inFmtCtx->streams[inVStreamIndex];
    AVPacket* pkt = NULL;
    //分配AVPacket结构体
    pkt = av_packet_alloc();
    int frame_index = 0;
    while(av_read_frame(inFmtCtx, pkt)>=0){//循环读取每一帧直到读完
        if(pkt->stream_index==inVStreamIndex){//确保处理的是视频流
            //FIXME：No PTS (Example: Raw H.264)
            //Simple Write PTS
            //如果当前处理帧的显示时间戳为0或者没有等等不是正常值
            if(pkt->pts==AV_NOPTS_VALUE){
                printf("frame_index:%d\n", frame_index);
                //Write PTS
                AVRational time_base1 = inVStream->time_base;
                //Duration between 2 frames (us)
                int64_t calc_duration = (double)AV_TIME_BASE / av_q2d(inVStream->r_frame_rate);
                //Parameters
                pkt->pts = (double)(frame_index*calc_duration) / (double)(av_q2d(time_base1)*AV_TIME_BASE);
                pkt->dts = pkt->pts;
                pkt->duration = (double)calc_duration / (double)(av_q2d(time_base1)*AV_TIME_BASE);
                frame_index++;
            }
            //Convert PTS/DTS
            pkt->pts = av_rescale_q_rnd(pkt->pts, inVStream->time_base, outVStream->time_base, (enum AVRounding)(AV_ROUND_NEAR_INF | AV_ROUND_PASS_MINMAX));
            pkt->dts = av_rescale_q_rnd(pkt->dts, inVStream->time_base, outVStream->time_base, (enum AVRounding)(AV_ROUND_NEAR_INF | AV_ROUND_PASS_MINMAX));
            pkt->duration = av_rescale_q(pkt->duration, inVStream->time_base, outVStream->time_base);
            pkt->pos = -1;
            pkt->stream_index = outVStreamIndex;
            printf("Write 1 Packet. size:%5d\tpts:%ld\n", pkt->size, pkt->pts);
            //Write
            if (av_interleaved_write_frame(outFmtCtx, pkt) < 0) {
                printf("Error muxing packet\n");
                return;
            }
            av_packet_unref(pkt);
        }
    }

    av_write_trailer(outFmtCtx);
}