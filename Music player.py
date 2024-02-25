import tkinter as tk
import os
import threading
import winsound

class MusicPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")

        self.current_folder = None
        self.playlist = []
        self.current_index = 0
        self.playing_thread = None

        self.play_button = tk.Button(master, text="Play", command=self.play_music)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_music, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.select_folder_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(side=tk.LEFT, padx=10)

    def select_folder(self):
        folder_selected = tk.filedialog.askdirectory()
        if folder_selected:
            self.current_folder = folder_selected
            self.load_playlist()

    def load_playlist(self):
        self.playlist = []
        if self.current_folder:
            for file in os.listdir(self.current_folder):
                if file.endswith(".wav"):
                    self.playlist.append(os.path.join(self.current_folder, file))

    def play_music(self):
        if not self.playlist:
            tk.messagebox.showinfo("Error", "No music files found in selected folder.")
            return

        if self.playing_thread is None or not self.playing_thread.is_alive():
            self.playing_thread = threading.Thread(target=self.play_music_thread)
            self.playing_thread.start()

    def play_music_thread(self):
        self.play_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        for i in range(self.current_index, len(self.playlist)):
            winsound.PlaySound(self.playlist[i], winsound.SND_FILENAME | winsound.SND_ASYNC)
            # Wait until the current song finishes playing or the user stops the music
            while winsound.PlaySound(None, winsound.SND_PURGE) == 0:
                if self.playing_thread is None or not self.playing_thread.is_alive():
                    break
            self.current_index = i + 1

        self.play_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def stop_music(self):
        if self.playing_thread and self.playing_thread.is_alive():
            self.playing_thread.join()
            self.playing_thread = None
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
