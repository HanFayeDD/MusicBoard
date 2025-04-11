import requests
from lxml import html
import os
from fake_useragent import UserAgent
from PIL import Image
import io
import streamlit as st
ua = UserAgent()

SEP = '_#'
def download_album_info(album_url, album_id, save_path='image'):
    # 设置请求头模拟浏览器访问
    h = ua.edge
    headers = {
        "User-Agent":h
    }
    print(h)

    try:
        response = requests.get(album_url, headers=headers)
        response.raise_for_status()
        print(response.status_code)
        # # 解析HTML
        with open(f"{album_id}.html", 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        tree = html.fromstring(response.text)
        
        
        # 获取专辑名字
        album_name_element = tree.xpath('//div[@class="tit"]/h2')[0].text
        print(album_name_element)
        # 获取专辑发行者
        album_name_author  = tree.xpath('//a[@class="s-fc7"]')[0].text
        print(album_name_author)
        # 获取专辑发行时间
        album_name_time = tree.xpath('//div[@class="topblk"]/p[@class="intr"][2]/text()')[0]
        print(album_name_time)   
        
        # 使用XPath获取封面图片URL
        img_element = tree.xpath('//div[@class="cover u-cover u-cover-alb"]/img')
        if not img_element:
            print("未找到封面图片元素，请检查XPath是否正确")
            return
            
        img_url = img_element[0].get('data-src')
        
        if not img_url:
            print("无法获取图片URL")
            return
    except:
        st.error('请稍后重试或输入的专辑ID有误', icon="🚨")   
        return 
    # 下载图片
    print(img_url)
    fname = f'{album_id}{SEP}{album_name_element}{SEP}{album_name_author}.jpg'
    img_data = requests.get(img_url, headers=headers).content
    file_name = os.path.join(save_path, fname)
    
    # 压缩图片
    try:
        # 将二进制数据转为Pillow图像对象
        img = Image.open(io.BytesIO(img_data))
        
        # 如果是PNG图片，转换为更高效的格式（如JPEG）
        if img.format == 'PNG':
            img = img.convert('RGB')  # 移除Alpha通道
            
        # 设置压缩质量（85%是常用值，范围1-100）
        img.save(file_name, quality=15, optimize=True)
        
        print(f"封面图片已压缩保存到: {file_name} (原始大小: {len(img_data)/1024:.1f}KB -> 新大小: {os.path.getsize(file_name)/1024:.1f}KB)")

    except Exception as e:
        # 如果压缩失败，回退到原始保存方式
        print(f"压缩失败，将保存原始图片: {e}")
        with open(file_name, 'wb') as f:
            f.write(img_data)
        
    # except Exception as e:
    #     print(f"发生错误: {e}")
    return (album_name_element, album_name_author, album_name_time)

# 使用示例
if __name__ == "__main__":
    album_id = '21257'
    album_url = f"https://music.163.com/album?id={album_id}" 
    download_album_info(album_url, album_id)

