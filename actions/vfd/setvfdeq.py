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
            if self.plugin.imon.isInited() and self.plugin.imon.isPluginModeEnabled():
                result = self.plugin.imon.setVfdEqData(eqdata)
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
