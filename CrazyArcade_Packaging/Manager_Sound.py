# coding: cp949
#pico2d.py에서 audio_on = False에서 audio_on = True로 변경함
#pico2d.py에서 Music 소멸자 막아놓음
from pico2d import *

SoundList = {}

def LoadSoundData():
    global SoundList
    
    #배너 사운드
    SoundList['WIN'] = load_music('.\\Sound\\SFX_Word_Win.ogg')
    SoundList['WIN'].set_volume(16)
    SoundList['LOSE'] = load_music('.\\Sound\\SFX_Word_Lose.ogg')
    SoundList['LOSE'].set_volume(16)
    SoundList['HURRYUP'] = load_music('.\\Sound\\SFX_Word_Hurryup.ogg')
    SoundList['HURRYUP'].set_volume(16)
    SoundList['START'] = load_music('.\\Sound\\SFX_Word_Start.ogg')
    SoundList['START'].set_volume(16)

    #플레이어 사운드
    SoundList['CHAR_DIE'] = load_music('.\\Sound\\SFX_Character_Die.ogg')
    SoundList['CHAR_DIE'].set_volume(16)
    SoundList['CHAR_FIXED'] = load_music('.\\Sound\\SFX_Character_Fixed.ogg')
    SoundList['CHAR_FIXED'].set_volume(16)
    SoundList['CHAR_REVIVAL'] = load_music('.\\Sound\\SFX_Character_Revival.ogg')
    SoundList['CHAR_REVIVAL'].set_volume(16)

    #물풍선 사운드
    SoundList['BUBBLE_ON'] = load_music('.\\Sound\\SFX_Bubble_On.ogg')
    SoundList['BUBBLE_ON'].set_volume(16)
    SoundList['BUBBLE_OFF'] = load_music('.\\Sound\\SFX_Bubble_Off.ogg')
    SoundList['BUBBLE_OFF'].set_volume(16)

    #버튼 사운드
    SoundList['BUTTON_ON'] = load_music('.\\Sound\\SFX_Button_On.ogg')
    SoundList['BUTTON_ON'].set_volume(16)
    SoundList['BUTTON_OFF'] = load_music('.\\Sound\\SFX_Button_Off.ogg')
    SoundList['BUTTON_OFF'].set_volume(16)
    SoundList['EMPTY_ON'] = load_music('.\\Sound\\SFX_Empty_On.ogg')
    SoundList['EMPTY_ON'].set_volume(16)
    SoundList['EMPTY_OFF'] = load_music('.\\Sound\\SFX_Empty_Off.ogg')
    SoundList['EMPTY_OFF'].set_volume(16)

    #몬스터 사운드
    SoundList['MONSTER_DIE'] = load_music('.\\Sound\\SFX_Monster_Basic_Normal_Die.ogg')
    SoundList['MONSTER_DIE'].set_volume(16)

    #보스몬스터 사운드
    SoundList['BOSS_MOVE'] = load_music('.\\Sound\\SFX_Monster_Boss_Move.ogg')
    SoundList['BOSS_MOVE'].set_volume(16)

    #아이템 사운드
    SoundList['ITEM_BANANA_OFF'] = load_music('.\\Sound\\SFX_Item_Banana_Off.ogg')
    SoundList['ITEM_BANANA_OFF'].set_volume(16)
    SoundList['ITEM_DART'] = load_music('.\\Sound\\SFX_Item_Dart.ogg')
    SoundList['ITEM_DART'].set_volume(16)
    SoundList['ITEM_ON'] = load_music('.\\Sound\\SFX_Item_On.ogg')
    SoundList['ITEM_ON'].set_volume(16)
    SoundList['ITEM_OFF'] = load_music('.\\Sound\\SFX_Item_Off.ogg')
    SoundList['ITEM_OFF'].set_volume(16)

def PlayEffectSound(_sound_name):
    global SoundList

    SoundList[_sound_name].play()


def PlayRepeatedEffectSound(_sound_name):
    global SoundList

    SoundList[_sound_name].repeat_play()


def StopRepeatedEffectSound(_sound_name):
    global SoundList

    SoundList[_sound_name].stop()