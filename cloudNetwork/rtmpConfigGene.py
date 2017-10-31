#!/usr/bin/python

import os
import re 

basic = '''
    server {
        listen 1935;
        server_name %s;      #vhost name
        timeout 10s;

        zero_timestamp on;        #timestamp reset switch
        gop_enable on;            #gop switch

        playagain_as_stoppause on;
        ignore_closestream    on;
        swf_check off;                       #off means swf check disable 
        swf_path /usr/local/sms_bak/swf/;    #directory where swf file stores
        swf_interval 60;                     #the time interval judge swf file update

        default_app on;

        application sms_default_app {
            pull local;
            live on;
            idle_streams on;
            idle_streams_timeout 30s;
            pull rtmp://%s dynamic;
            push rtmp://%s dynamic;
        }       
    }
'''

def rtmpConfig(sUrls):

    if sUrls is None:
        return

    lUrls = re.split("\s+", sUrls)
    print(lUrls)

    configs = ""

    f = open('rtmpConfig', 'w')

    for url in lUrls:
        if len(url) == 0:
            continue
        config = basic % (url, url, url)
        f.write('%s%s' % (config, os.linesep))
        configs += config

    f.close()
    print(configs)

if __name__ == "__main__":
    sUrls = '''
ks.pull.yximgs.com

tx.pull.yximgs.com

ws.pull.yximgs.com
ws01.pull.yximgs.com
ws02.pull.yximgs.com
ws03.pull.yximgs.com

ali.pull.yximgs.com

tx-game.pull.yximgs.com

bd.pull.yximgs.com

xy.pull.yximgs.com
xy01.pull.yximgs.com
    '''

    rtmpConfig(sUrls)
    
'''
[root@RND-SM-1-59Q cs]# more rtmpConfig 

    server {
        listen 1935;
        server_name ks.pull.yximgs.com;      #vhost name
        timeout 10s;

        zero_timestamp on;        #timestamp reset switch
        gop_enable on;            #gop switch

        playagain_as_stoppause on;
        ignore_closestream    on;
        swf_check off;                       #off means swf check disable 
        swf_path /usr/local/sms_bak/swf/;    #directory where swf file stores
        swf_interval 60;                     #the time interval judge swf file update

        default_app on;

        application sms_default_app {
            pull local;
            live on;
            idle_streams on;
            idle_streams_timeout 30s;
            pull rtmp://ks.pull.yximgs.com dynamic;
            push rtmp://ks.pull.yximgs.com dynamic;
        }       
    }


    server {
        listen 1935;
        server_name tx.pull.yximgs.com;      #vhost name
        timeout 10s;

        zero_timestamp on;        #timestamp reset switch
        gop_enable on;            #gop switch

        playagain_as_stoppause on;
        ignore_closestream    on;
        swf_check off;                       #off means swf check disable 
        swf_path /usr/local/sms_bak/swf/;    #directory where swf file stores
        swf_interval 60;                     #the time interval judge swf file update

        default_app on;

        application sms_default_app {
            pull local;
            live on;
            idle_streams on;
            idle_streams_timeout 30s;
            pull rtmp://tx.pull.yximgs.com dynamic;
            push rtmp://tx.pull.yximgs.com dynamic;
        }       
    }


    server {
        listen 1935;
        server_name ws.pull.yximgs.com;      #vhost name
        timeout 10s;

        zero_timestamp on;        #timestamp reset switch
        gop_enable on;            #gop switch

        playagain_as_stoppause on;
        ignore_closestream    on;
        swf_check off;                       #off means swf check disable 
        swf_path /usr/local/sms_bak/swf/;    #directory where swf file stores
        swf_interval 60;                     #the time interval judge swf file update

        default_app on;

        application sms_default_app {
            pull local;
            live on;
            idle_streams on;
            idle_streams_timeout 30s;
            pull rtmp://ws.pull.yximgs.com dynamic;
            push rtmp://ws.pull.yximgs.com dynamic;
        }       
    }


    server {
        listen 1935;
        server_name ws01.pull.yximgs.com;      #vhost name
        timeout 10s;

        zero_timestamp on;        #timestamp reset switch
        gop_enable on;            #gop switch

        playagain_as_stoppause on;
        ignore_closestream    on;
        swf_check off;                       #off means swf check disable 
        swf_path /usr/local/sms_bak/swf/;    #directory where swf file stores
        swf_interval 60;                     #the time interval judge swf file update

        default_app on;

        application sms_default_app {
            pull local;
            live on;
            idle_streams on;
            idle_streams_timeout 30s;
            pull rtmp://ws01.pull.yximgs.com dynamic;
            push rtmp://ws01.pull.yximgs.com dynamic;
        }       
    }


    server {
        listen 1935;
        server_name ws02.pull.yximgs.com;      #vhost name
        timeout 10s;

        zero_timestamp on;        #timestamp reset switch
        gop_enable on;            #gop switch

        playagain_as_stoppause on;
        ignore_closestream    on;
        swf_check off;                       #off means swf check disable 
        swf_path /usr/local/sms_bak/swf/;    #directory where swf file stores
        swf_interval 60;                     #the time interval judge swf file update

        default_app on;

        application sms_default_app {
            pull local;
            live on;
            idle_streams on;
            idle_streams_timeout 30s;
            pull rtmp://ws02.pull.yximgs.com dynamic;
            push rtmp://ws02.pull.yximgs.com dynamic;
        }       
    }
'''
