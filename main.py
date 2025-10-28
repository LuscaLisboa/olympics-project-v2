import tkinter as tk

from ui.app import App


def main():
    root = tk.Tk()
    root.title("Olympics-project-v2")
    root.geometry("1100x700")
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()