from customtkinter import *
from tkinter import *
import os
from pygame import mixer
from PIL import Image
from queue import Queue
import time
import threading
from threading import Thread
from mutagen.mp3 import MP3
import random

# Initialize the appearance mode and default color theme
set_appearance_mode("System")
set_default_color_theme("blue")

class MusicPlayerApp(CTk,Tk):
    def __init__(self):
        super().__init__()

        # Function to check the state of switches periodically
        def check_switches():
            autoplay_state = self.switch_var_autoplay.get()
            repeat_state = self.switch_var_repeat.get()
            shuffle_state = self.switch_var_shuffle.get()

            if shuffle_state == "on":
                self.switch_repeat.configure(state=DISABLED)
                self.switch_autoplay.configure(state=DISABLED)
            elif repeat_state == "on":
                self.switch_autoplay.configure(state=DISABLED)
                self.switch_shuffle.configure(state=DISABLED)
            elif autoplay_state == "on":
                self.switch_shuffle.configure(state=DISABLED)
                self.switch_repeat.configure(state=DISABLED)
            else:
                self.switch_autoplay.configure(state=NORMAL)
                self.switch_repeat.configure(state=NORMAL)
                self.switch_shuffle.configure(state=NORMAL)

            app.after(1000, check_switches)

        # Initialize variables and the window
        self.music_paused = False
        self.music_stop = True
        self.current_music = None
        self.shuffle_mode =  False

        # ... (window setup code)
        set_appearance_mode("system")
        set_default_color_theme("blue")
        self.resizable(False,False)
        self.title("Darshan's mp3 music player")
        self.geometry("1080x720+260+40")
        mixer.init()

        # Create and configure various components of the music player interface
        # ... (frame setup, buttons, sliders, labels, etc.)

        # Frame
        self.frame = CTkFrame(master=self, corner_radius=10, width=560, height=550)
        self.frame.grid(row=0, column=0, padx=20, pady=10)
        self.frame.grid_propagate(False)

        # Frame Components
        
        # Logo Label
        self.logo_label = CTkLabel(self.frame, text="Mp3 Music Player", font=CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Browse button
        self.browse_button = CTkButton(self.frame, text="Browse Music", font=CTkFont(size=20, weight="bold"), width=400)
        self.browse_button.grid(row=1, column=0, padx=20, pady=20)

        # Scrollbar
        self.scroll = Scrollbar(self.frame)

        # Playlist
        new_font_size = 10
        self.playlist = Listbox(self.frame, width=90, height=20, bg="#333333", fg="grey",
                                selectbackground="lightblue", font=("arial", new_font_size, "bold"),
                                cursor="hand2", bd=0, yscrollcommand=self.scroll.set)

        # Scrollbar configuration
        self.scroll.configure(command=self.playlist.yview)
        self.scroll.grid(row=2, column=1, padx=(0, 20), pady=20, sticky="ns")
        self.playlist.grid(row=2, column=0, padx=(20, 0), pady=20)

        # Search entry
        self.search_entry = CTkEntry(master=self.frame, placeholder_text="Search Song")
        self.search_entry.grid(row=3, column=0, pady=10, padx=20, columnspan=3, sticky="nsew")

        # Search button
        search_image_path=os.path.join(os.path.dirname(__file__),"magnifying-glass.png")
        search_image = CTkImage(light_image = Image.open(search_image_path))
        self.search_button = CTkButton(self.frame, text="Search", font=CTkFont(size=16,weight="bold"), width=200,image=search_image)
        self.search_button.grid(row=4, column=0, padx=20, pady=10, columnspan=3)

        # Frame 1
        self.frame1 = CTkFrame(master=self, corner_radius=10, width=560, height=120)
        self.frame1.grid(row=1, column=0, padx=20, pady=10)
        self.frame1.grid_propagate(False)

        # Frame 1 Components

        # Apperance Mode
        optionmenu_var = StringVar(value="Dark")
        self.appearance_mode_optionemenu = CTkOptionMenu(self.frame1, values=["Light", "Dark", "System"],width=150,variable=optionmenu_var)
        self.appearance_mode_optionemenu.grid(row=1, column=0, pady=(10, 20))

         # Switches and Sliderself.
         # ... (repeat, autoplay, shuffle, volume etc...)
        self.switch_var_repeat = StringVar(value="off")
        self.switch_var_shuffle = StringVar(value="off")
        self.switch_var_autoplay = StringVar(value="off")
        self.switch_shuffle = CTkSwitch(self.frame1,text="Shuffle",variable=self.switch_var_shuffle,onvalue="on",offvalue="off",font=CTkFont(size=16,weight="bold"))
        self.switch_shuffle.grid(row=0,column=0,padx=40,pady=(10,20))
        self.switch_repeat = CTkSwitch(self.frame1,text="Repeat",variable=self.switch_var_repeat,onvalue="on",offvalue="off",font=CTkFont(size=16,weight="bold"))
        self.switch_repeat.grid(row=0,column=1,padx=30,pady=(10,20))
        self.switch_autoplay = CTkSwitch(self.frame1,text="Autoplay",variable=self.switch_var_autoplay,onvalue="on",offvalue="off",font=CTkFont(size=16,weight="bold"))
        self.switch_autoplay.grid(row=0,column=2,pady=(10,20))
        self.volume_button = CTkLabel(self.frame1,text="Volume",font=CTkFont(size=25,weight="bold"))
        self.volume_button.grid(row=1,column=1,pady=(10,20))
        self.slider=CTkSlider(self.frame1, from_=0, to=100,number_of_steps=100)
        self.slider.grid(row=1,column=2,padx=0,pady=(10,20))
        self.slider.set(100)
        threading.Thread(target=check_switches, daemon=True).start()

        # Image Label
        image_path = os.path.join(os.path.dirname(__file__),"p3.jpg")
        image = CTkImage(light_image = Image.open(image_path),size=(420,550))
        self.image_label = CTkLabel(self,image=image,text="")
        self.image_label.grid(row=0,column=1,pady=16)

        # Frame 2
        self.frame2 = CTkFrame(master=self, corner_radius=10, width=460, height=120)
        self.frame2.grid(row=1, column=1, pady=10,padx=20)
        self.frame2.grid_propagate(False)

        # Row and Column configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Buttons
        # ... (timer, progress_scale, play, pause, stop etc...)
        self.time_elapsed_label = CTkLabel(self.frame2,text="00:00",font=CTkFont(size=16, weight="bold"))
        self.time_elapsed_label.grid(row=0,column=0)
        self.progress_scale = CTkSlider(self.frame2,width=320,from_=0,to=100,number_of_steps=100)
        self.progress_scale.set(0)
        self.progress_scale.grid(row=0,column=1,columnspan=5,pady=20,sticky="w")


        left_image_path = os.path.join(os.path.dirname(__file__), "leftarrow.png")
        image = CTkImage(light_image=Image.open(left_image_path), size=(30, 30))
        self.left_button = CTkButton(self.frame2, image=image, text="", width=60, height=50)
        self.left_button.grid(row=1, column=1)

        pause_image_path = os.path.join(os.path.dirname(__file__),"pause.png")
        play_image_path = os.path.join(os.path.dirname(__file__),"Play.png")
        image1 = CTkImage(light_image = Image.open(play_image_path),size=(30,30))
        image2 = CTkImage(light_image = Image.open(pause_image_path),size=(30,30))
        self.play_pause_button = CTkButton(self.frame2,image=image1,text="",width=60,height=50) 
        self.play_pause_button.grid(row=1,column=2,padx=25)

        right_image_path = os.path.join(os.path.dirname(__file__), "rightarrow.png")
        image3 = CTkImage(light_image=Image.open(right_image_path), size=(30, 30))
        self.right_button = CTkButton(self.frame2, image=image3, text="", width=60, height=50)
        self.right_button.grid(row=1, column=3)

        stop_image_path = os.path.join(os.path.dirname(__file__), "stop.png")
        image4 = CTkImage(light_image=Image.open(stop_image_path), size=(30, 30))
        self.stop_button = CTkButton(self.frame2, image=image4, text="", width=60, height=50)
        self.stop_button.grid(row=1, column=0,padx=(20,25))

        Queue_image_path = os.path.join(os.path.dirname(__file__), "rightarrow.png")
        image5 = CTkImage(light_image=Image.open(Queue_image_path), size=(30, 30))
        self.queue_button = CTkButton(self.frame2, image=image5, text="", width=60, height=50)
        self.queue_button.grid(row=1, column=4,padx=(25,20))


        # Backend Functions
        # ... (add music, browse music, shuffle, play, pause etc...)

        # Browse music function
        def add_music():
            path = filedialog.askdirectory()
            if path and os.path.isdir(path):
                os.chdir(path)
                songs = os.listdir()

                for song in songs:
                    if song.endswith(".mp3"):
                        self.playlist.insert(END, song)

        for item in self.playlist.get(0, END):
            music_length = MP3(os.path.join(os.getcwd(), item)).info.length
            self.progress_scale.configure(to=int(music_length))
            break

        # Search songs function
        def search_song():
            song_to_find = self.search_entry.get().lower().split()  
            self.playlist.selection_clear(0, END)  

            for i in range(self.playlist.size()):
                song = self.playlist.get(i).lower()
                if all(word in song for word in song_to_find):
                    self.playlist.selection_set(i) 
                    self.playlist.activate(i)
                    self.playlist.see(i) 

        # Appearance mode function
        def change_appearance_mode_event(new_appearance_mode: str):
            set_appearance_mode(new_appearance_mode)
        
        # Converting seconds to minutes
        def convert_seconds_to_time(seconds):
            minutes, seconds = divmod(int(seconds), 60)
            hours, minutes = divmod(minutes, 60)
            return f"{minutes:02d}:{seconds:02d}"
        
        # Update progress scale according to music and autoplay and repeat songs function
        def update_progress_scale():
            if mixer.music.get_busy():
                song_length = MP3(os.path.join(os.getcwd(), self.current_music)).info.length
                current_time = mixer.music.get_pos() / 1000  

                progress_percentage = (current_time / song_length) * 100

                self.progress_scale.set(int(progress_percentage))
                self.time_elapsed_label.configure(text=convert_seconds_to_time(current_time))
                
                app.after(1000, update_progress_scale) 
                        
            elif self.music_paused:
                self.progress_scale.set(self.progress_scale.get())
                app.after(1000, update_progress_scale)

            else:
                self.progress_scale.set(0)
                self.time_elapsed_label.configure(text="00:00")

                if self.switch_var_autoplay.get() == "on" and not self.music_stop:
                    time.sleep(1)
                    play_next_song()

                elif self.switch_var_repeat.get() == "on" and not self.music_stop:
                    mixer.music.load(self.current_music)
                    mixer.music.play()
                    threading.Thread(target=update_progress_scale, daemon=True).start()

                else:
                    self.play_pause_button.configure(image=image1)
        
        # Play music function
        def play_music():
            if self.playlist.curselection():
                music_name = self.playlist.get(ACTIVE)
                if self.music_paused:
                    self.music_paused = False
                    mixer.music.unpause()
                    self.play_pause_button.configure(image=image2)  # Change icon to pause
                else:
                    if not mixer.music.get_busy():
                        mixer.music.load(music_name)
                        mixer.music.play()
                        self.play_pause_button.configure(image=image2)
                        self.current_music = music_name
                        self.music_stop = False
                        threading.Thread(target=update_progress_scale, daemon=True).start()
                    else:
                        self.music_paused = True
                        mixer.music.pause()
                        self.play_pause_button.configure(image=image1)
            else:
                print("Please select the music first")

        #Play next song
        def play_next_song():
            current_index = self.playlist.curselection()
            if current_index:
                next_index = (current_index[0] + 1) % self.playlist.size()
                self.playlist.selection_clear(0, END)
                self.playlist.selection_set(next_index)
                self.playlist.activate(next_index)
                self.playlist.see(next_index)
                    
                music_name1 = self.playlist.get(next_index)
                mixer.music.load(music_name1)
                mixer.music.play()
                self.current_music = music_name1
                self.music_stop = False
                threading.Thread(target=update_progress_scale, daemon=True).start()
                self.play_pause_button.configure(image=image2)
                self.music_paused = False
        
            else:
                print("First select the song")
        
        # Play previous song
        def play_previous_song():
            current_index = self.playlist.curselection()
            if current_index:
                previous_index = (current_index[0] - 1) % self.playlist.size()
                self.playlist.selection_clear(0, END)
                self.playlist.selection_set(previous_index)
                self.playlist.activate(previous_index)
                self.playlist.see(previous_index)
                
                music_name2 = self.playlist.get(previous_index)
                mixer.music.load(music_name2)
                mixer.music.play()
                self.current_music = music_name2
                self.music_stop = False
                threading.Thread(target=update_progress_scale, daemon=True).start()
                self.play_pause_button.configure(image=image2)
            else:
                print("First select the song")
        
        # Stop Music
        def stop_music():
            self.music_stop = True
            mixer.music.stop()
            self.play_pause_button.configure(image=image1)
            self.music_paused = False
            self.current_music = None
            self.time_elapsed_label.configure(text="00:00")

        # Display playing queue
        def display_queue():
            if mixer.music.get_busy():
                if self.switch_var_autoplay.get() == "on":
                    music_name = self.playlist.get(ACTIVE)
                    current_index = self.playlist.curselection()
                    next_index = (current_index[0] + 1) % self.playlist.size()
                    music_name1= self.playlist.get(next_index)
                    print("Current Song:",music_name)
                    print("Next Song to play",music_name1)
                    print("-------------------------------------------------------------------")
                elif self.switch_var_repeat.get() == "on": 
                    music_name = self.playlist.get(ACTIVE)
                    print("Current Song:",music_name)
                    print("Next Song to play:",music_name)
                    print("-------------------------------------------------------------------")
                else:
                    music_name = self.playlist.get(ACTIVE)
                    print("Current Song:",music_name)
                    print("-------------------------------------------------------------------")



            else:
                print("The queue is empty")
                print("-------------------------------------------------------------------")

        # Function to shuffle the songs
        def handle_shuffle_switch():
            global shuffle_mode
            if self.switch_var_shuffle.get() == "on" and not self.music_stop:
                shuffle_mode = True
                if not mixer.music.get_busy() and not self.music_paused:
                    index_to_play = random.randint(0, self.playlist.size()-1)
                    self.playlist.selection_clear(0, END)
                    self.playlist.selection_set(index_to_play)
                    self.playlist.activate(index_to_play)
                    self.playlist.see(index_to_play)
                    music_name3 = self.playlist.get(index_to_play)
                    mixer.music.load(music_name3)
                    time.sleep(0.5)
                    mixer.music.play()
                    self.current_music = music_name3
                    self.music_stop = False
                    threading.Thread(target=update_progress_scale, daemon=True).start()
                    self.play_pause_button.configure(image=image2)
                    self.music_paused = False
            else:
                shuffle_mode = False
            self.after(1000,handle_shuffle_switch)
        
        # Volume control
        def update_volume(value):
            volume = value / 100  
            mixer.music.set_volume(volume)  

        # Assingning functions to buttons
        self.play_pause_button.configure(command=play_music)
        self.right_button.configure(command=play_next_song)
        self.left_button.configure(command=play_previous_song)
        self.stop_button.configure(command=stop_music)
        self.queue_button.configure(command=display_queue)
        self.switch_shuffle.configure(command=handle_shuffle_switch)
        self.slider.configure(command=lambda value: update_volume(value))
        self.appearance_mode_optionemenu.configure(command=change_appearance_mode_event)
        self.browse_button.configure(command=add_music)
        self.search_button.configure(command=search_song)

if __name__ == "__main__":
    app = MusicPlayerApp()
    app.mainloop()
 
 
