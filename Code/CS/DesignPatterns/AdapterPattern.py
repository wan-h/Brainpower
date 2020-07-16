# coding: utf-8
# Author: wanhui0729@gmail.com

# 为媒体播放器和更高级的媒体播放器创建接口。
class MediaPlayer(object):
    def play(self, audioType: str, fileName: str):
        pass
class AdvancedMediaPlayer(object):
    def playVlc(self, fileName: str):
        pass
    def playMp4(self, fileName: str):
        pass

# 创建实现了 AdvancedMediaPlayer 接口的实体类。
class VlcPlayer(AdvancedMediaPlayer):
    def playVlc(self, fileName: str):
        print("Playing vlc file. Name: {}".format(fileName))
    def playMp4(self, fileName: str):
        pass
class Mp4Player(AdvancedMediaPlayer):
    def playVlc(self, fileName: str):
        pass
    def playMp4(self, fileName: str):
        print("Playing mp4 file. Name: {}".format(fileName))

# 创建实现 MediaPlayer 接口的适配器类。
class MediaAdapter(MediaPlayer):
    def __init__(self, audioType: str):
        if audioType == 'vlc':
            self.advancedMusicPlayer = VlcPlayer()
        elif audioType == 'mp4':
            self.advancedMusicPlayer = Mp4Player()
        else:
            raise ValueError("Not supported audioType")
    def play(self, audioType: str, fileName: str):
        if audioType == 'vlc':
            self.advancedMusicPlayer.playVlc(fileName)
        elif audioType == 'mp4':
            self.advancedMusicPlayer.playMp4(fileName)
        else:
            raise ValueError("Not supported audioType")

# 创建实现了 MediaPlayer 接口的实体类。
class AudioPlayer(MediaPlayer):
    def __init__(self):
        self.mediaAdapter = None
    def play(self, audioType: str, fileName: str):
        if audioType == 'mp3':
            print("Playing mp3 file. Name: {}".format(fileName))
        elif audioType == 'vlc' or audioType == 'mp4':
            mediaAdapter = MediaAdapter(audioType)
            mediaAdapter.play(audioType, fileName)
        else:
            print("Invalid media. {} format not supported".format(audioType))


if __name__ == '__main__':
    audioPlayer = AudioPlayer()
    audioPlayer.play('mp3', 'beyond the horizon.mp3')
    audioPlayer.play('mp4', 'alone.mp4')
    audioPlayer.play('vlc', 'far far away.vlc')
    audioPlayer.play('avi', 'mind me.avi')