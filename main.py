from tkinter import *
from pytube import YouTube, Playlist

# defining the main roles for the app
root = Tk()
root.title("Downloader App")
app_image = PhotoImage(file="app_icon.png") 
root.iconphoto(True,app_image)
root.geometry(newGeometry="500x500")
root.resizable(False, False)

# Variables
result_show = False
clear_clicked = False
radio_val = IntVar()
radio_resulition_val = StringVar()
radio_val.set(value=1)
radio_resulition_val.set(value="720p")
link_field = Entry(root, width=40)
result_label = Label(root, text="", fg="blue", padx=5, pady=5)
result_label.grid(row=10, column=3, padx=20, columnspan=10)
listbox = Listbox(root, selectmode=SINGLE, width=40, height=10,border=0,borderwidth=0)
onProgress_label = Label(root, text="", fg="#E3C46B")

scrollbar = Scrollbar(root, command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)


def on_download_click():
    global onProgress_label

    def on_progress_callback(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        onProgress_label.config(text=f"Downloading... {int(percentage)}%")

    if radio_val.get() == 1:
        down_type = "video"
    elif radio_val.get() == 2:
        down_type = "playlist"

    link = link_field.get()

    if link:
        if down_type == "video":
            ved_link = YouTube(link, on_progress_callback=on_progress_callback)
            ved_link.streams.get_by_resolution(radio_resulition_val.get()).download()
            print(f"{ved_link.title} is downloaded")
            result_text = f"{ved_link.title} is downloaded"
            listbox.insert(END, ved_link.title)
            return result_text
        elif down_type == "playlist":
            ved_link = Playlist(link)
            for video in ved_link.videos:
                video.streams.get_by_resolution(radio_resulition_val.get()).download(output_path=f"../{ved_link.title}")
                listbox.insert(END, video.title)
            result_text = f"{ved_link.title} is downloaded"
            return result_text
    else:
        print("Dosn't completed")
        onProgress_label.config(text="")
        return "Failed To Download ... try again"


def update_result_label():
    result_text = on_download_click()
    global clear_clicked
    if clear_clicked:
        result_label.config(text=result_text, bg="#333", fg="#FFF")
        result_label.grid(row=10, column=3, padx=20, columnspan=10)
    elif not clear_clicked:
        result_label.config(text=result_text, bg="#333", fg="#FFF")


def reset_all():
    link_field.delete(0, END)
    result_label.grid_remove()
    global clear_clicked
    clear_clicked = True
    global onProgress_label
    onProgress_label.config(text="")


# The design
Label(root, text="Downloader app makes it easy for you...", fg="green").grid(row=0, column=0, columnspan=5, pady=10,sticky="nsew")
onProgress_label.grid(row=0, column=6, sticky="nsew")
Radiobutton(root, text="Video", value=1, variable=radio_val, selectcolor="green").grid(row=1, column=3, )
Radiobutton(root, text="Playlist", value=2, variable=radio_val, selectcolor="green").grid(row=1, column=6)
link_field.grid(row=2, column=1, columnspan=10, padx=20)
Radiobutton(root, text="420p", value="420p", variable=radio_resulition_val, selectcolor="green").grid(row=2, column=11)
Radiobutton(root, text="720p", value="720p", variable=radio_resulition_val, selectcolor="green").grid(row=3, column=11)
download_button = Button(root, text="Download", fg="green", background="#FFF", padx=20, pady=10,
command=update_result_label, relief="solid")
download_button.grid(row=3, column=1, columnspan=4, pady=10, padx=5)
clear_button = Button(root, text="Clear", background="#FFF", fg="red", command=reset_all, padx=20, pady=10,
borderwidth=2, relief="solid")
clear_button.grid(row=3, column=4, columnspan=4, pady=10, padx=5)
listbox.grid(row=8, column=0, columnspan=10)

root.mainloop()