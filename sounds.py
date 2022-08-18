from pygame import mixer


class Sounds:
    def __init__(self):
        # general setup
        self.sounds = {'shoot_ping':mixer.Sound('audio/shoot_ping.wav'),'hit_ping':mixer.Sound('audio/hit_ping.wav'),'coin_ping':mixer.Sound('audio/coin_ping.wav')}

    def play(self,sound):
        # play sound
        self.sounds[sound].play()

    def set_volume(self,volume):
        # set the volume of every sound to the value passed in
        for key in self.sounds:
            self.sounds[key].set_volume(volume)

    def get_volume(self):
        # return the volume of the sounds
        return list(self.sounds.values())[0].get_volume()