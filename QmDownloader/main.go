package main 

import(
	"fmt"
	"os"
	"io"
	"regexp"
	"strings"
	"net/http"
	"net/url"
	"io/ioutil"
	"compress/gzip"
)

func DownloadString(remoteUrl string, queryValues url.Values) (body []byte, err error) {
	client := &http.Client{}
	body = nil
	uri, err := url.Parse(remoteUrl)

	//fmt.Println("uri: ", uri)

	if(err != nil){
		return
	}
	if(queryValues != nil){
		values := uri.Query()
		if(values != nil){
			for k,v := range values {
				queryValues[k] = v
			}
		}
		uri.RawQuery = queryValues.Encode()
	}
	request, err := http.NewRequest("GET", uri.String(), nil)
	request.Header.Add("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	request.Header.Add("Accept-Encoding", "gzip, deflate");
	request.Header.Add("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3");
	request.Header.Add("Connection", "keep-alive");
	request.Header.Add("Host", uri.Host);
	request.Header.Add("Referer", uri.String());
	request.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0");

	response, err := client.Do(request)
	defer response.Body.Close();
	if(err != nil){
		return ;
	}

	if response.StatusCode == 200 {
		switch response.Header.Get("Content-Encoding") {
		case "gzip":
			reader, _ := gzip.NewReader(response.Body)
			for {
				buf := make([]byte, 1024)
				n, err := reader.Read(buf)

				if err != nil && err != io.EOF {
					panic(err)
				}

				if n == 0 {
					break
				}
				body = append(body,buf...);
			}
		default:
			body, _ = ioutil.ReadAll(response.Body)

		}
	}

	return
}

func WriteStringToFile(filepath, s string) error {
	fo, err := os.Create(filepath)
	if (err != nil) {
		return err
	}
	defer fo.Close()

	_,err = io.Copy(fo, strings.NewReader(s))
	if err != nil {
		return err
	}

	return nil
}

func qm_song(url string) {
	response, err := DownloadString(url, nil)
	if(err != nil){
		fmt.Println("访问url出错: ", err)
		return
	}

	/*WriteStringToFile("info.txt", string(response))*/

	// get singer name
	reg := regexp.MustCompile(
	`<a 
      .*?
      .*?
      class="singer_user__name"
    >
      (.*?)
    </a>`)
	singer_user__name := reg.FindAllString(string(response), -1)
	contents := singer_user__name[0]
	bytecon := reg.FindAllSubmatch([]byte(contents), -1)
	singer := string(bytecon[0][1])

	// get music name
	reg = regexp.MustCompile(`<h2 class="play_name">(.*?)</h2>`)
	play_name := reg.FindAllString(string(response), -1)
	contents = play_name[0]
	bytecon = reg.FindAllSubmatch([]byte(contents), -1)
	music_name := string(bytecon[0][1])

	// get song link
	reg = regexp.MustCompile(`<script type='text/javascript' >.*?"playurl".*?</script>`)
	script := reg.FindAllString(string(response), -1)
	contents = script[0]
	reg = regexp.MustCompile(`"playurl":(.*?),"playurl_video"`)
	bytecon = reg.FindAllSubmatch([]byte(contents), -1)
	songlink := string(bytecon[0][0])
	songlink = strings.Trim(songlink, "\"playurl\":\"")
	songlink = strings.Trim(songlink, "\",\"playurl_video")

	// download file
	filename := music_name+"-"+singer+".mp3"
	fmt.Println("正在下载 ", music_name,"-",singer," ......");
	songRes ,err:= http.Get(songlink);
	if(err != nil){
		fmt.Println("下载文件时出错：",songlink);
		return ;
	}
	songFile, err := os.Create(filename);
	written, err := io.Copy(songFile, songRes.Body);
	if(err != nil){
		fmt.Println("保存音乐文件时出错：",err);
		return ;
	}
	fmt.Println(music_name,"下载完成,文件大小：",fmt.Sprintf("%.2f", (float64(written)/(1024*1024))),"MB");
}

func main() {
	if(len(os.Args) <= 1) {
		fmt.Println("输入全民k歌链接.")
		return
	}
	url := os.Args[1]
	qm_song(url)

}
