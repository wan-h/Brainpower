# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个抽象类，它的模板方法被设置为 final。
class Game(object):
    def initialize(self):
        pass
    def startPlay(self):
        pass
    def endPlay(self):
        pass
    def play(self):
        self.initialize()
        self.startPlay()
        self.endPlay()

# 创建扩展了上述类的实体类。
class Cricket(Game):
    def endPlay(self):
        print("Cricket Game Finished!")
    def initialize(self):
        print("Cricket Game Initialized! Start playing.")
    def startPlay(self):
        print("Cricket Game Started. Enjoy the game!")
class Football(Game):
    def endPlay(self):
        print("Football Game Finished!")
    def initialize(self):
        print("Football Game Initialized! Start playing.")
    def startPlay(self):
        print("Football Game Started. Enjoy the game!")

# 使用 Game 的模板方法 play() 来演示游戏的定义方式。
if __name__ == '__main__':
    game = Cricket()
    game.play()
    print("")
    game = Football()
    game.play()