class SetVfdText(eg.ActionBase):
    name = "Set VFD Text"
    description = "Displays Text on a VFD Display"
    iconFile = "icon_display"

    def __call__(self, line1="", line2=""):
        try:
            if self.plugin.imon.isInited() and self.plugin.imon.isPluginModeEnabled():
                result = self.plugin.imon.setVfdText(line1, line2)
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

