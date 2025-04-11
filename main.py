import streamlit as st 
from get_info import download_album_info
import os
from PIL import Image
from get_info import SEP
FOLDER = 'image'

def generate_tag(s:str):
    # 生成标签
    if s.endswith('.jpg'):
        s = s[:-4]
    tags = s.split(SEP)
    album_id, album_name, album_author = tags
    return f"{album_name}\n{album_author}"

def image_to_base64(img):
    from io import BytesIO
    import base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def music_board():
    st.divider()
    image_files = os.listdir(FOLDER)
    # 每行显示3张图片
    cols = st.columns(4)

    for idx, image_file in enumerate(image_files):
        with cols[idx % 4]:
            try:
                img = Image.open(os.path.join(FOLDER, image_file))
                st.image(img, caption=generate_tag(image_file))
                album_id = image_file.split(SEP)[0]
            except Exception as e:
                st.error(f"无法加载图片 {image_file}: {e}")


def title():
    global ipt_id
    st.write("输入网易云歌曲分享链接URL中专辑ID")
    ipt_id = st.text_input("输入专辑ID", placeholder="example:21302")
    if ipt_id:
        # print(ipt_url)
        # album_id = ipt_url[ipt_url.index('id=')+3:]
        # print(album_id)
        # album_id = '21302'
        album_url = f"https://music.163.com/album?id={ipt_id}" 
        download_album_info(album_url, ipt_id)
        
def sidebar():
    with st.sidebar:
        st.title("专辑ID获取方式")
        st.subheader("网页端")
        img = Image.open(os.path.join('guide', 'g1.png'))
        st.image(img, caption="网页端获取方式")
        st.subheader("手机端")
        img = Image.open(os.path.join('guide', 'g2.jpg'))
        st.image(img, caption="手机端获取方式")
        st.markdown('''
                    - 复制到的文本内容：分享陈绮贞的专辑《Groupies吉他手》: http://music.163.com/album/21302/?userid=1904702393 (来自@网易云音乐)
                    - 其中`21302`即为专辑ID
                    ''')
        st.write("可能有时候会有bug，大家见谅😀")
        
        
st.set_page_config(page_title="MusicBoard", layout="wide")

pg = st.navigation([
    st.Page(music_board, title='MusicBoard', icon="🤗")
])

ipt_id = None

st.title("MusicBoard")
title()
sidebar()


pg.run()