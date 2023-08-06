import requests
import json
## 调用api 登录获取cookie
## @getid 最终返回微哨返回的登录cookie
## @getme 返回本次要打卡的信息
def getid(stu_code,password):
    try:
        s = requests.Session()
        loginurl="https://api.zit.edu.cn/login"
        url_s = "https://api.zit.edu.cn/oauth/authorize"
        
        get_cookies=s.get(url=loginurl)
        cookie=get_cookies.headers.get('Set-Cookie')
        
        verifyKey="{}_zit".format(stu_code)
        ## print(cookie)
        
        headers2={
                "Content-Type":"application/x-www-form-urlencoded",
                "Cookie":cookie
                }
        
        data = {
                "schoolcode": "zit",
                "username": stu_code,
                "password": password,
                "verifyValue":"", 
                "verifyKey": verifyKey,
                "ssokey":"",
                }
        params={
                "client_id":"pqZ3wGM07i8R9mR3",
                "redirect_uri":"https://lightapp.zit.edu.cn/check/questionnaire",
                "response_type":"code",
                "scope":"base_api",
                "state":"ruijie"
                }
        res=s.post(url=loginurl,headers=headers2,data=data,allow_redirects=False)
        res = s.get(url=url_s,headers=headers2,params=params,allow_redirects=False)
        spaserver_url=res.text[22:]
        cook = s.get(url=str(spaserver_url), headers=headers2, allow_redirects=False).headers['set-cookie']
        return cook

    except:
        return "Unknown"
    
def getme(stu_code,cook):
    s = requests.Session()
    schoolcode="zit"
    head = {
        'Content-Type': 'application/json',
        'Cookie': cook,
    }
    authorityid=f'["10025","10081","10214","10263"]'

    url1 = f'https://lightapp.zit.edu.cn/api/questionnaire/questionnaire/getQuestionNaireList?sch_code=zit&stu_code={stu_code}&authorityid={authorityid}&type=1&pagenum=1&pagesize=20&stu_range=999&searchkey='
    head = { 
        'Cookie': cook,
    }   
    try:
        # 获取 昨天/最新 的打卡信息
        data = s.get(url1,headers=head).text
        info = s.get(url1,headers=head).json().get("data")[0]
        activityid=info.get('activityid')
        authorityid=info.get('authorityid') 
        
        url2 = f'https://lightapp.zit.edu.cn/api/questionnaire/questionnaire/getQuestionDetail?sch_code={schoolcode}&stu_code={stu_code}&activityid={activityid}&can_repeat=1&page_from=onpublic&private_id=0'
        # info里面存放着最新的的打卡记录
        info = requests.get(url2, headers=head).json().get("data")
        questions = info.get("question_list")
        #print(data)
        private_id=info.get("last_private_id")
        flag=0
        answers=[]
        while flag < len(questions):
            answer = {
                "questionid": questions[flag].get("questionid"),
                "optionid": questions[flag].get("user_answer_optionid"),
                "optiontitle": 0,
                "question_sort": 0,
                'question_type': questions[flag].get("question_type"),
                "option_sort": 0,
                'range_value': "",
                "content": questions[flag].get("user_answer_content"),
                "isotheroption": questions[flag].get("otheroption"),
                "otheroption_content": questions[flag].get("user_answer_otheroption_content"),
                "isanswered": questions[flag].get("user_answer_this_question"),
                "answerid": questions[flag].get("answerid"),
            }
            jump = 0
            type = answer["question_type"]
            #print(answer.get("optionid"))
            if type == 1:
                for i in questions[flag].get("option_list"):
                    if answer["optionid"].isdigit() and i.get("optionid") == int(answer["optionid"]):
                        answer["optiontitle"] = i.get("title")
                        if questions[flag].get("hsjump"):
                            jump = i.get("jumpid") - 1

            elif type in [3, 4, 7, 8, 9]:
                answer["optionid"] = 0
            answer["answered"] = answer["isanswered"]
            answers.append(answer)
            if jump:
                flag = jump
            else:
                flag += 1

        flag = 0
        totalArr = []
        while flag < len(questions):
            answer = {
                "questionid": questions[flag].get("questionid"),
                "optionid": questions[flag].get("user_answer_optionid"),
                "optiontitle": 0,
                "question_sort": 0,
                'question_type': questions[flag].get("question_type"),
                "option_sort": 0,
                'range_value': "",
                "content": questions[flag].get("user_answer_content"),
                "isotheroption": questions[flag].get("otheroption"),
                "otheroption_content": questions[flag].get("user_answer_otheroption_content"),
                "isanswered": questions[flag].get("user_answer_this_question")
            }
            type = answer['question_type']

            if type == 1 and answer["optionid"] != "":
                for i in questions[flag].get("option_list"):
                    if answer["optionid"].isdigit() and i.get("optionid") == int(answer["optionid"]):
                        answer["optiontitle"] = i.get("title")
            elif type in [3, 7]:
                answer["optionid"] = 0

            if questions[flag].get("user_answer_this_question"):
                answer["isanswered"] = True
                answer["answerid"] = questions[flag].get("answerid")
                answer["answered"] = answer["isanswered"]
            else:
                answer["hide"] = True
                answer["optionid"] = 0
                answer["isanswered"] = ''
                answer["answered"] = False

            totalArr.append(answer)
            flag += 1

        head['Referer'] = 'lightapp.zit.edu.cn/'
        userinfo = requests.get("https://lightapp.zit.edu.cn/userInfo", headers=head).json().get("data")
        data = {
            "sch_code": userinfo.get("schcode"),
            "stu_code": userinfo.get("stucode"),
            "stu_name": userinfo.get("username"),
            "identity": userinfo.get("identity"),
            "path": userinfo.get("path"),
            "organization": userinfo.get("organization"),
            "gender": userinfo.get("gender"),
            "activityid": activityid,
            "anonymous": 0,
            "canrepeat": 1,
            "repeat_range": 1,
            "question_data": answers,
            "totalArr": totalArr,
            "private_id": private_id
        }
        #print(data)
        return data
    except:
        return "Unknown"

## 参数说明：
##    @ name  -> str: 方便打印输入的昵称
##    @ username ->str : 学号
##    @ password -> str: 密码
##    @ sign -> int: 打卡人数
##    @ unsigned -> int : 未打卡人数
##    @ unpron -> arr[NULL]: 用于存放失败学号的数组
def runandpretty(name,username,password,sign,unsign,unpron):
    cook = getid(username,password)
    mydata = getme(username,cook)
    res = post(mydata,cook)
    if res[0:3]=="[S]":   
        sign+=1
    if res[0:3]=="[E]":
        unsign+=1
        unpron.append(username)
    text = []
    text.append(name)
    text.append(username)
    text.append(res)
    return text,sign,unsign 

## 利用sql 填报的表单说明
## @ tables  -> str :用来存放数据的表  
def sql_report(tables):
    data = get_config()
    try:
        db = pymysql.connect(data[0],data[1],data[2],data[3],charset='utf8')
        print("[S]: Successfully connected to database.")
        cur = db.cursor()
        sql ='SELECT * FROM {}'.format(tables)
        cur.execute(sql)
        results = cur.fetchall()
        count = 0
        print("[S]: Successfully get myclass.")
        table = PrettyTable(["Name","Userid","Status"])
        unsign=0  
        sign=0
        unpron=[]
        for row in results:
            name,qq,username,password =row
            text,sign,unsign = runandpretty(name,username,password,sign,unsign,unpron)
            table.add_row(text)
            count+=1
            print("\r",end="")
            print("Run progress : ({}/{})".format(count,len(results)),end="")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")      
        print(table)
    except pymysql.Error as e:
        print("[E]:"+str(e))
    db.close() ## shutdown database
    return sign,unsign,count


