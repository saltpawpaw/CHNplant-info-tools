# author: Yujing Yan
# grab data from cvh website
# different fields are seperated by "#"

import urllib2, re
#import shutil, string, xlwt, io

#build a new excel
#exl = xlwt.Workbook()
#tablesp = exl.add_sheet('sheet1')

spinput = '/Users/wulalayan/Documents/project/test.txt' #species name list, must be seperated by "/n"
output = '/Users/wulalayan/Documents/project/' #location to store the result, will generate result file automatically

with open(spinput,'r') as f: #read the names
    splist = f.readlines()
#f = io.open('/Users/wulalayan/Documents/project/splist1.txt', "r", encoding='utf-16')
#splist = f.readlines()
nrow=1
url_main = "http://www.cvh.ac.cn/"

#convert the sp name to url->change space into %20
#spname = "Acantholimon hedinii"
for spname in splist:
    print splist.index(spname)
    spname = spname.strip()    #delete "/n"
    print spname
    spnameu = spname.replace(" ","%20")
    #open the url
    url = url_main+"search/"+spnameu+"?n=1"
    reqse = urllib2.Request(url)
    fdse = urllib2.urlopen(reqse)
    htmlse = fdse.read()
    #get the specimen id on the 1st page
    spid = re.findall(r'/spm/.+?\'', htmlse) #some include whitespace
    #spid = re.findall(r'/spm/\S+', htmlse)  #findall, return list
    spidall=spid
    synonm1 = re.findall(r'href=\'(/search/.+?)\?n=1\'>', htmlse) #find other names
    if spid: 
    #get the page num url
        pnum = re.findall(r'href=(\?page=[0-9]+?.+?)>[0-9]+?', htmlse)  #search for "?page=2&searchtype=1&n=1"
        if pnum:
            for p in pnum:
                urlp = url_main+"search/"+spnameu+p
                #print urlp
                reqsep = urllib2.Request(urlp)
                fdsep = urllib2.urlopen(reqsep)
                htmlsep = fdsep.read()
                spidp = re.findall(r'/spm/.+?\'', htmlsep)
                spid = spid+spidp
        #if there exist synonyms, open their url and get the specimenid
    if synonm1:
        for syn in synonm1:
            print "Synonm1: "+syn
            syn = syn.replace(" ","%20")
            urlsyn1 = url_main+syn+"?n=1"
            reqsyn1 = urllib2.Request(urlsyn1)
            fdsyn1 = urllib2.urlopen(reqsyn1)
            htmlsyn1 = fdsyn1.read()
            #get the specimen id on the 1st page
            synid1 = re.findall(r'/spm/.+?\'', htmlsyn1)
            synonm2 = re.findall(r'href=\'(/search/.+?)\?n=1\'>', htmlsyn1) #find other names
            if synid1:
                synpnum1 = re.findall(r'href=(\?page=[0-9]+?.+?)>[0-9]+?', htmlsyn1)  #search for "?page=2&searchtype=1&n=1"
                if synpnum1:
                    for p in synpnum1:
                        urlsynp = url_main+"search/"+syn+p
                        #print urlp
                        reqsynp = urllib2.Request(urlsynp)
                        fdsynp = urllib2.urlopen(reqsynp)
                        htmlsynp = fdsynp.read()
                        synidp = re.findall(r'/spm/.+?\'', htmlsynp)
                        synid1 = synid1+synidp
        spidall = spid+synid1
        #print ("2", spidall)
        if synonm2: #if there exist synonyms, open their url and get the specimen id
            for syn in synonm2:
                print "Synonm2: "+syn
                syn = syn.replace(" ","%20")
                urlsyn2 = url_main+syn+"?n=1"
                reqsyn2 = urllib2.Request(urlsyn2)
                fdsyn2 = urllib2.urlopen(reqsyn2)
                htmlsyn2 = fdsyn2.read()
                #get the specimen id on the 1st page
                synid2 = re.findall(r'/spm/.+?\'', htmlsyn2)
                if synid2: #get the pages
                    synpnum2 = re.findall(r'href=(\?page=[0-9]+?.+?)>[0-9]+?', htmlsyn2)  #search for "?page=2&searchtype=1&n=1"
                    if synpnum2:
                        for p in synpnum2:
                            urlsynp = url_main+"search/"+syn+p
                            #print urlp
                            reqsynp = urllib2.Request(urlsynp)
                            fdsynp = urllib2.urlopen(reqsynp)
                            htmlsynp = fdsynp.read()
                            synidp = re.findall(r'/spm/.+?\'', htmlsynp)
                            synid2 = synid2+synidp
            spidall = spid+synid1+synid2
    print "The number of specimen is "+str(len(spidall)/2)
    if spidall:
        spid_dic = dict()
        #print ("3", spidall)
        for id in spidall:
            spid_dic[id] = 1
        #open the specimen id
        for key in spid_dic:
            id = key.rstrip("'")
            id = id.replace(" ","%20")
            print id
            spurl = url_main+id
            reqsp = urllib2.Request(spurl)
            fdsp = urllib2.urlopen(reqsp)
            htmlsp = fdsp.read()
            #get the specimen info part, search 'sptitle2'
            scount = 1
            for n in re.finditer('sptitle2', htmlsp):
                flag1 = n.end()
                flag2 = n.start()
                if scount == 1:
                    spcname1 = flag1
                if scount ==2:
                    spcname2 = flag2
                if scount ==4:
                    desc1 = flag1
                if scount == 8:
                    desc2 = flag2
                scount = scount+1
            spcname = htmlsp[spcname1: spcname2]
            desc = htmlsp[desc1:desc2]
            #print spcname
            #species name
            spcn = re.findall(r'blank.+?</a',spcname)
            spcn = re.findall(r'>(.+?)<',spcn[0])
            spcn = spcn[0].decode('UTF-8')
            filesp = open(output+'result.txt', 'a')
            filesp.write('\n'+spname+'#'+id+'#'+spcn.encode('UTF-8')+'#')
            #tablesp.write(nrow, 0, spname)
            #tablesp.write(nrow, 1, id)
            #tablesp.write(nrow, 2, spcn)
            coldate = re.findall(r'o_spcoldate.+?>(.+?)</div',desc)  #collection date
            if coldate:
                coldate = coldate[0].decode('UTF-8')
                filesp.write(coldate.encode('UTF-8')+'#')
                #tablesp.write(nrow, 3, coldate)
            else:
                filesp.write('#')
            loca = re.findall(r'o_spplace.+?>(.+?)</div',desc) #location
            if loca:
                loca = loca[0].decode('UTF-8')
                filesp.write(loca.encode('UTF-8')+'#')
                #tablesp.write(nrow, 4, loca)
            else:
                filesp.write('#')
            habitat = re.findall(r'o_spenviro.+?>(.+?)</div',desc)  #habitat
            if habitat:
                habitat = habitat[0].decode('UTF-8')
                filesp.write(habitat.encode('UTF-8')+'#')
                #tablesp.write(nrow, 5, habitat)
            else:
                filesp.write('#')
            ele = re.findall(r'o_spal.+?>(.+?)</div',desc)  #elevation
            if ele:
                ele = ele[0].decode('UTF-8')
                filesp.write(ele.encode('UTF-8')+'#')
                #tablesp.write(nrow, 6, ele)
            else:
                filesp.write('#')
            filesp.close()
            #nrow = nrow+1
    else:
        filesp = open(output+'result.txt', 'a')
        filesp.write('\n'+spname)
        filesp.close()
        #tablesp.write(nrow, 0, spname)
        #nrow = nrow+1
        continue
#exl.save('/Users/wulalayan/Documents/project/test.xls') 