from pygame import mixer


class Set_sounds:
    def __init__(self) -> None:
        mixer.init()

        self.boton1 = mixer.Sound(r"C:\Users\Edouard\Music\sonidos\A_Mellow_Pulse.ogg")

        self.sounds_list: list[mixer.Sound] = [self.boton1]
        self.set_volumen(.5)

    def play(self, sound) -> None:
        if not hasattr(self, sound):
            return
        getattr(self, sound).play()

    def stop(self, sound) -> None:
        if not hasattr(self, sound):
            return
        getattr(self, sound).stop()

    def set_volumen(self, vol) -> None:
        for s in self.sounds_list:
            s.set_volume(vol)
        # for s in self.sounds_list[-3:]:
        #     s.set_volume(vol*.5)