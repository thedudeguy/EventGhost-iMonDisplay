"""
This module wraps the IMON Display API DLL to
integrate with LCD / VFD devices

"""

from ctypes import CDLL, c_int, CFUNCTYPE, POINTER, byref
from ctypes.wintypes import HWND, UINT, LPCSTR, BOOL, BYTE
from os.path import dirname, join, abspath
from imon_message import DSPResult, DSPEQDATA, bandInfoToCType

# Load the imon display DLL into memory.
imonDll = CDLL(abspath(join(dirname(__file__), "iMONDisplay.dll")))

# DLL Function Setup
imonDll.IMON_Display_Init.argtypes = [HWND, UINT]
imonDll.IMON_Display_Init.restype  = DSPResult

imonDll.IMON_Display_Uninit.argtypes = []
imonDll.IMON_Display_Uninit.restype  = DSPResult

imonDll.IMON_Display_IsInited.argtypes = []
imonDll.IMON_Display_IsInited.restype  = DSPResult

imonDll.IMON_Display_IsPluginModeEnabled.argtypes = []
imonDll.IMON_Display_IsPluginModeEnabled.restype  = DSPResult

imonDll.IMON_Display_SetVfdText.argtypes = [LPCSTR, LPCSTR]
imonDll.IMON_Display_SetVfdText.restype = DSPResult

imonDll.IMON_Display_SetVfdEqData.argtypes = [POINTER(DSPEQDATA)]
imonDll.IMON_Display_SetVfdEqData.restype = DSPResult

imonDll.IMON_Display_SetLcdText.argtypes = [LPCSTR]
imonDll.IMON_Display_SetLcdText.restype = DSPResult

imonDll.IMON_Display_SetLcdAllIcons.argtypes = [BOOL]
imonDll.IMON_Display_SetLcdAllIcons.restype = DSPResult

imonDll.IMON_Display_SetLcdOrangeIcon.argtypes = [BYTE, BYTE]
imonDll.IMON_Display_SetLcdOrangeIcon.restype = DSPResult

imonDll.IMON_Display_SetLcdMediaTypeIcon.argtypes = [BYTE]
imonDll.IMON_Display_SetLcdMediaTypeIcon.restype = DSPResult

imonDll.IMON_Display_SetLcdSpeakerIcon.argtypes = [BYTE, BYTE]
imonDll.IMON_Display_SetLcdSpeakerIcon.restype = DSPResult

imonDll.IMON_Display_SetLcdVideoCodecIcon.argtypes = [BYTE]
imonDll.IMON_Display_SetLcdVideoCodecIcon.restype = DSPResult

imonDll.IMON_Display_SetLcdAudioCodecIcon.argtypes = [BYTE]
imonDll.IMON_Display_SetLcdAudioCodecIcon.restype = DSPResult

imonDll.IMON_Display_SetLcdAspectRatioIcon.argtypes = [BYTE]
imonDll.IMON_Display_SetLcdAspectRatioIcon.restype = DSPResult

imonDll.IMON_Display_SetLcdEtcIcon.argtypes = [BYTE]
imonDll.IMON_Display_SetLcdEtcIcon.restype = DSPResult

imonDll.IMON_Display_SetLcdProgress.argtypes = [c_int, c_int]
imonDll.IMON_Display_SetLcdProgress.restype = DSPResult

# Main Functions ###################################

def init(hwnd, wm):
    """
    This function should be called to use other functions in iMON Display API.
    When the caller application calls this function, API tries to request Display Plug-in Mode to iMON.

    Parameters
    ---------
    hwnd : HWND
        API will send/post message to this handle. hwnd is a reference to a win32 window, specifically
    wm : UINT
        API will send/post message to hwndNoti with this message identifier, such as that created by the win32 api
        RegisterWindowMessage("IMON_DISPLAY")

    Returns
    -------
    DSPResult : EnumMember
        This function will return one of DSPResult DSP_SUCCEEDED enum on success.
        only returned if succeeded.

    Raises
    ------
    Exception
        Raised when any response is return from IMON that is not a success.
        This can includeDSP_E_INVALIDARG or DSP_E_OUTOFMEMORY errors from the
        DSPResult Enumorater.

    """
    result = imonDll.IMON_Display_Init(HWND(hwnd), UINT(wm))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def unInit():
    """
    This function should be called when the caller application need not use this API any more.
    If this function call is missed, iMON can't display other information.

    Returns
    -------
    DSPResult : EnumMember
        This function will return one of DSPResult DSP_SUCCEEDED enum on success.
        only returned if succeeded.

    Raises
    ------
    Exception
        Raised when any response is return from IMON that is not a success.

    """
    result =  imonDll.IMON_Display_Uninit()
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def isInited():
    """
    This function can be used when the caller application wants to know if API is initialized.

    Returns
    -------
    DSPResult
        This function will return one of DSPResult enumeration value.
        If API is initialized, this call will return DSP_S_INITED.
        Otherwise DSP_S_NOT_INITED will be returned.

    """
    result = imonDll.IMON_Display_IsInited()
    if result == DSPResult.DSP_S_INITED:
        return True
    return False

def isPluginModeEnabled():
    """
    This function can be used when the caller application wants to know if API can control iMON display.

    Returns
    -------
    DSPResult
        This function will return one of DSPResult enumeration value.
        If API can control iMON display, this call will return DSP_S_IN_PLUGIN_MODE.
        Otherwise DSP_S_NOT_IN_PLUGIN_MODE will be returned.

    """
    result = imonDll.IMON_Display_IsPluginModeEnabled()
    if result == DSPResult.DSP_S_IN_PLUGIN_MODE:
        return True
    return False

# VFD Functions ###################################

def setVfdText(line1, line2):
    """
    This function can be used when the caller application wants to display text data on VFD module.

    Parameters
    ----------
        line1 : string
            This string data will be displayed on the 1st line of VFD module.
        line2 : string
            This string data will be displayed on the 2nd line of VFD module.

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
        DSP_E_POINTER, DSP_E_NOT_INITED or DSP_E_FAIL can be raised if failed.

    Notes
    -----
        It doesn't support multi-byte character and if string data is longer than 16 characters, it displays 16 characters from the first.
        The iMON API asks for LPCTSTR types passed, but that isn't available in ctypes so I'm using LPCSTR instead. Don't know
        if that will cause issues.

    """
    result = imonDll.IMON_Display_SetVfdText(LPCSTR(line1), LPCSTR(line2))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setVfdEqData(eqData):
    """
    This function can be used when the caller application wants to display equalizer data on VFD module.

    Parameters
    ----------
    eqData: dict
        Accepts a dictionary container bands 1 - 16. for example:{1: 14, 2: 50, etc...}

    Notes
    -----
    Any missing bands not defined will be defaulted to 0. Each band should range from 0 - 100. The key for each being 1 - 16
    (starts at 1 not 0)

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
        DSP_E_POINTER, DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.

    """
    cEqData = bandInfoToCType(eqData)
    dspEqData = DSPEQDATA(cEqData)
    result = imonDll.IMON_Display_SetVfdEqData(byref(dspEqData))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

# LCD Functions ###################################

def setLcdText(line):
    """
    This function can be used when the caller application wants to display text data on LCD module.

    Parameters
    ----------
        line : string
            This string data will be displayed on the LCD module.

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
        DSP_E_POINTER, DSP_E_NOT_INITED or DSP_E_FAIL can be raised if failed.

    Notes
    -----
        It supports multi-byte character and if string data is longer than display area, it will start to scroll.
        When text scrolling is finished, API will notify it with DSPNotifyCode enumeration value, DSPNM_LCD_TEXT_SCROLL_DONE.
        The iMON API asks for LPCTSTR types passed, but that isn't available in ctypes so I'm using LPCSTR instead. Don't know
        if that will cause issues.

    """
    result = imonDll.IMON_Display_SetLcdText(LPCSTR(line))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdAllIcons(state):
    """
    This function can be used when the caller application wants to turn on/off all icons on LCD module.

    Parameters
    ----------
        state : bool
            If this value is TRUE, iMON will turn on all icons. Otherwise, iMON will turn off all icons.

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
         DSP_E_NOT_INITED or DSP_E_FAIL can be raised if failed.

    """
    result = imonDll.IMON_Display_SetLcdAllIcons(BOOL(state))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdOrangeIcon(peel=False, slice1=False, slice2=False, slice3=False, slice4=False, slice5=False, slice6=False, slice7=False, slice8=False):
    """
    This function can be used when the caller application wants to turn on/off orange shaped disk icons on the upper left part of LCD module.
    Disk icons consist of 8 pieces of orange and orange peel.

    Parameters
    ----------
    peel : bool
        turns on of off the peel like icon on the display
    slice1 : bool
        turns on or off the first slice of the orange thingy
    slice2 : bool
        turns on or off the second slice of the orange thingy
    slice3 : bool
        turns on or off the third slice of the orange thingy
    slice4 : bool
        turns on or off the fourth slice of the orange thingy
    slice5 : bool
        turns on or off the fifth slice of the orange thingy
    slice6 : bool
        turns on or off the sixth slice of the orange thingy
    slice7 : bool
        turns on or off the seventh slice of the orange thingy
    slice8 : bool
        turns on or off the eighth slice of the orange thingy

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
        DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.

    """
    # No Idea if this will work.
    slices = [slice1, slice2, slice3, slice4, slice5, slice6, slice7, slice8]
    peel = [peel, False, False, False, False, False, False, False]
    byte1 = int(''.join([str(int(x)) for x in slices]), 2)
    byte2 = int(''.join([str(int(x)) for x in peel]), 2)
    result = imonDll.IMON_Display_SetLcdOrangeIcon(BYTE(byte1), BYTE(byte2))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdMediaTypeIcon(music=False, movie=False, photo=False, cd=False, tv=False, web=False, news=False):
    """
    This function can be used when the caller application wants to turn on/off media type icons on the upper part of LCD module.

    Parameters
    ----------
    music : bool
    movie : bool
    photo : bool
    cd : bool
    tv : bool
    web : bool
    news : bool

    Notes
    -----
    Each bit represents one of media type icons. From MSB each bit represents MUSIC, MOVIE, PHOTO, CD/DVD, TV, WEBCASTING and NEWS/WEATHER icon.\n

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
        DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.

    """
    # No Idea if this will work.
    bits = [music, movie, photo, cd, tv, web, news, False]
    byte = int(''.join([str(int(x)) for x in bits]), 2)
    result = imonDll.IMON_Display_SetLcdMediaTypeIcon(BYTE(byte))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdSpeakerIcon(l=False, c=False, r=False, sl=False, lfe=False, sr=False, spdif=False, rr=False):
    """
    This function can be used when the caller application wants to turn on/off speaker icons on the upper right part of LCD module.

    Parameters
    ----------
    l : bool
        Left Speaker
    c : bool
        Center Speaker
    r : bool
        Right Speaker
    sl : bool
        Surrount Left
    lfe : bool
        Subwoofer
    sr : bool
        Surround Right
    spdif : bool
        SPDIF Digital
    rr : bool
        I don't know.

    Notes
    -----
    (byte 1)Each bit represents one of speaker icons.\nFrom MSB each bit represents L, C, R, SL, LFE, SR, RL and SPDIF icon.
    (byte 2)MSB represents RR icon. Other bits are not used.

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
        DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.

    """
    # No Idea if this will work
    bits1 = [l, c, r, sl, lfe, sr, spdif]
    bits2 = [rr, False, False, False, False, False, False, False]
    byte1 = int(''.join([str(int(x)) for x in bits1]), 2)
    byte2 = int(''.join([str(int(x)) for x in bits2]), 2)
    result = imonDll.IMON_Display_SetLcdSpeakerIcon(BYTE(byte1), BYTE(byte2))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdVideoCodecIcon(mpg=False, divx=False, xvid=False, wmv=False, mp3=False, ac3=False, dts=False, wma=False):
    """
    This function can be used when the caller application wants to turn on/off codec icons for video file on the lower part of LCD module.

    Parameters
    ----------
    mpg : bool
    divx : bool
    xvid : bool
    wmv : bool
    mp3 : bool
    ac3 : bool
    dts : bool
    wma : bool

    Notes
    -----
    Each bit represents one of video codec icons. From MSB each bit represents MPG, DIVX, XVID, WMV, MPG, AC3, DTS and WMA icon.
    Note there looks to be some error in the documentation, there are 2 entries for MPG. I made a guess here and used the second
    'MPG' as 'MP3' instead. Don't know if that is right, but the last bits seem to be audio related.

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
        DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.

    """
    # No Idea if this will work.
    bits = [mpg, divx, xvid, wmv, mp3, ac3, dts, wma]
    byte = int(''.join([str(int(x)) for x in bits]), 2)
    result = imonDll.IMON_Display_SetLcdVideoCodecIcon(BYTE(byte))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdAudioCodecIcon(mp3=False, ogg=False, wma=False, wav=False):
    """
    This function can be used when the caller application wants to turn on/off codec icons for audio file on the lower part of LCD module.

    Paremeters
    ----------
    mp3 : bool
    ogg : bool
    wma : bool
    wav : bool

    Notes
    -----
    Each bit represents one of audio codec icons. From MSB each bit represents MP3, OGG, WMA and WAV icon.

    Raises
    -------
    Exception
        DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.*/

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    """
    # No Idea if this works
    bits = [mp3, ogg, wma, wav, False, False, False, False]
    byte = int(''.join([str(int(x)) for x in bits]), 2)
    result = imonDll.IMON_Display_SetLcdAudioCodecIcon(BYTE(byte))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdAspectRatioIcon(src=False, fit=False, tv=False, hdtv=False, scr1=False, scr2=False):
    """
    This function can be used when the caller application wants to turn on/off aspect ratio icons on the lower right part of LCD module.

    Parameters
    ----------
    src : bool
    fit : bool
    tv : bool
    hdtv : bool
    scr1 : bool
    scr2 : bool

    Raises
    -------
    Exception
        DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Notes
    -----
    Each bit represents one of aspect ratio icons. From MSB each bit represents SRC, FIT, TV, HDTV, SCR1 and SCR2 icon.

    """
    # No Idea if this works
    bits = [src, fit, tv, hdtv, scr1, scr2, False, False]
    byte = int(''.join([str(int(x)) for x in bits]), 2)
    result = imonDll.IMON_Display_SetLcdAspectRatioIcon(BYTE(byte))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdEtcIcon(repeat=False, shuffle=False, alarm=False, rec=False, vol=False, time=False):
    """
    This function can be used when the caller application wants to turn on/off icons on the lower left part of LCD module.

    Parameters
    ----------
    repeat : bool
    shuffle : bool
    alarm : bool
    rec : bool
    vol : bool
    time : bool

    Raises
    -------
    Exception
        DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.



    Notes
    -----
    Each bit represents icon. From MSB each bit represents REPEAT, SHUFFLE, ALARM, REC, VOL and TIME icon.

    """
    # No Idea if this works
    bits = [repeat, shuffle, alarm, rec, vol, time, False, False]
    byte = int(''.join([str(int(x)) for x in bits]), 2)
    result = imonDll.IMON_Display_SetLcdEtcIcon(BYTE(byte))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

def setLcdProgress(progress, total):
    """
    This function can be used when the caller application wants to display progress bar on the upper and lower left part of text area of LCD module.

    Parameters
    ----------
    progress : int
        It represents the current position of progress bar.
    total : int
        It represents the total length of progress bar.

    Raises
    ------
    Exception
        DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    """
    # Should work
    result = imonDll.IMON_Display_SetLcdProgress(c_int(progress), c_int(total))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name

imonDll.IMON_Display_SetLcdEqData.argtypes = [POINTER(DSPEQDATA), POINTER(DSPEQDATA)]
imonDll.IMON_Display_SetLcdEqData.restype = DSPResult

def setLcdEqData(eqDataLeft, eqDataRight):
    """
    This function can be used when the caller application wants to display equalizer data on LCD module.

    Parameters
    ----------
    eqDataLeft: dict
        Accepts a dictionary container bands 1 - 16 For the Left Channel. for example:{1: 14, 2: 50, etc...}
    eqDataRight: dict
        Accepts a dictionary container bands 1 - 16 For the Right Channel.

    Notes
    -----
    Any missing bands not defined will be defaulted to 0. Each band should range from 0 - 100. The key for each being 1 - 16
    (starts at 1 not 0)

    Returns
    -------
    DSPResult
        DSP_SUCCEEDED will be returned if succeeded.

    Raises
    ------
    Exception
        DSP_E_POINTER, DSP_E_NOT_INITED or DSP_E_FAIL can be returned if failed.

    Example
    -------
    >>>setLcdEqData({1:21, 2:13, 3:10}, {14:21, 15:13, 16:10})

    """
    cEqDataLeft = bandInfoToCType(eqDataLeft)
    cEqDataRight = bandInfoToCType(eqDataRight)
    dspEqDataLeft = DSPEQDATA(cEqDataLeft)
    dspEqDataRight = DSPEQDATA(cEqDataRight)

    result = imonDll.IMON_Display_SetLcdEqData(byref(dspEqDataLeft), byref(dspEqDataRight))
    if (result == DSPResult.DSP_SUCCEEDED):
        return result
    raise Exception, result.name


###################################

#print("init:", init())
#print("unInit:", unInit())
#print("isInited:", isInited())
#print("isPluginModeEnabled:", isPluginModeEnabled())
#setVfdText("test", "test")
#setLcdText("test");
#setLcdAllIcons(True)
#setLcdOrangeIcon()
#setLcdMediaTypeIcon()
#setLcdSpeakerIcon()
#setLcdVideoCodecIcon()
#setLcdAudioCodecIcon()
#setLcdAspectRatioIcon()
#setLcdEtcIcon()
#setLcdProgress(5, 100)
#setVfdEqData({1:21, 2:13, 3:10})
#setLcdEqData({1:21, 2:13, 3:10}, {1:21, 2:13, 3:10})
