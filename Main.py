from tkinter import *
import  pygame

import os
import shutil

info=""
looping = 0
L=[]
ps=""

root = Tk()
root.title('Music Player')
root.resizable(False,False)
root.geometry('500x450')
root.iconbitmap('images.ico')
pygame.mixer.init()


    
def play ():
    global L
    global ps
    if not (play_list.curselection()):
        play_list.activate(0)
        play_list.selection_set(0)
       
    song = play_list.get(ACTIVE)
    
    for i in L:
        if (ps==i):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                play_b.configure(image=ipause_b)
                text_info.config(text= str(song)+" is paused")
            else:
                pygame.mixer.music.unpause()
                play_b.configure(image=iplay_b)
                text_info.config(text= "Now playing "+str(song))
        elif song in i :
                pygame.mixer.music.load(i)
                pygame.mixer.music.play(loops=looping)
                play_b.configure(image=iplay_b) 
                ps=i
                text_info.config(text= "Now playing "+str(song))
           

def copy_file_to_folder(source_file, destination_folder):
    # Check if the source file exists
    if not os.path.isfile(source_file):
        print(f"Error: Source file '{source_file}' does not exist.")
        return

    # Check if the destination folder exists
    if not os.path.exists(destination_folder):
        print(f"Error: Destination folder '{destination_folder}' does not exist.")
        return

    # Get the file name from the source file path
    file_name = os.path.basename(source_file)

    # Create the full destination file path by joining the destination folder with the file name
    destination_file = os.path.join(destination_folder, file_name)

    # Perform the copy operation
    shutil.copy(source_file, destination_file)

    print(f"File '{file_name}' copied to '{destination_folder}' successfully.")
    
def stop():
    pygame.mixer.music.stop()
    
def loop():
    global looping
    global info
    if pygame.mixer.music.get_busy():
        text_info.config(text="activate loop before playing the song")
        loop_b.config(borderwidth=3)
        root.after(1000, revert_text_label)        
        return
    info= text_info.cget("text")
    if (looping == 0):
        looping = -1
        text_info.config(text="loop on")
        loop_b.config(borderwidth=3)
        root.after(1000, revert_text_label)
    elif (looping == -1):
        looping =0
        text_info.config(text="loop off")
        loop_b.config(borderwidth=0)
        root.after(1000, revert_text_label)
    
def revert_text_label():
    global info
    print(info)
    text_info.config(text=info)    
  
def pause():
    
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        play_b.configure(image=ipause_b)
    else:
        pygame.mixer.music.unpause()
        play_b.configure(image=iplay_b)

def on_closing():
    stop()
    root.destroy()

def next_one():
    global L
    global ps
    if not (play_list.curselection()):
        return
    play_b.configure(image=iplay_b)
    next_song = play_list.curselection()
    next_song = next_song[0]+1
    if next_song >= len(L):
        next_song=0

    pygame.mixer.music.load(L[next_song])
    ps=L[next_song]
    pygame.mixer.music.play(loops=looping)       
    text_info.config(text= "Now playing "+play_list.get(next_song))
    play_list.selection_clear(0,END)
    play_list.activate(next_song)
    play_list.selection_set(next_song)
    
def back_one():
    global L
    global ps
    if not (play_list.curselection()):
        return
    play_b.configure(image=iplay_b)
    next_song = play_list.curselection()
    next_song = next_song[0]-1
    if next_song < 0 :
        next_song=len(L)-1

    pygame.mixer.music.load(L[next_song])
    ps=L[next_song]
    pygame.mixer.music.play(loops=looping)       
    text_info.config(text= "Now playing "+play_list.get(next_song))
    play_list.selection_clear(0,END)
    play_list.activate(next_song)
    play_list.selection_set(next_song)
    
def delete_file(file_path):
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return

        # Delete the file
        os.remove(file_path)

        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")
        
def add_ms():
    global L
    ch=""
    f=-1
    all_items = [play_list.get(idx) for idx in range(play_list.size())]
    song = filedialog.askopenfilenames(initialdir="Audio/",title="Chose a song",filetypes=(("mp3 Files","*.mp3"),))
    for i in song:
        for j in range(len(i)-1,0,-1):
            if (i[j]=='/'):
                break
            ch=ch+i[j]
        ch=ch[::-1]
        f=f+1
        if((song [f] in L) or (ch in all_items)):
            print("no")
            ch=""
        else:
            copy_file_to_folder(song [f],"Audio/")
            L.append("Audio/"+ch)
            play_list.insert(END , ch)
            ch=""
def del_s():
    global L
    if not (play_list.curselection()):
        return
    print(L)
    song = play_list.get(ACTIVE)
    L.remove("Audio/"+song)
    play_list.delete(ANCHOR)
    pygame.mixer.music.stop()
    delete_file("Audio/"+song)
def del_all():
    global L
    play_list.delete(0,END)
    for i in L:
        delete_file(i)
    L=[]
    print(L)
    pygame.mixer.music.stop()


men=Menu(root)
root.config(menu=men)

add_song = Menu(men, tearoff=False)
men.add_cascade(label="Music management",menu=add_song) 
add_song.add_command(label="delete All Musics",command=del_all)

play_list = Listbox(root, bg="black",fg="white",width=60,selectbackground="gray")
play_list.pack(pady=20)

iplay_b=PhotoImage(file='Icons/play.png')
ipause_b=PhotoImage(file='Icons/pause.png')
iloop_b=PhotoImage(file='Icons/repeat.png')
iforward_b=PhotoImage(file='Icons/skip-forward.png')
iback_b=PhotoImage(file='Icons/skip-back.png')
iplus_b=PhotoImage(file='Icons/file-plus.png')
iminus_b=PhotoImage(file='Icons/file-minus.png')

frame = Frame(root)
frame.pack()

back_b=Button(frame,image=iback_b,borderwidth=0,command=back_one)
back_b.grid(row=0,column=1 , padx=10)


play_b=Button(frame,image =iplay_b,borderwidth=0,command=play)
play_b.grid(row=0,column=2, padx=10)


loop_b=Button(frame,image =iloop_b,borderwidth=0,command=loop)
loop_b.grid(row=0,column=4, padx=10)

forward_b=Button(frame,image=iforward_b,borderwidth=0,command=next_one)
forward_b.grid(row=0,column=3, padx=10)

plus_b=Button(frame,image =iplus_b,borderwidth=0,command=add_ms)
plus_b.grid(row=2,column=2, padx=10)

del_b=Button(frame,image =iminus_b,borderwidth=0,command=del_s)
del_b.grid(row=2,column=3, padx=10)


text_info = Label(root,text="Welcome !")
text_info.pack(pady=20)

def init():
    ch=""
    f=-1
    folder_path = 'Audio/'
    # Get a list of files that match the pattern in the folder
    song =  [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    #print(song)
    for i in song:
        for j in range(len(i)-1,0,-1):
            
            if (i[j]== "/"):
                break
            ch=ch+i[j]
        ch=ch[::-1]
        f=f+1
        if(ch in L):
            pass
        else:
            L.append(song [f])
            
            play_list.insert(END , ch)
            ch=""
            
init()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


