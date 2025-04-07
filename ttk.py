import requests
import os
import random
#from playsound import playsound
from tinytag import TinyTag
import pyautogui
import pygame
import time
import threading
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
    # 等待音频播放完毕
    #while pygame.mixer.music.get_busy():
       # time.sleep(0.1)
def get_absolute_path(relative_path):
    """
    获取文件的绝对路径。

    参数:
    relative_path (str): 文件的相对路径。

    返回:
    str: 文件的绝对路径。
    """
    absolute_path = os.path.abspath(relative_path)
    return absolute_path
def get_audio_duration(file_path):
    """
    获取音频文件的时长（以秒为单位）。

    参数:
    file_path (str): 音频文件的路径。

    返回:
    float: 音频文件的时长（秒）。
    """
    try:
        tag = TinyTag.get(file_path)
        if tag is not None and tag.duration is not None:
            return tag.duration
        else:
            return "无法获取音频文件时长"
    except Exception as e:
        return f"无法获取音频文件时长: {e}"
def list_absolute_paths_in_directory(directory_path):
    """
    获取指定目录下所有文件的绝对路径。

    参数:
    directory_path (str): 目录的路径。

    返回:
    list: 目录下所有文件的绝对路径列表。
    """
    files = [os.path.abspath(os.path.join(directory_path, f)) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return files

def get_file_name(file_path):
    """
    获取文件路径中的文件名称。

    参数:
    file_path (str): 文件的路径。

    返回:
    str: 文件的名称。
    """
    file_name = os.path.basename(file_path)
    return file_name
'''
# 示例用法
relative_path = "D:\\桌面\\python作业\\GPT-SoVTIS脚本\\1.wav"
absolute_path = get_absolute_path(relative_path)
print(f"绝对路径: {absolute_path}")
url = "http://127.0.0.1:9880/tts"
params = {
    "text": "我是爱莉希雅，一位如飞花般绚丽的少女",
    "text_lang": "zh",
    "ref_audio_path": f"D:\\桌面\\python作业\\GPT-SoVTIS脚本\\1.wav",
    "prompt_lang": "zh",
    "prompt_text": "啊亲爱的山阙，请将我的剑我的花与我的爱带给那孑然独行的旅人。",
    "text_split_method": "cut5",
    "batch_size": 1,
    "media_type": "wav",
    "streaming_mode": True
}

response = requests.get(url, params=params)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("音频文件已保存为 output.wav")
else:
    print(f"请求失败，状态码: {response.status_code}, 响应: {response.text}")
'''
def click_and_hold_for_duration(x, y, duration):
    # 移动鼠标到指定位置
    pyautogui.moveTo(x, y)
    
    # 按住鼠标左键
    pyautogui.mouseDown()
    
    # 等待指定的时间
    time.sleep(duration)
    
    # 释放鼠标左键
    pyautogui.mouseUp()
    
    print(f"鼠标在 ({x}, {y}) 位置按住 {duration} 秒后已释放。")
def main(txt,item):#传入需要生成的文本以及情绪
    try:
        path=get_absolute_path(f"参考音频\\{item}")#
        lis=list_absolute_paths_in_directory(path)
        selected_audio = random.choice(lis)  # 随机选择一个音频文件
        url="http://127.0.0.1:9880/tts"
        params={
            "text": txt,
            "text_lang": "zh",
            "ref_audio_path": selected_audio,
            "prompt_lang": "zh",
            "prompt_text": get_file_name(selected_audio)[4:-4],
            "aux_ref_audio_paths": lis,  #将所有该情绪的语音文件作为参考
        }
        response = requests.get(url, params=params)
    except:
        print('无情绪分类，采用默认语气推理')
        path=get_absolute_path(f"参考音频")
        lis=list_absolute_paths_in_directory(path)
        url="http://127.0.0.1:9880/tts"
        params={
            "text": txt,
            "text_lang": "zh",
            "ref_audio_path": lis[0],
            "prompt_lang": "zh",
            "prompt_text": get_file_name(lis[0])[:-4],
        }
        response = requests.get(url, params=params)
    if response.status_code == 200:
        # 保存音频文件
        with open("output.wav", "wb") as f:
            f.write(response.content)
        print("音频文件已保存为 output1.wav")
        thread = threading.Thread(target=click_and_hold_for_duration, args=(443, 955, int(get_audio_duration('output.wav')) + 1))
        thread.start()
        time.sleep(0.3)
        play_audio('output.wav')
        time.sleep(int(get_audio_duration('output.wav')) + 1)
    else:
        print(f"请求失败，状态码: {response.status_code}, 响应: {response.text}")
    
if __name__ == "__main__":
    main('哎呀，你居然是这么想的吗？好狡猾哦。','撒娇')
