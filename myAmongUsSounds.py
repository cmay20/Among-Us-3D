import simpleaudio as sa

class Sounds(object):

    def __init__(self):
        '''MUSIC:'''
        #main title screen music
        #SOURCE: https://www.youtube.com/watch?v=_0ittRlRY28
        #converted to wav with https://ontiva.com/watch?v=_0ittRlRY28
        filename = 'gameSounds/amongUsMainTitle.wav'
        self.mainTitleMusicWav_obj = sa.WaveObject.from_wave_file(filename)

        #game ambience music/noise
        #SOURCE: https://www.youtube.com/watch?v=oRuoaG6ugW0
        #converted to wav with https://ontiva.com/watch?v=oRuoaG6ugW0
        filename = 'gameSounds/amongUsGameAmbience.wav'
        self.gameMusicWav_obj = sa.WaveObject.from_wave_file(filename)

        '''SOUND EFFECTS:'''
        #click on splash screen button sound
        #SOURCE: https://www.youtube.com/watch?v=oVRg2FRl0gY 
        #converted to wav with https://ontiva.com/watch?v=_0ittRlRY28 
        filename = 'gameSounds/buttonClick.wav'
        self.buttonClickWav_obj = sa.WaveObject.from_wave_file(filename)

        #kill sound
        #SOURCE: **************************find this source
        filename = 'gameSounds/amongUsKillSound.wav'
        self.killSoundWav_obj = sa.WaveObject.from_wave_file(filename)

        filename = 'gameSounds/reportSound.wav'
        self.reportSoundWav_obj = sa.WaveObject.from_wave_file(filename)
    
    
    #Main title music PLAY
    def playMainTitleScreenMusic(self):
        self.mTMplay_obj = self.mainTitleMusicWav_obj.play()
        if not self.mTMplay_obj.is_playing():
            self.mTMplay_obj = self.mainTitleMusicWav_obj.play()
        #self.mTMplay_obj.wait_done() #Wait until sound has finished playing
    
    #Main title music STOP
    def stopIfPlayingMainTitleScreenMusic(self):
        if self.mTMplay_obj.is_playing():
            self.mTMplay_obj.stop()


    #game music PLAY ****this played almost immediately, i wonder y, test this out
    def playGameMusic(self):
        self.gMusicplay_obj = self.gameMusicWav_obj.play()
        if not self.gMusicplay_obj.is_playing(): #not called multiple times
            self.gMusicplay_obj = self.gameMusicWav_obj.play()
        #self.mTMplay_obj.wait_done() #Wait until sound has finished playing
    
    #game music STOP
    def stopIfPlayingGameMusic(self):
        if self.gMusicplay_obj.is_playing():
            self.gMusicplay_obj.stop()


    #Button click PLAY
    def playButtonClickSound(self):
        bClickPlay_obj = self.buttonClickWav_obj.play()
        #bClickPlay_obj.wait_done()

    #kill sound PLAY
    def playKillSound(self):
        playKill_obj = self.killSoundWav_obj.play()
        #play_obj.wait_done() 
    
    def playReportSound(self):
        reportPlay_obj = self.reportSoundWav_obj.play()
        #reportPlay_obj.wait_done()