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
        vfdGroup.AddAction(SetVfdEqData)

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

class SetVfdEqData(eg.ActionBase):
    name = "Set VFD Equalizer"
    description = "Displays Equalizer Data on a VFD Display"
    iconFile = "icon_display"

    def __call__(self,
                 eq1=0,
                 eq2=0,
                 eq3=0,
                 eq4=0,
                 eq5=0,
                 eq6=0,
                  eq7=0,
                  eq8=0,
                  eq9=0,
                  eq10=0,
                  eq11=0,
                  eq12=0,
                  eq13=0,
                  eq14=0,
                  eq15=0,
                  eq16=0):
        eqdata = {
            1:eq1,
            2:eq2,
            3:eq3,
            4:eq4,
            5:eq5,
            6:eq6,
            7:eq7,
            8:eq8,
            9:eq9,
            10:eq10,
            11:eq11,
            12:eq12,
            13:eq13,
            14:eq14,
            15:eq15,
            16:eq16
        }
        try:
            if imon.isInited() and imon.isPluginModeEnabled():
                result = imon.setVfdEqData(eqdata)
                self.plugin.TriggerEvent("vfd.setVfdEqData")
            else:
                raise Exception, "Not Connected"
        except Exception, msg:
            self.PrintError("Unable to display eq: " + str(msg))

    def Configure(self,
                  eq1=0,
                  eq2=0,
                  eq3=0,
                  eq4=0,
                  eq5=0,
                  eq6=0,
                  eq7=0,
                  eq8=0,
                  eq9=0,
                  eq10=0,
                  eq11=0,
                  eq12=0,
                  eq13=0,
                  eq14=0,
                  eq15=0,
                  eq16=0):

        panel = eg.ConfigPanel()
        eqctl1 = panel.SpinIntCtrl(eq1, min=0, max=100)
        eqctl2 = panel.SpinIntCtrl(eq2, min=0, max=100)
        eqctl3 = panel.SpinIntCtrl(eq3, min=0, max=100)
        eqctl4 = panel.SpinIntCtrl(eq4, min=0, max=100)
        eqctl5 = panel.SpinIntCtrl(eq5, min=0, max=100)
        eqctl6 = panel.SpinIntCtrl(eq6, min=0, max=100)
        eqctl7 = panel.SpinIntCtrl(eq7, min=0, max=100)
        eqctl8 = panel.SpinIntCtrl(eq8, min=0, max=100)
        eqctl9 = panel.SpinIntCtrl(eq9, min=0, max=100)
        eqctl10 = panel.SpinIntCtrl(eq10, min=0, max=100)
        eqctl11 = panel.SpinIntCtrl(eq11, min=0, max=100)
        eqctl12 = panel.SpinIntCtrl(eq12, min=0, max=100)
        eqctl13 = panel.SpinIntCtrl(eq13, min=0, max=100)
        eqctl14 = panel.SpinIntCtrl(eq14, min=0, max=100)
        eqctl15 = panel.SpinIntCtrl(eq15, min=0, max=100)
        eqctl16 = panel.SpinIntCtrl(eq16, min=0, max=100)

        bandsBox = panel.BoxedGroup(
            "Bands (1-16)",
            ("Band 1", eqctl1),
            ("Band 2", eqctl2),
            ("Band 3", eqctl3),
            ("Band 4", eqctl4),
            ("Band 5", eqctl5),
            ("Band 6", eqctl6),
            ("Band 7", eqctl7),
            ("Band 8", eqctl8),
            ("Band 9", eqctl9),
            ("Band 10", eqctl10),
            ("Band 11", eqctl11),
            ("Band 12", eqctl12),
            ("Band 13", eqctl13),
            ("Band 14", eqctl14),
            ("Band 15", eqctl15),
            ("Band 16", eqctl16)
        )
        eg.EqualizeWidths(bandsBox.GetColumnItems(0))
        panel.sizer.Add(bandsBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                eqctl1.GetValue(),
                eqctl2.GetValue(),
                eqctl3.GetValue(),
                eqctl4.GetValue(),
                eqctl5.GetValue(),
                eqctl6.GetValue(),
                eqctl7.GetValue(),
                eqctl8.GetValue(),
                eqctl9.GetValue(),
                eqctl10.GetValue(),
                eqctl11.GetValue(),
                eqctl12.GetValue(),
                eqctl13.GetValue(),
                eqctl14.GetValue(),
                eqctl15.GetValue(),
                eqctl16.GetValue()
            )


class SetVfdText(eg.ActionBase):
    name = "Set VFD Text"
    description = "Displays Text on a VFD Display"
    iconFile = "icon_display"

    def __call__(self, line1="", line2=""):
        try:
            if imon.isInited() and imon.isPluginModeEnabled():
                result = imon.setVfdText(line1, line2)
                self.plugin.TriggerEvent("vfd.setVfdText")
            else:
                raise Exception, "Not Connected"
        except Exception, msg:
            self.PrintError("Unable to display text: " + str(msg))

    def Configure(self, line1="", line2=""):

        panel = eg.ConfigPanel()
        line1Control = panel.TextCtrl(line1)
        line2Control = panel.TextCtrl(line2)

        displayBox = panel.BoxedGroup(
            "Display Text",
            ("Line 1", line1Control),
            ("Line 2", line2Control),
        )
        eg.EqualizeWidths(displayBox.GetColumnItems(0))
        panel.sizer.Add(displayBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                line1Control.GetValue(),
                line2Control.GetValue()
            )
