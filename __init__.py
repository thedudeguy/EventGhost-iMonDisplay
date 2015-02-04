import eg

eg.RegisterPlugin(
    name = "IMON Display",
    author = "Chris Churchwell",
    version = "0.0.1",
    kind = "remote",
    description = "Connects to the IMON Manager as a plugin in order to take control of the VFD/LCD Display. IMON Manager must be running.",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADWElEQVQ4jS3By09cZRgH"
        "4N/7fufMOXMOM3POwDDcq0ViL6EGGoob0k1jYoJumpgYiDvTxGhd6R9homvjbeGmi+pO"
        "dwZtRCMW0wpULlKQCgwUmDJXzvV73fg8VPLzqNbbyJgms2G4ArrmFfKvFf3iVNbJDmgR"
        "3W41t0+q1R/r9eZ3huKHUdAOtJBYhoAMw4BSirVIT9Z2Zs+/MDJ74crEcOm5UcvKdZGI"
        "4Oz0UPYfP2yv/bmw+mRn58skDr+FoKpFRFmmQXGSlJMk+aDAwa3X33p/QF18wzC7Rijj"
        "doLdEsQfgdU7pjr9fLm6u3q1VjsFCMsEHaps1naCMJrJAu9Mv/eRvzl0m691HuDFfJU8"
        "I0CHEeBysQmBiRV3mgfsU2f1j59GtNZbXsHfUFEkL5nQH16dunG+ef1TNVO+h4u5E8rl"
        "i2Q4PuXcLA335qibD1FOt2jBexul6pxb2X2SO4v0rwqgN/sduenNfGON+g16ObdOyi1j"
        "sLeEgU6bejxbMgYjTDTO5QPsHEc4Kt2g8JfP8m2dLnOG0snS0GBHUBrDhLuCjFuE6zgg"
        "IiJiEAkpJjJMA6G2MOk+QloeR3mwq0jAOLuO0Zfvu0RCIF81SZkWERHhf8wMAYEBSgHy"
        "jDaEgNy5UdNi9DMpShgxQACLgBhC0BARiAjSVEMkASsCaQi0BhgwJZZII+YwUY/PDv9O"
        "rAyw1bAkbzFEWAABAIhoiAZ0KuJlCdv1DOwM0KhsBBrY4lYQz1cOj6qlvTn8jFeIW3vw"
        "fZt0StCAQESEFQodWUqbTzCvXpXi3hwq+0/3ASwqiLTCVC57rb+e96/f5u1jxrizIYN9"
        "PXBtG1nLRHeHoH6wJl+sXUCrYwjbX90MN3cOvofK3FGO4zbPgrDRrD0byx795jvjt/iR"
        "XEGrdoQ0buG4FmLxX8Ld40mcxjlsfj6dLC8uLCWp/riQc9ZVrLVWRJV2lLRqh7vD8dYP"
        "eaVEPeVLtB4NYanmYW0vQuX3u3rlzrvByoP7S0EYf6IU3zsLk4iYGRAhYc5Jmk4Zpj1b"
        "9L1Jr9TdZWcLGRCk2TgNGyeVg+qz+nyaxF8bBi8miW53egWQbduIoghETEopM9W6X4tM"
        "MNE4EQ0A0FrLP4DcJ+IHhsEHcRSlAISZ8B9r7Ju1EcqVkQAAAABJRU5ErkJggg==)"
    )

)

from eg.WinApi.Dynamic import RegisterWindowMessage
import imon
from imon import DSPNotifyCode, DSPNInitResult, DSPType

# Registers a custom message type for the windows event system
WM_IMON_DISPLAY = RegisterWindowMessage("IMON_DISPLAY")

class imonHandler(object):

    def __init__(self, plugin):
        self.plugin = plugin

    def handle(self, notifyCode, payload):
        try:
            notify = getattr(self, notifyCode.name)
        except AttributeError:
            self.plugin.PrintError("Unhandled Display Notification: " + str(notifyCode.name))
        else:
            notify(payload)

    def DSPNM_PLUGIN_SUCCEED(self, payload):
        displayType = DSPType(payload)
        self.plugin.TriggerEvent("imon.connected")

    def DSPNM_PLUGIN_FAILED(self, payload):
        cause = DSPNInitResult(payload)
        self.plugin.PrintError("iMON Plugin Failure: " + str(cause.name))
        self.plugin.TriggerEvent("failure")

    def DSPNM_IMON_RESTARTED(self, payload):
        displayType = DSPType(payload)
        self.plugin.TriggerEvent("imon.restarted", str(displayType.name))

    def DSPNM_IMON_CLOSED(self, payload):
        self.plugin.TriggerEvent("imon.disconnected")

    def DSPNM_HW_CONNECTED(self, payload):
        displayType = DSPType(payload)
        self.plugin.TriggerEvent("hardware.connected")

    def DSPNM_HW_DISCONNECTED(self, payload):
        cause = DSPNInitResult(payload)
        self.plugin.TriggerEvent("hardware.disconnected")

    def DSPNM_LCD_TEXT_SCROLL_DONE(self, payload):
        self.plugin.TriggerEvent("scroll.complete")


class IMONDisplay(eg.PluginBase):
    """
    An EventGhost plugin in order to allow Event
    Ghost to take control of IMON Display Devices.

    This plugin connects to the IMON Manager software also running
    on the same computer, using the Display API.

    Notes
    -----
    IMON Manager must be running.

    """

    def __init__(self):
        """Constructor. Initializes the plugin."""
        self.imonHandler = imonHandler(self)
        # Set up actions
        vfdGroup = self.AddGroup(
            "VFD Displays",
            "Actions specifically for VFD Type Displays"
        )
        vfdGroup.AddAction(SetVfdText)

    def __start__(self):
        """Called when the plugin is actived."""
        # Set up the message receiver in order to watch for messages from imon manager
        eg.messageReceiver.AddHandler(WM_IMON_DISPLAY, self.imonWndProc)
        # Attempt to connect tp imon

        try:
            result = imon.init(eg.messageReceiver.hwnd, WM_IMON_DISPLAY)
            self.TriggerEvent("init", result.name)
        except Exception, msg:
            eg.PrintError("Unable to Initialize Display API: " + str(msg))

    def __stop__(self):
        """Called when the plugin is deactivated."""
        # Make sure to disconnect.
        try:
            result = imon.unInit()
            self.TriggerEvent("uninit", result.name)
        except Exception, msg:
            eg.PrintError(str(msg))

        #destroy the handler
        eg.messageReceiver.RemoveHandler(WM_IMON_DISPLAY, self.imonWndProc)

    def imonWndProc(self, dummyHwnd, dummyMesg, wParam=None, lParam=None):
        """
        A Windows Event Message Handler Callback. Processes events sent to the IMON_DISPLAY
        message name that were sent in from the IMON Manager.

        Notes
        -----
        The iMONDisplayAPI.h file contains all of the messages that can be sent.

        Paramaters
        ----------
        dummyHwnd: HWND
            Not used. A reference to the processing thread/window.
        dummyMesg: UINT
            Not used. A Reference to the message, contains the IMON_DISPLAY reference
            I believe.
        wParam : ???
            The first paramater of the message. This will be a DSPNotifyCode enum
        lParam : ???
            The second paramater of the message.

        """

        notifyCode = DSPNotifyCode(wParam)
        self.imonHandler.handle(notifyCode, lParam)

        return 1


class SetVfdText(eg.ActionBase):
    name = "Set VFD Text"
    description = "Displays Text on a VFD Display"
    iconFile = "icon_display"

    def __call__(self, line1="", line2=""):
        try:
            if imon.isInited() and imon.isPluginModeEnabled():
                imon.setVfdText(line1, line2)
            else:
                raise Exception, "Not Connected"
        except Exception, msg:
            self.PrintError("Unable to display text: " + str(msg))

    def Configure(self, line1="", line2=""):
        panel = eg.ConfigPanel()
        line1Control = wx.TextCtrl(panel, -1, line1)
        line2Control = wx.TextCtrl(panel, -1, line2)
        panel.sizer.Add(line1Control, 1, wx.EXPAND)
        panel.sizer.Add(line2Control, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                line1Control.GetValue(),
                line2Control.GetValue()
            )
