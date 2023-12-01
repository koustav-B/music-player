import os
import random
import pygame

def list_music_files(music_folder):
    return [file for file in os.listdir(music_folder) if file.endswith((".mp3", ".wav"))]

def print_song_info(music_file):
    try:
        import eyed3
        audiofile = eyed3.load(music_file)
        if audiofile.tag:
            return f"Artist: {audiofile.tag.artist}, Title: {audiofile.tag.title}"
    except ImportError:
        pass
    return os.path.basename(music_file)

def play_music(music_folder, repeat_mode=False, random_playback=False):
    music_files = list_music_files(music_folder)

    if not music_files:
        print("No music files found in the folder.")
        return

    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)

    while True:
        if not music_files:
            print("No more music files in the playlist.")
            if repeat_mode:
                music_files = list_music_files(music_folder)
            else:
                break

        if random_playback:
            random.shuffle(music_files)

        random_music_file = os.path.join(music_folder, music_files.pop(0))
        print(f"Playing: {print_song_info(random_music_file)}")

        pygame.mixer.music.load(random_music_file)
        pygame.mixer.music.play()

        while True:
            action = input("Enter 'p' to pause, 'r' to resume, 'v' to change volume, 'n' for the next track, 'q' to quit: ").lower()
            if action == 'p':
                pygame.mixer.music.pause()
            elif action == 'r':
                pygame.mixer.music.unpause()
            elif action == 'v':
                new_volume = float(input("Enter the volume (0.0 to 1.0): "))
                if 0.0 <= new_volume <= 1.0:
                    pygame.mixer.music.set_volume(new_volume)
                else:
                    print("Invalid volume. Volume should be between 0.0 and 1.0.")
            elif action == 'n':
                pygame.mixer.music.stop()
                break
            elif action == 'q':
                pygame.mixer.music.stop()
                pygame.quit()
                exit()

if __name__ == '__main__':
    music_folder = input("Enter the directory where your music files are located: ")
    if not os.path.exists(music_folder) or not os.path.isdir(music_folder):
        print("Invalid directory. Please provide a valid directory path.")
        exit()

    repeat_mode = input("Enable Repeat Mode? (y/n): ").lower() == 'y'
    random_playback = input("Enable Random Playback? (y/n): ").lower() == 'y'

    play_music(music_folder, repeat_mode, random_playback)
