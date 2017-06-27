/*
    Author        : tuxpy
    Email         : q8886888@qq.com.com
    Create time   : 2017-01-09 16:34:35
    Filename      : tianyancha.go
    Description   :
*/

package client

import (
    configs "configs/tianyancha"
    "crypto/md5"
    "datatype"
    "encoding/json"
    "fmt"
    "geetest"
    "log"
    "net/url"
    "os"
    "path"
    "path/filepath"
    "regexp"
    "requests"
    "strconv"
    "strings"
    "time"
    "utils"
)

type TianYanChaParser struct {
    robot        *Robot
    index_page   *requests.Response
    api_page     *requests.Response
    api_response *datatype.TianYanChaApiResponse
    company_id   string
    company_name string
}

type TianYanChaTongJiData struct {
    JSCode      string
    Token       string
    FxckNumbers []int
}

func (parser *TianYanChaParser) parse_tongji_response(response *requests.Response) TianYanChaTongJiData {
    tongji_json := map[string]interface{}{}
    json.Unmarshal(response.Bytes, &tongji_json)
    v := strings.Split(tongji_json["data"].(map[string]interface{})["v"].(string), ",")
    js_code := ""
    for _, code := range v {
        code_number, _ := strconv.Atoi(code)
        js_code += string(code_number)
    }
    token_re := regexp.MustCompile("token=(\\w+);")
    token := token_re.FindAllStringSubmatch(js_code, -1)[0][1]

    fxck_re := regexp.MustCompile("'([\\d,]+)'")
    fxck_chars := strings.Split(fxck_re.FindAllStringSubmatch(js_code, -1)[0][1], ",")
    fxck_numbers := make([]int, len(fxck_chars))
    for index, char := range fxck_chars {
        number, _ := strconv.Atoi(char)
        fxck_numbers[index] = number
    }

    return TianYanChaTongJiData{
        JSCode:      js_code,
        Token:       token,
        FxckNumbers: fxck_numbers,
    }

}

func (parser *TianYanChaParser) get_id_by_url(url string) string {
    r := regexp.MustCompile("http.+/(\\d+)")
    return r.FindAllStringSubmatch(url, -1)[0][1]
}

func (parser *TianYanChaParser) SolveCheck(response *requests.Response) (*requests.Response, error) {
    for i := 0; i < 5; i++ {
        if !response.Selector.Has(configs.ROBOT_CHECK) {
            return response, nil

        }
        log.Println("发现机器人检测，准备解决")
        geetest.Solve(response.Request.URL.String())
        log.Println("已解决，等重试")
        if len(response.History) == 0 {
            return nil, nil
        }
        _response, err := requests.Request(requests.Options{
            URL:    response.History[0].URL.String(),
            Method: "GET",
        })
        if err == nil {
            response = _response

        } else {
            continue
        }
    }

    return response, fmt.Errorf("Has Robot Check")
}

type GOFlipPageOptions struct {
    url_format       string
    begin            int
    size             int
    total            int
    headers          map[string]string
    parse_total_func func(*requests.Response) int // 如果不传total,并且begin为1, 则根据第一个请求来获取出total
}

// 翻译
func (parser *TianYanChaParser) GOFlipPage(options GOFlipPageOptions) ([]*requests.Response, error) {
    urls := []string{}
    url_responses_map := map[string]*requests.Response{}

    // 如果没有total, 并且begin是1, 则根据第一个请求获取出total
    if options.total == 0 && options.begin == 1 && options.parse_total_func != nil {
        first_url := fmt.Sprintf(options.url_format, 1, options.size)
        first_response, err := parser.robot.Request(requests.Options{
            URL:     first_url,
            Method:  "GET",
            Headers: options.headers,
        })
        if err != nil {
            return nil, err
        }
        urls = append(urls, first_url)
        url_responses_map[first_url] = first_response
        options.begin = 2
        options.total = options.parse_total_func(first_response)
    }

    if options.total == 0 {
        return []*requests.Response{}, nil
    }

    max_page := options.total / options.size
    if options.total%options.size != 0 {
        max_page++
    }
    flip_count := max_page - options.begin + 1
    response_count := flip_count + len(urls)

    out := make(chan *requests.GOResponse)
    options_chan := make(chan requests.Options)
    defer func() {
        close(options_chan)
        close(out)
    }()

    concurrent := 4
    requests.GORequest(concurrent, options_chan, out)

    go func() {
        for page := options.begin; page <= max_page; page++ {
            URL := fmt.Sprintf(options.url_format, page, options.size)
            urls = append(urls, URL)
            request_options := requests.Options{
                URL:     URL,
                Method:  "GET",
                Headers: options.headers,
                Debug:   false,
            }
            parser.robot.WrapRequestOptions(&request_options)
            options_chan <- request_options
        }
    }()

    responses := make([]*requests.Response, response_count)
    for index := 0; index < flip_count; index++ {
        go_response := <-out
        if go_response.Error != nil {
            return nil, go_response.Error
        } else {
            url_responses_map[go_response.Options.URL] = go_response.Response
        }
    }

    for index, _url := range urls {
        responses[index] = url_responses_map[_url]
    }

    return responses, nil
}

func (parser *TianYanChaParser) RequestApi() (*requests.Response, error) {

    index_url := parser.index_page.Request.URL.String()
    eid := parser.get_id_by_url(index_url)
    iframe_url := fmt.Sprintf("http://dis.tianyancha.com/dis/old#/show?ids=%s&cnz=true", eid)
    iframe_page, err := parser.robot.Request(requests.Options{
        URL:    iframe_url,
        Method: "GET",
    })
    utils.CheckErrorPanic(err)

    // 取出带有_sgAttr的js链接
    js_re := regexp.MustCompile("http.+?c\\.tianyancha\\.com/vr/resources/js/\\w+.js")
    js_url := js_re.FindString(string(iframe_page.Bytes))
    js_page, err := parser.robot.Request(requests.Options{
        URL: js_url,
    })
    if err != nil {
        return nil, err
    }

    // 从js中取出_sgAttr
    sgattr_re := regexp.MustCompile("n\\._sgArr=(.+?);")
    sgattrs_string := sgattr_re.FindAllStringSubmatch(string(js_page.Bytes), -1)[0][1]
    sgattrs_string = `[["6","b","t","f","2","z","l","5","w","h","q","i","s","e","c","p","m","u","9","8","y","k","j","r","x","n","-","0","3","4","d","1","a","o","7","v","g"],["1","8","o","s","z","u","n","v","m","b","9","f","d","7","h","c","p","y","2","0","3","j","-","i","l","k","t","q","4","6","r","a","w","5","e","x","g"],["s","6","h","0","p","g","3","n","m","y","l","d","x","e","a","k","z","u","f","4","r","b","-","7","o","c","i","8","v","2","1","9","q","w","t","j","5"],["x","7","0","d","i","g","a","c","t","h","u","p","f","6","v","e","q","4","b","5","k","w","9","s","-","j","l","y","3","o","n","z","m","2","1","r","8"],["z","j","3","l","1","u","s","4","5","g","c","h","7","o","t","2","k","a","-","e","x","y","b","n","8","i","6","q","p","0","d","r","v","m","w","f","9"],["j","h","p","x","3","d","6","5","8","k","t","l","z","b","4","n","r","v","y","m","g","a","0","1","c","9","-","2","7","q","e","w","u","s","f","o","i"],["8","q","-","u","d","k","7","t","z","4","x","f","v","w","p","2","e","9","o","m","5","g","1","j","i","n","6","3","r","l","b","h","y","c","a","s","0"],["d","4","9","m","o","i","5","k","q","n","c","s","6","b","j","y","x","l","a","v","3","t","u","h","-","r","z","2","0","7","g","p","8","f","1","w","e"],["7","-","g","x","6","5","n","u","q","z","w","t","m","0","h","o","y","p","i","f","k","s","9","l","r","1","2","v","4","e","8","c","b","a","d","j","3"],["1","t","8","z","o","f","l","5","2","y","q","9","p","g","r","x","e","s","d","4","n","b","u","a","m","c","h","j","3","v","i","0","-","w","7","k","6"]]`
    sgattrs := [][]string{}
    json.Unmarshal([]byte(sgattrs_string), &sgattrs)

    api_headers := map[string]string{
        "Tyc-From":   "normal",
        "Accept":     "application/json, text/plain, */*",
        "CheckError": "check",
        "Referer":    index_url,
    }
    // 从tongji中取出token, tongji接口中的v进行ascii => string, 取出token
    tongji_url := fmt.Sprintf("http://www.tianyancha.com/tongji/%s.json?random=%d", eid, time.Now().Unix()*1000)
    tongji_page, err := parser.robot.Request(requests.Options{
        URL:     tongji_url,
        Headers: api_headers,
    })
    if err != nil {
        return nil, err
    }
    tongji_data := parser.parse_tongji_response(tongji_page)

    // 算出utm
    xs := fmt.Sprintf("%d", eid[0])
    x, _ := strconv.Atoi(xs)
    if len(xs) > 1 {
        x, _ = strconv.Atoi(string(xs[1]))
    }
    sogou := sgattrs[x] // window.$SoGou$ = window._sgArr[x] x为eid的首位数字的ascii码，如果大于10, 则采用最二位，否则采用第一位
    fmt.Println("sogou", sogou, "x", x)
    utm := ""
    for _, number := range tongji_data.FxckNumbers {
        utm += sogou[number]
    }

    u, _ := url.Parse("http://www.tianyancha.com")
    parser.robot.SetCookie(u, "token", tongji_data.Token, nil)
    parser.robot.SetCookie(u, "_utm", utm, nil)
    // fmt.Println("token", token, "_utm", utm)

    response, err := parser.robot.Request(requests.Options{
        URL:     fmt.Sprintf("http://www.tianyancha.com/company/%s.json", eid),
        Headers: api_headers,
        Method:  "GET",
        Debug:   false,
    })

    return response, err

}

func (parser *TianYanChaParser) Init() {
    parser.index_page, parser.api_page, parser.api_response = nil, nil, nil
}

// 填充基本信息
func (parser *TianYanChaParser) PadBaseInfo(einfo *EInfo, error_chan chan<- error) {
    einfo.Base = parser.api_response.Data.BaseInfo

    PostDBCacheAPI("/baseinfo", parser.GetUUID(), einfo.Base, 50)
    error_chan <- nil
}

// 填充高管信息
func (parser *TianYanChaParser) PadStaffList(einfo *EInfo, error_chan chan<- error) {
    statff_list := parser.api_response.Data.StaffList
    einfo.StaffList = statff_list

    PostDBCacheAPI("/seniorminfo", parser.GetUUID(), einfo.StaffList, 50)
    error_chan <- nil
}

// 填充投资方信息
func (parser *TianYanChaParser) PadInvestorList(einfo *EInfo, error_chan chan<- error) {
    investore_list := parser.api_response.Data.InvestorList
    einfo.InvestorList = investore_list

    PostDBCacheAPI("/sharehinfo", parser.GetUUID(), einfo.InvestorList, 50)

    error_chan <- nil
}

// 填充对外投资信息
func (parser *TianYanChaParser) PadInvestList(einfo *EInfo, error_chan chan<- error) {
    invest_list := parser.api_response.Data.InvestList
    einfo.InvestList = invest_list

    PostDBCacheAPI("/foreigni", parser.GetUUID(), einfo.InvestList, 50)

    error_chan <- nil
}

// 填充法律诉讼
func (parser *TianYanChaParser) PadLawSuitList(einfo *EInfo, error_chan chan<- error) {
    first_page_list := parser.api_response.Data.LawSuitList
    einfo.LawSuitList = first_page_list
    responses, err := parser.GOFlipPage(GOFlipPageOptions{
        url_format: fmt.Sprintf("http://www.tianyancha.com/getlawsuit/%s.json?page=%%d&ps=%%d", parser.GetName()),
        begin:      2,
        size:       20,
        total:      parser.api_response.Data.LawSuitTotal,
        headers: map[string]string{
            "Referer":         parser.index_page.Request.URL.String(),
            "Tyc-From":        "normal",
            "Accept":          "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        },
    })
    if err != nil {
        error_chan <- err
        return
    }
    for _, response := range responses {
        api_response := datatype.TianYanChaLawSuitListResponse{}
        utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &api_response))
        einfo.LawSuitList = append(einfo.LawSuitList, api_response.Data.Items...)
    }

    // 将法律诉讼的内容也爬下来
    in := make(chan *requests.GOResponse)
    options_chan := make(chan requests.Options)
    requests.GORequest(5, options_chan, in)
    defer func() {
        close(options_chan)
        close(in)
    }()

    go func() {
        for _, lawsuit := range einfo.LawSuitList {
            page_url := fmt.Sprintf("http://www.tianyancha.com/lawsuit/%s", lawsuit["uuid"])
            request_options := requests.Options{
                URL:      fmt.Sprintf("http://www.tianyancha.com/lawsuit/detail/%s.json", lawsuit["uuid"]),
                Method:   "GET",
                DataType: "json",
                Headers: map[string]string{
                    "Referer": page_url,
                },
            }
            parser.robot.WrapRequestOptions(&request_options)
            options_chan <- request_options
        }
    }()

    urls_responses_map := map[string]*requests.Response{}
    for i := 0; i < len(einfo.LawSuitList); i++ {
        go_response := <-in
        if go_response.Error != nil {
            error_chan <- nil
            return
        }
        urls_responses_map[go_response.Options.URL] = go_response.Response
    }
    for _, lawsuit := range einfo.LawSuitList {
        URL := fmt.Sprintf("http://www.tianyancha.com/lawsuit/detail/%s.json", lawsuit["uuid"])
        response := urls_responses_map[URL]
        lawsuit_detail_response := datatype.TianYanChaLawSuitDetailData{}
        utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &lawsuit_detail_response))
        lawsuit["detail"] = lawsuit_detail_response.Data
    }
    PostDBCacheAPI("/legalp", parser.GetUUID(), einfo.LawSuitList, 5)
    error_chan <- nil
}

// 填充变更信息
func (parser *TianYanChaParser) PadChangeInfoList(einfo *EInfo, error_chan chan<- error) {
    change_list := parser.api_response.Data.ComChanInfoList
    einfo.ChangeList = change_list
    PostDBCacheAPI("/changesinfo", parser.GetUUID(), einfo.ChangeList, 50)
    error_chan <- nil
}

func (parser *TianYanChaParser) SolveApiRobotCheckRequest(options requests.Options) (*requests.Response, error) {
    var response *requests.Response
    var err error
    for i := 0; i < 10; i++ {
        response, err = parser.robot.Request(options)
        if err != nil {
            break
        }
        if response.StatusCode == 501 {
            robot_check_response, err := parser.robot.Request(requests.Options{
                URL: "http://antirobot.tianyancha.com/captcha/verify?return_url=" + response.Request.URL.String() + "&rnd=" + response.Header.Get("Rnd"),
            })
            _, err = parser.SolveCheck(robot_check_response)
            if err != nil {
                break
            }
        } else {
            break
        }
    }

    return response, err
}

// 年报
func (parser *TianYanChaParser) PadYearReportList(einfo *EInfo, error_chan chan<- error) {
    year_report_list := parser.api_response.Data.YearReportList
    for _, year_report := range year_report_list {
        page_url := fmt.Sprintf("http://www.tianyancha.com/reportContent/%s/%s", parser.GetID(), year_report["reportYear"])

        response, err := parser.SolveApiRobotCheckRequest(requests.Options{
            Method: "GET",
            URL:    fmt.Sprintf("http://www.tianyancha.com/annualreport/newReport.json?id=%s&year=%s", parser.GetID(), year_report["reportYear"]),
            Headers: map[string]string{
                "Accept":          "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
                "Referer":         page_url,
            },
        })
        if err != nil {
            error_chan <- err
            return
        }
        year_report_response := datatype.TianYanChaYearReportResponse{}
        //    if json.Unmarshal(response.Bytes, &year_report_response) != nil {
        //        fmt.Println("Error Json Content", string(response.Bytes), response.StatusCode, response.Header)
        //    }
        utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &year_report_response))
        year_report["content"] = year_report_response.Data
    }
    einfo.YearReportList = year_report_list
    PostDBCacheAPI("/annualr", parser.GetUUID(), einfo.YearReportList, 50)
    error_chan <- nil
}

// 填充招标
func (parser *TianYanChaParser) PadCompanyBidList(einfo *EInfo, error_chan chan<- error) {
    company_bid_list := []map[string]interface{}{}
    responses, err := parser.GOFlipPage(GOFlipPageOptions{
        url_format: fmt.Sprintf("http://www.tianyancha.com/extend/getCompanyBid.json?companyName=%s&pn=%%d&ps=%%d", parser.GetName()),
        size:       20,
        begin:      1,
        parse_total_func: func(response *requests.Response) int {
            company_bid_response := datatype.TianYanChaCompanyBidResponse{}
            utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &company_bid_response))
            return company_bid_response.Data.Total
        },
    })
    if err != nil {
        error_chan <- err
        return
    }
    for _, response := range responses {
        company_bid_response := datatype.TianYanChaCompanyBidResponse{}
        utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &company_bid_response))
        company_bid_list = append(company_bid_list, company_bid_response.Data.List...)
    }

    einfo.CompanyBidList = company_bid_list
    error_chan <- nil

}

// 填充法院公告
func (parser *TianYanChaParser) PadCourtAnnouncements(einfo *EInfo, error_chan chan<- error) {
    response, err := parser.robot.Request(requests.Options{
        URL:      fmt.Sprintf("http://www.tianyancha.com/court/%s.json", parser.GetName()),
        Method:   "GET",
        DataType: "json",
    })
    if err != nil {
        error_chan <- err
        return
    }
    court_announcements_response := datatype.TianYanChaCourtAnnouncementsResponse{}
    utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &court_announcements_response))

    court_announcements := court_announcements_response.CourtAnnouncements // 法院公告这个接口肯定是临时工写的，数据没有包括在data里面
    einfo.CourtAnnouncements = court_announcements

    PostDBCacheAPI("/courtn", parser.GetUUID(), einfo.CourtAnnouncements, 50)
    error_chan <- err
}

func (parser *TianYanChaParser) _SaveTM2Local(id string, response *requests.Response) {
    localpath := utils.RelativeExecPath(fmt.Sprintf("images/%s", parser.GetUUID()))
    os.MkdirAll(localpath, 0744)
    writer, err := os.Create(filepath.Join(localpath, id+path.Ext(response.Request.URL.String())))
    utils.CheckErrorPanic(err)
    defer writer.Close()
    writer.Write(response.Bytes)
}

// 填充商标信息
func (parser *TianYanChaParser) PadTMList(einfo *EInfo, error_chan chan<- error) {
    url_format := fmt.Sprintf("http://www.tianyancha.com/tm/getTmList.json?id=%s&pageNum=%%d&ps=%%d", parser.GetID())
    responses, err := parser.GOFlipPage(GOFlipPageOptions{
        url_format: url_format,
        size:       50,
        begin:      1,
        parse_total_func: func(response *requests.Response) int {
            tm_list_response := datatype.TianYanChaTMListResponse{}
            json.Unmarshal(response.Bytes, &tm_list_response)
            total, _ := strconv.Atoi(tm_list_response.Data.Total)
            return total
        },
    })
    if err != nil {
        error_chan <- err
        return
    }
    einfo.TMList = []map[string]interface{}{}
    for _, response := range responses {
        tm_list_response := datatype.TianYanChaTMListResponse{}
        json.Unmarshal(response.Bytes, &tm_list_response)

        down_options := make([]requests.Options, len(tm_list_response.Data.Items))
        for index, _ := range down_options {
            down_options[index] = requests.Options{
                URL:    tm_list_response.Data.Items[index]["tmPic"].(string),
                Client: parser.robot.session,
                Method: "GET",
            }
        }
        image_responses, err := requests.MapRequest(5, down_options)
        if err != nil {
            error_chan <- err
            return
        }
        for index, item := range tm_list_response.Data.Items {
            parser._SaveTM2Local(item["id"].(string), image_responses[index])
            //     image_base64_bytes := utils.B64Encode(image_responses[index].Bytes)
            //     item["file_content"] = string(image_base64_bytes)
        }
        einfo.TMList = append(einfo.TMList, tm_list_response.Data.Items...)
    }

    PostDBCacheAPI("/stademinfo", parser.GetUUID(), einfo.TMList, 50)
    error_chan <- nil

}

// 填充专利信息
func (parser *TianYanChaParser) PadPatentList(einfo *EInfo, error_chan chan<- error) {
    url_format := fmt.Sprintf("http://www.tianyancha.com/extend/getPatentList.json?companyName=%s&pn=%%d&ps=%%d", parser.GetName())
    responses, err := parser.GOFlipPage(GOFlipPageOptions{
        url_format: url_format,
        begin:      1,
        size:       50,
        parse_total_func: func(response *requests.Response) int {
            patent_list_response := datatype.TianYanChaPatentListResponse{}
            utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &patent_list_response))
            return patent_list_response.Data.Total
        },
    })
    if err != nil {
        error_chan <- err
        return
    }
    einfo.PatentList = []map[string]interface{}{}
    for _, response := range responses {
        patent_list_response := datatype.TianYanChaPatentListResponse{}
        utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &patent_list_response))
        einfo.PatentList = append(einfo.PatentList, patent_list_response.Data.PatentList...)
    }
    PostDBCacheAPI("/patentinfo", parser.GetUUID(), einfo.PatentList, 50)
    error_chan <- err
}

// 填充著作权
func (parser *TianYanChaParser) PadCopyRightList(einfo *EInfo, error_chan chan<- error) {
    url_format := fmt.Sprintf("http://www.tianyancha.com/extend/getCopyrightList.json?companyName=%s&pn=%%d&ps=%%d", parser.GetName())
    responses, err := parser.GOFlipPage(GOFlipPageOptions{
        url_format: url_format,
        size:       20,
        begin:      1,
        parse_total_func: func(response *requests.Response) int {
            copyright_list_response := datatype.TianYanChaCopyRightListResponse{}
            utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &copyright_list_response))
            return copyright_list_response.Data.Total
        },
    })
    if err != nil {
        error_chan <- err
        return
    }
    einfo.CopyRightList = []map[string]interface{}{}
    for _, response := range responses {
        copyright_list_response := datatype.TianYanChaCopyRightListResponse{}
        utils.CheckErrorPanic(json.Unmarshal(response.Bytes, &copyright_list_response))
        einfo.CopyRightList = append(einfo.CopyRightList, copyright_list_response.Data.CopyRightList...)
    }

    PostDBCacheAPI("/copyrightinfo", parser.GetUUID(), einfo.CopyRightList, 50)
    error_chan <- nil

}

// 填充备案信息
func (parser *TianYanChaParser) PadICPList(einfo *EInfo, error_chan chan<- error) {
    response, err := parser.robot.Request(requests.Options{
        URL:      fmt.Sprintf("http://www.tianyancha.com/IcpList/%s.json", parser.GetID()),
        Method:   "GET",
        DataType: "json",
    })
    if err != nil {
        error_chan <- err
        return
    }

    ipc_list_response := datatype.TianYanChaIPCListResponse{}
    json.Unmarshal(response.Bytes, &ipc_list_response)

    einfo.IPCList = ipc_list_response.Data
    PostDBCacheAPI("/websiter", parser.GetUUID(), einfo.IPCList, 50)
    error_chan <- nil
}

func (parser *TianYanChaParser) GetName() string {
    if parser.company_name == "" {
        parser.company_name = parser.api_response.Data.BaseInfo["name"].(string)
    }
    return parser.company_name
}

func (parser *TianYanChaParser) GetID() string {
    if parser.company_id == "" {
        parser.company_id = fmt.Sprint(int(parser.api_response.Data.BaseInfo["id"].(int64)))
    }
    return parser.company_id
}

func (parser *TianYanChaParser) GetUUID() string {
    hash := md5.New()
    hash.Write([]byte(parser.GetID()))
    return fmt.Sprintf("%x", hash.Sum(nil))
}

func (parser *TianYanChaParser) InstallOne(URL string) (*EInfo, error) {
    index_page, err := parser.robot.Request(requests.Options{
        URL:    URL,
        Method: "GET",
    })
    if err != nil {
        return nil, err
    }
    parser.index_page = index_page

    _, err = parser.SolveCheck(parser.index_page)
    if err != nil {
        return nil, err
    }

    api_page, err := parser.RequestApi()
    if err != nil {
        return nil, err
    }

    parser.api_page = api_page
    parser.api_response = &datatype.TianYanChaApiResponse{}
    utils.CheckErrorPanic(json.Unmarshal(api_page.Bytes, parser.api_response))
    FtoI(parser.api_response.Data.BaseInfo)
    fmt.Println("Start parse", parser.GetID(), parser.GetName())

    // 请求完首页和api页面后，开始进行信息的组装
    einfo := &EInfo{}
    error_chans := []chan error{}

    generate_sccess_chan := func() chan error {
        _chan := make(chan error)
        error_chans = append(error_chans, _chan)

        return _chan
    }

    go parser.PadBaseInfo(einfo, generate_sccess_chan())
    go parser.PadStaffList(einfo, generate_sccess_chan())
    go parser.PadInvestorList(einfo, generate_sccess_chan())
    go parser.PadInvestList(einfo, generate_sccess_chan())
    go parser.PadLawSuitList(einfo, generate_sccess_chan())
    go parser.PadChangeInfoList(einfo, generate_sccess_chan())
    go parser.PadYearReportList(einfo, generate_sccess_chan())
    go parser.PadCourtAnnouncements(einfo, generate_sccess_chan())
    go parser.PadTMList(einfo, generate_sccess_chan())
    go parser.PadPatentList(einfo, generate_sccess_chan())
    go parser.PadCopyRightList(einfo, generate_sccess_chan())
    go parser.PadICPList(einfo, generate_sccess_chan())
    // go parser.PadCompanyBidList(einfo, generate_sccess_chan())

    for i := 0; i < len(error_chans); i++ {
        <-error_chans[i]
        close(error_chans[i])

    }
    return einfo, nil
}