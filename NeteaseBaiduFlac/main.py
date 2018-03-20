# -*- coding: utf-8 -*-

import re
import os
import sys
import json
import urllib2
import requests

def download(url):
	h = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}
	r = requests.get(url, headers= h)
	contents = r.text
	return contents

def get_Netease_song_ids(url):
	contents = download(url)
	res = r'<ul class="f-hide">(.*?)</ul>'
	song_list = re.findall(res, contents, re.S | re.M)
	#print song_list
	if(song_list):
		contents = song_list[0]
	else:
		print 'Can not fetch information from URL.'

	res = r'<li><a href=\"\/song\?id=(.*?)\">.*?</a></li>'
	song_ids = re.findall(res, contents, re.S | re.M)
	#print song_ids
	return song_ids

def get_Netease_song_name_and_singer(id):
	url = 'https://api.imjad.cn/cloudmusic'
	payload = {'type': 'detail', 'id':id}
	r = requests.get(url, params=payload)
	contents = r.text
	d = json.loads(contents, encoding="utf-8")
	if('songs' not in d):
		return ""
	songname = d["songs"][0]["name"]
	songsinger = d["songs"][0]["ar"][0]["name"]
	#print songname
	#print songsinger
	return songname, songsinger

def get_Baidu_music_link(song_name, singer):
	# 获得百度音乐歌曲id
	url = 'http://sug.music.baidu.com/info/suggestion'
	mess = song_name + ' ' + singer
	payload = {'word': mess, 'version': '2.1.1', 'from': '0'}
	r = requests.get(url, params=payload)
	contents = r.text
	#print contents
	d = json.loads(contents, encoding="utf-8")
	if('data' not in d):
		print "%s is not found.\n" % song_name
		return 0
	songid = d["data"]["song"][0]["songid"]
	#print "songid: " + songid

	# 百度音乐free api
	url = "http://music.baidu.com/data/music/fmlink"
	payload = {'songIds': songid, 'type': 'flac'}
	r = requests.get(url, params=payload)
	contents = r.text
	d = json.loads(contents, encoding="utf-8")
	if d is not None and 'data' not in d or d["data"] == '' or d["data"]["songList"] == '':
		return 0

	bsongname = d["data"]["songList"][0]["songName"]
	bsongsinger = d["data"]["songList"][0]["artistName"]

	#print "baidu songname", bsongname
	#print "baidu songsinger", bsongsinger
	if(song_name != bsongname or singer != bsongsinger):
		print "%s is not found.\n" % song_name
		return 0

	songlink = d["data"]["songList"][0]["songLink"]
	if(len(songlink) < 10):
		print "Do not have flac for %s.\n" % song_name
		return 0
	#print "Song Source: " + songlink
	return songlink

def download_music(url, song_name, singer):
	f = urllib2.urlopen(url)

	print "Downloading: " + song_name + "......"
	path = "songdir"
	if not os.path.isdir(path):
		os.mkdir(path)

	filename = "./" + path + "/" + song_name + "-" + singer + ".flac"
	with open(filename, "wb") as code:
		code.write(f.read())
	print "Download %s is finished.\n" % song_name


if __name__ == '__main__':
	url = 'http://music.163.com/#/playlist?id=2144830118'
	url = re.sub("#/", "", url).strip()
	neteaseids = get_Netease_song_ids(url)
	for id in neteaseids:
		name, singer = get_Netease_song_name_and_singer(id)
		link = get_Baidu_music_link(name,singer)
		if link != 0:
			download_music(link, name, singer)


