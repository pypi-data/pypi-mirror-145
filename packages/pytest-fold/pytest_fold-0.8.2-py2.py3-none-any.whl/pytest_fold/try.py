import TermTk as ttk

root = ttk.TTk()

logWin = ttk.TTkWindow(
    parent=root,
    pos=(10, 2),
    size=(80, 20),
    title="LogViewer Window",
    border=True,
    layout=ttk.TTkVBoxLayout(),
)
ttk.TTkLogViewer(parent=logWin)

btnShow = ttk.TTkButton(parent=root, text="Show", pos=(0, 0), size=(10, 3), border=True)
btnHide = ttk.TTkButton(parent=root, text="Hide", pos=(0, 3), size=(10, 3), border=True)

btnShow.clicked.connect(logWin.show)
btnHide.clicked.connect(logWin.hide)

root.mainloop()
