print "Kalam startup macro file"

createDocument()

edmund = createMacro("edmund", open("edmund.py").read())
edmund.setMenuText("Edmund")
edmund.setText("Edmund")
edmund.setToolTip("Psychoanalyze Edmund")
edmund.setStatusTip("Psychoanalyze Edmund")
installMacro(edmund, kalam.macroMenu)

