"""
This module basically creates all the Enumerations from the iMONDisplayDefines.h file
which are used through the api.

Attributes
----------
DSPResult : ImonEnum
    These enumeration values represent the returned result for iMON Display API function calls.
    All iMON Display API function calls return one of this result values.
	For meaning of each result, refer the notes.
DSPNInitResult : ImonEnum
    These enumeration values represent the result status for requesting Display Plug-in Mode to iMON.
    iMON Display API notifies one of this result values to the caller application after requesting
    Display Plug-in Mode to iMON.
    For more information, refer the notes.
DSPType : ImonEnum
    These enumeration values represent display type.
    Currently iMON Display API supports VFD and LCD products.
DSPNotifyCode: ImonEnum
    These enumeration values represent the notification codes.
    iMON Display API will send or post message to the caller application.
    The caller application should assign the message and the winodw handle
    to receivce message with IMON_Display_Init fucntion.
    These enumeration values are used with WPARAM parameter of the message.
    For more information, see the explanation of each notification notes below.

Notes
-----
Each Enum has a meaning, here they are:

DSPResult
    DSP_SUCCEEDED
        Function Call Succeeded Without Error
	DSP_E_FAIL
        Unspecified Failure
	DSP_E_OUTOFMEMORY
        Failed to Allocate Necessary Memory
	DSP_E_INVALIDARG
        One or More Arguments Are Not Valid
	DSP_E_NOT_INITED
        API is Not Initialized
	DSP_E_POINTER
        Pointer is Not Valid
	DSP_S_INITED
        API is Initialized
	DSP_S_NOT_INITED
        API is Not Initialized
	DSP_S_IN_PLUGIN_MODE
        API Can Control iMON Display (Display Plug-in Mode)
	DSP_S_NOT_IN_PLUGIN_MODE
        API Can't Control iMON Display

DSPNInitResult
    DSPN_SUCCEEDED
        Display Plug-in Mode is Initialized Successfully
    DSPN_ERR_IN_USED
        Display Plug-in is Already Used by Other Application
    DSPN_ERR_HW_DISCONNECTED
        iMON HW is Not Connected
    DSPN_ERR_PLUGIN_DISABLED
        The Connected iMON HW doesn't Support Display Plug-in
    DSPN_ERR_PLUGIN_DISABLED
        Display Plug-in Mode Option is Disabled
    DSPN_ERR_IMON_NO_REPLY
        The Latest iMON is Not Installed or iMON Not Running
    DSPN_ERR_UNKNOWN
        Unknown Failure

DSPType
    DSPN_DSP_NONE
        No support devices
    DSPN_DSP_VFD
        VFD products
    DSPN_DSP_LCD
        LCD products

DSPNotifyCode
    DSPNM_PLUGIN_SUCCEED
        When API succeeds to get the control for the display, API will post caller-specified
        message with DSPNM_PLUGIN_SUCCEED as WPARAM parameter.
        LPARAM represents DSPType. This value can be 0x01 (VFD), 0x02 (LCD) or 0x03 (VFD+LCD).
    DSPNM_PLUGIN_FAILED
        When API fails to get the control for the display, API will post caller-specified
        message with DSPNM_PLUGIN_FAILED as WPARAM parameter.
        LPARAM represents error code with DSPNResult.
    DSPNM_IMON_RESTARTED
        When iMON starts, API will post caller-specified message
        with DSPNM_IMON_RESTARTED as WPARAM parameter.
        LPARAM represents DSPType. This value can be 0 (No Display),
        0x01 (VFD), 0x02 (LCD) or 0x03 (VFD+LCD).
    DSPNM_IMON_CLOSED
        When iMON closed, API will post caller-specified message with
        DSPNM_IMON_CLOSED as WPARAM parameter. LPARAM is not used.
    DSPNM_HW_CONNECTED
        When iMON HW newly connected, API will post caller-specified message with
        DSPNM_HW_CONNECTED as WPARAM parameter. LPARAM represents DSPType.
        This value can be 0 (No Display), 0x01 (VFD), 0x02 (LCD) or 0x03 (VFD+LCD).
    DSPNM_HW_DISCONNECTED
        When iMON HW disconnected, API will post caller-specified message
        with DSPNM_HW_DISCONNECTED as WPARAM parameter. LPARAM is DSPNResult
        value, DSPN_ERR_HW_DISCONNECTED.
    DSPNM_LCD_TEXT_SCROLL_DONE
        When iMON LCD finishes scrolling Text, API will post caller-specified message with
        DSPNM_LCD_TEXT_SCROLL_DONE as WPARAM parameter. The caller application may need to
        know when text scroll is finished, for sending next text. LPARAM is not used.

"""

from imon_enum import ImonEnum
from ctypes import Structure, c_int

DSPResult = ImonEnum(
    ('DSP_SUCCEEDED', 0),
    ('DSP_E_FAIL',),
    ('DSP_E_OUTOFMEMORY',),
    ('DSP_E_INVALIDARG',),
    ('DSP_E_NOT_INITED',),
    ('DSP_E_POINTER',),
    ('DSP_S_INITED', 0x1000),
    ('DSP_S_NOT_INITED',),
    ('DSP_S_IN_PLUGIN_MODE',),
    ('DSP_S_NOT_IN_PLUGIN_MODE',)
)

DSPNInitResult = ImonEnum(
    ('DSPN_SUCCEEDED', 0),
	('DSPN_ERR_IN_USED', 0x0100),
	('DSPN_ERR_HW_DISCONNECTED',),
	('DSPN_ERR_NOT_SUPPORTED_HW',),
	('DSPN_ERR_PLUGIN_DISABLED',),
	('DSPN_ERR_IMON_NO_REPLY',),
	('DSPN_ERR_UNKNOWN', 0x0200)
)

DSPType = ImonEnum(
	('DSPN_DSP_NONE', 0),
	('DSPN_DSP_VFD', 0x01),
	('DSPN_DSP_LCD', 0x02)
)

DSPNotifyCode = ImonEnum(
	('DSPNM_PLUGIN_SUCCEED', 0),
	('DSPNM_PLUGIN_FAILED',),
	('DSPNM_IMON_RESTARTED',),
	('DSPNM_IMON_CLOSED',),
	('DSPNM_HW_CONNECTED',),
	('DSPNM_HW_DISCONNECTED',),
	('DSPNM_LCD_TEXT_SCROLL_DONE', 0x1000),
)

# a Type for a c_int array 16
BANDINFO = c_int*16

def bandInfoToCType(bandInfo):
    """
    Converts a python dict band info (keys 1 -16) to a ctype int array
    """
    data = BANDINFO(
        (bandInfo[1] if 1 in bandInfo else 0),
        (bandInfo[2] if 2 in bandInfo else 0),
        (bandInfo[3] if 3 in bandInfo else 0),
        (bandInfo[4] if 4 in bandInfo else 0),
        (bandInfo[5] if 5 in bandInfo else 0),
        (bandInfo[6] if 6 in bandInfo else 0),
        (bandInfo[7] if 7 in bandInfo else 0),
        (bandInfo[8] if 8 in bandInfo else 0),
        (bandInfo[9] if 9 in bandInfo else 0),
        (bandInfo[10] if 10 in bandInfo else 0),
        (bandInfo[11] if 11 in bandInfo else 0),
        (bandInfo[12] if 12 in bandInfo else 0),
        (bandInfo[13] if 13 in bandInfo else 0),
        (bandInfo[14] if 14 in bandInfo else 0),
        (bandInfo[15] if 15 in bandInfo else 0),
        (bandInfo[16] if 16 in bandInfo else 0)
    )
    return data

class DSPEQDATA(Structure):
    """
    Data Struct to return data back to the IMON API
    This structure contains Equalizer data for 16 bands.
    @param	BandData    It represents Equalizer data for 16 bands. Its range is from 0 to 100.*/
    """
    _fields_ = [('BandData', BANDINFO)]
