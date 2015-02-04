import time

class ShowTime(eg.ActionBase):
    name = "Show Time"
    description = "Displays Time"
    iconFile = "icon_display"

    def __call__(self):
        line1 = time.strftime("%x")
        line2 = time.strftime("%I:%M %p")
        try:
            if self.plugin.imon.isInited() and self.plugin.imon.isPluginModeEnabled():
                result = self.plugin.imon.setVfdText(line1, line2)
                self.plugin.TriggerEvent("vfd.setVfdText")
            else:
                raise Exception, "Not Connected"
        except Exception, msg:
            self.PrintError("Unable to display text: " + str(msg))
