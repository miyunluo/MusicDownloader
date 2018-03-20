### 网易云音乐歌单flac文件下载

基于

（python）https://github.com/YongHaoWu/NeteaseCloudMusicFlac

​（go）https://github.com/lifei6671/NeteaseCloudMusicFlac



**加入artistName解决查询结果不精确的问题**



---



API

**Netease Music**

```python
url = 'https://api.imjad.cn/cloudmusic'
payload = {'type': 'detail', 'id':id}
```

通过id获得歌名与歌手名

**Baidu Music**

```python
url = 'http://sug.music.baidu.com/info/suggestion'
mess = song_name + ' ' + singer
payload = {'word': mess, 'version': '2.1.1', 'from': '0'}
```

获得歌曲id

```python
url = "http://music.baidu.com/data/music/fmlink"
payload = {'songIds': songid, 'type': 'flac'}
```

获得flac文件链接