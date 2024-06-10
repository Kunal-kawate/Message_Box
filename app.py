import streamlit as st
import dropbox
import random

# VS environment path D:\Final_Proejcts\QR_Gen\.venv\Scripts\python.exe -m 

headers = {
    'authorization' : st.secrets['API_KEY'],
    'content-type': 'application/json'
}

TOKEN = headers["authorization"]

dbx = dropbox.Dropbox(TOKEN) 

def list_files_in_folder(): 
    file_list = []
    # dbx = dropbox.Dropbox(TOKEN) 
    try: 
        folder_path = "/MAIN"
        files = dbx.files_list_folder(folder_path).entries   
        for file in files: 
            file_list.append(file.name) 
        return file_list      
    except Exception as e: 
        print(str(e))

def read_from_dropbox(dropbox_path):
    try:
        metadata, res = dbx.files_download(dropbox_path)
        content = res.content.decode('utf-8')
        return content
    except dropbox.exceptions.ApiError as err:
        print(f'Failed to download {dropbox_path} -- {err}')
        return None
    
def create_text_file_on_dropbox(file_content, dropbox_path):
    try:
        file_bytes = file_content.encode('utf-8')
        dbx.files_upload(file_bytes, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        print(f'File created on Dropbox at {dropbox_path} with specified content.')
    except dropbox.exceptions.ApiError as err:
        print(f'Failed to create file at {dropbox_path} -- {err}')

def display_message_in_box(message,random_num_Text):
    if random_num_Text == 0:
        st.info(message)
    elif random_num_Text == 1:
        st.success(message)
    elif random_num_Text == 2:
        st.warning(message)
    elif random_num_Text == 3:
        st.error(message)

def main():
    st.set_page_config(layout="centered")
    st.title("Kunya.Thing ")
    st.sidebar.title("About")
    st.sidebar.write("""
Welcome to my special corner of the web! 🌟 Here, friends, family, and well-wishers can share their thoughts, memories, and funny incidents about me. 💬 Whether it's a cherished moment we've shared, a hilarious story that makes you laugh every time 😂, or simply a heartfelt message ❤️, this is your space to express it.
""")
    st.sidebar.write('**Your identity remains a secret, so feel free to share without any worries!** 🤫✨')
    st.write("From Memories to Moments: Your Stories Here ⬇️")


    # ----------read and print existed data-------------------
    files = list_files_in_folder()

    for file_name in files:
        name = '/MAIN/' + file_name
        content = read_from_dropbox(name)
        random_num_Text = random.randint(0,3)
        display_message_in_box(content,random_num_Text )
    # ----------------end------------------------------------

    # Text input at the bottom
    user_input = st.text_input("Write anything!", key="input", placeholder="Type your message here...")

    col1, col2 = st.columns([1, 5])
    
    with col1:
        send_button = st.button("Save")
    
    with col2:
        re_fresh_button = st.button("Refresh")

    if send_button and user_input:
        randome_file_name = str(random.randint(0,100))
        while True:
            if randome_file_name not in files:
                break
            else:
                randome_file_name = str(random.randint(0,100))

        dropbox_path = '/MAIN/'+randome_file_name+'.txt'
        create_text_file_on_dropbox(user_input, dropbox_path)
        

    if re_fresh_button:
        st.session_state.clear()

if __name__ == "__main__":
    main()
