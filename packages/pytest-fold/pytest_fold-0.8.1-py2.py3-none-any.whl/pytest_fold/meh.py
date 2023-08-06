import TermTk as ttk

class TkTui:
    def __init__(self) -> None:
        self.root = ttk.TTk(layout=ttk.TTkGridLayout())
        self.summary_results = "test \033[42;1;30mANSI\033[44;1;33m TTkString"


    def create_top_frame(self) -> None:
        self.top_frame = ttk.TTkFrame(
            border=True,
        )
        self.top_label = ttk.TTkLabel(
            parent=self.top_frame,
            text=ttk.TTkString(self.summary_results),
        )

    def create_quit_button(self) -> None:
        self.quit_button_frame = ttk.TTkFrame(border=True)
        self.quit_button = ttk.TTkButton(
            parent=self.quit_button_frame,
            text="Quit",
            maxWidth=6,
        )
        self.quit_button.clicked.connect(self.root.quit)

    def create_main_frame(self) -> None:
        # Main frame to hold tab and text widgets
        self.main_frame = ttk.TTkFrame(
            border=False,
            layout=ttk.TTkVBoxLayout(),
        )

    def create_tabs(self) -> None:
        self.tab_widget = ttk.TTkTabWidget(border=True)
        tab_label = "Summary"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_area.setText("Blah blah blah")
        self.tab_widget.addTab(text_area, f" {tab_label} ")

    def do_layout(self) -> None:
        self.root.layout().addWidget(self.top_frame, 0, 0)
        # self.root.layout().addWidget(self.top_label, 0,0)
        self.root.layout().addWidget(self.quit_button_frame, 0, 1)
        self.root.layout().addWidget(self.quit_button, 0, 1)
        self.root.layout().addWidget(self.main_frame, 1, 0, 1, 2)
        self.root.layout().addWidget(self.tab_widget, 1, 0, 1, 2)


def main():
    tui = TkTui()

    tui.create_top_frame()
    tui.create_quit_button()
    tui.create_main_frame()
    tui.create_tabs()

    tui.do_layout()

    tui.root.mainloop()


if __name__ == "__main__":
    main()
