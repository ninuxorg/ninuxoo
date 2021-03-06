#!/usr/bin/python

import sys
import cgi
import urllib2
import BeautifulSoup
import smbc


sys.stderr = sys.stdout

SMBC_TYPE = {'share':3, 'folder':7, 'file':8}


NAS_LIST = 'Ninux_NAS'

######################################################

def getform(valuelist, theform, notpresent=''):
    """This function, given a CGI form, extracts the data from it, based on
    valuelist passed in. Any non-present values are set to '' - although this can be changed.
    (e.g. to return None so you can test for missing keywords - where '' is a valid answer but to have the field missing isn't.)"""
    data = {}
    for field in valuelist:
        if not theform.has_key(field):
            data[field] = notpresent
        else:
            if  type(theform[field]) != type([]):
                data[field] = theform[field].value
            else:
                values = map(lambda x: x.value, theform[field])     # allows for list type values
                data[field] = values
    return data


def pagefetch(thepage):
    req = urllib2.Request(thepage)
    u = urllib2.urlopen(req)
    data = u.read()
    return data

pre_html = u'''
<html>
<head>
<title>ninuXoo! - VoIP</title>
</head>
<link rel="stylesheet" href="/ninuxoo/ninuxoo.css" type="text/css" />
<body>
<div id="navmenu"> 
        <ul> 
                <li><a href="/">Cerca</a></li> 
                <li><a href="/cgi-bin/new_files.cgi">Novit&agrave;</a></li> 
                <li><a href="/cgi-bin/browse_share.cgi">Files</a></li> 
                <li><a href="/cgi-bin/proxy_wiki.cgi?url=Elenco_Telefonico_rete_VoIP_di_ninux.org">VoIP</a></li> 
		<li><a href="http://10.168.177.178:8888/">JukeBox</a></li> 
                <li><a href="http://10.162.0.85/">WebMail</a></li> 
                <li><a href="http://blog.ninux.org">Blog</a></li> 
                <li><a href="http://wiki.ninux.org">Wiki</a></li> 
        </ul> 
</div> 
<div class="logo">
<a href="/cgi-bin/ninuxoo.cgi">
<img src="/ninuxoo/ninuxoo.png" border="0" alt="ninuXoo!"/>
</a>
</div>
<br />
<br />
<div id="result">
'''

post_html = '''
</div>
</body>
</html>
'''
###################################################


def strip_tags(element, tags_to_strip) :
   for tag in element.findAll(True):
      if tag.name in tags_to_strip:
         for i, x in enumerate(tag.parent.contents):
            if x == tag: 
               break
            else:
               continue
         for r in reversed(tag.contents):
            tag.parent.insert(i, r)
         tag.extract()
   return element


if __name__ == '__main__':
    print "Content-type: text/html"         # this is the header to the server
    print                                   # so is this blank line
    outhtml = pre_html
    form = cgi.FieldStorage()           
    data = getform(['url', 'download'],form)
    if not data['url'] :
        # show the NAS list from the wiki 
        data = pagefetch('http://wiki.ninux.org/' + NAS_LIST )
        soup = BeautifulSoup.BeautifulSoup(data)
        rows = soup.findAll("tr")
        outhtml += "<ul class='files'>" 
        for r in rows:
            tds = r.findAll("td") 
            tags_to_strip = 'p', 'span', 'a'
            name = strip_tags(tds[0], tags_to_strip).contents[0]
            url = strip_tags(tds[1], tags_to_strip).contents[0]
            location = strip_tags(tds[2], tags_to_strip).contents[0]
            outhtml += u"<li class='resource'><a href='/cgi-bin/browse_share.cgi?url=" + str(url).strip() + "'>" + str(name).strip() + "</a> (" + str(location).strip() + ")</li>"
        outhtml += "</ul>"
        outhtml += post_html
    elif data['url']:
         if data['url'].find('smb://') >= 0:
             ctx = smbc.Context()
         # e allora samba
             try:
                 entries = ctx.opendir (data['url']).getdents ()
             except:
                 outhtml += u"Error opening " + data['url']
                 entries = []
             outhtml += u"<h1>Contenuto di " + data['url'] + "</h1>"
             outhtml += "<ul class='files'>"
             for entry in entries:
                 try:
                     entry_url = data['url'].encode('ascii', errors='xmlcharrefreplace')
                     entry_name = entry.name.encode('ascii', errors='xmlcharrefreplace')
                     entry_ty = entry.smbc_type
                 except UnicodeEncodeError:
                     continue
                 if entry_name == ".":
                     pass
                 elif entry_name == "..":
                     entry_url = ('/').join(  entry_url.split('/')[:-1] )
                     outhtml += u"<li><a href='/cgi-bin/browse_share.cgi?url=%r'>..</a></li>" % (entry_url)
                 else:
                     smbctype = int(entry_ty)
                     if smbctype == SMBC_TYPE['file']:
                         download_from_smb = "<a href='%s/%s'>%s</a>" % (entry_url, entry_name, entry_name)
                         outhtml += u"<li class='download'>" + download_from_smb + "</li>"
                     else:
                         outhtml += "<li class='browse'><a href='/cgi-bin/browse_share.cgi?url=%s/%s'>%s</a></li>" % (entry_url, entry_name, entry_name)
             outhtml += "</ul>"
             outhtml += post_html

    print outhtml

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4


