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
