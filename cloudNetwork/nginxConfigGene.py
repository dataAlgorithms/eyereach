#!/usr/bin/python

import os
import re 

httpHead = '''
user  root;
worker_processes 2;
#worker_cpu_affinity 0001;
#rtmp_auto_push on;
#rtmp_auto_push_reconnect 1s;
#rtmp_socket_dir /home/work/nginx/test-conf/stat_test/edge;
error_log   /usr/local/sms/logs/error.log debug;
worker_rlimit_nofile 30000;
worker_rlimit_core 10240000000;
working_directory /tmp;
pid /usr/local/sms/logs/nginx.pid;

events {
    worker_connections  1024;
    accept_mutex off;
}

http {
    resolver 119.29.29.29;

    log_format http_logformat '$msec' ' $request_time' ' $remote_addr' ' -/$status' ' $bytes_sent' ' $request_method' ' $scheme://$host$request_uri' ' -' ' -' ' PLAY' ' "$http_referer"' ' "$escape_http_user_agent"' ' -' ' )@out#(RL=$req
uest_length' '^~${DOLLAR}' 'PRTCL=$server_protocol' '^~${DOLLAR}' 'DUR=$request_time';
    access_log  /data/proclog/log/sms/access/http_access.log http_logformat;
    lua_shared_dict rtmp_dict 10m;
    lua_shared_dict stat_shared_dict 10m;
    init_by_lua_file '/usr/local/sms/lua/control/init_actioin.lua';
    init_worker_by_lua_file '/usr/local/sms/lua/control/init_worker_action.lua';
    lua_package_path "/usr/local/sms/lua/?.lua;/usr/local/sms/lua/limit_center/?.lua;/usr/local/sms/3party/?.lua;/usr/local/sms/3party/lib/?.lua;;";
    lua_package_cpath "/usr/local/sms/3party/?.so;/usr/local/sms/3party/lib/?.so;;";
    geo $DOLLAR {default "$";}

    lua_shared_dict report 10m;

    server {
        listen 8080;
        server_name cc_public;

        proxy_intercept_errors on;
        recursive_error_pages on;
        location  / {
                set $user_host $arg_cchost;
                if ($query_string ~* "cchost=[^&]+&?(.*)&interclient=[^&]+") {
                        set $user_args $1;
                        rewrite ^ $uri?$user_args? break;
                }

                proxy_pass http://$user_host;
                proxy_set_header Host $user_host;
                error_page 302 = @error_page_302;
        }
        location ~ /proxyto/([^/]+)(.*) {
            proxy_pass http://$1$2$is_args$query_string;
            error_page 302 = @error_page_302;
        }
        location @error_page_302 {
            rewrite_by_lua '
                local _, _, upstream_http_location = string.find(ngx.var.upstream_http_location, "^http:/(.*)$")
                ngx.header["cnkedao"] = "/proxyto" .. upstream_http_location
                ngx.exec("/proxyto" .. upstream_http_location);
            ';
        }
    }

'''

http = '''

    #####################http start###################
    server {
        listen 8080;
        server_name cc_common; 

        proxy_intercept_errors on;
        recursive_error_pages on;
        location  / {
            if ($arg_ratio) {
                rewrite ^(.*)_(\d+).flv$ $1.flv break;
            }

            proxy_pass http://$arg_cchost$uri?$args;
            proxy_set_header Host $arg_cchost;
            error_page 302 = @error_page_302;
        }
        location ~ /proxyto/([^/]+)(.*) {
            proxy_pass http://$1$2$is_args$query_string;
            error_page 302 = @error_page_302;
        }
        location @error_page_302 {
            rewrite_by_lua '
                local _, _, upstream_http_location = string.find(ngx.var.upstream_http_location, "^http:/(.*)$")
                ngx.header["cnkedao"] = "/proxyto" .. upstream_http_location
                ngx.exec("/proxyto" .. upstream_http_location);
            ';
        }
    }

    upstream flv.common.8080 {
        server  127.0.0.1:8080;
        localfirst;
        #keepalive 1024;
    }

    server {
        listen 80;
        server_name %s;

        location ~* \.flv$ {
            if ($arg_cchost) {
                break;
            }
            if ($arg_ratio) {
                rewrite ^(.*).flv$ $1_$arg_ratio.flv?cchost=$host last;
            }
            if ($arg_ratio = "") {
                rewrite ^(.*).flv$ $1.flv?cchost=$host last;
            }

            http_live on;
 
            gop_enable on;
            gop_min 250;
            zero_timestamp on;
            
            stream_type live_flv;
            
            live_proxy_connect_timeout 10s;
            live_proxy_http_version 1.1;
            live_proxy_ignore_client_abort off;
            live_proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504 http_403 http_404;
            add_header Cache-Control no-cache;
            add_header Content-Type video/x-flv;
            add_header Access-Control-Allow-Origin *;
            add_header Server "";
            live_proxy_pass http://flv.common.8080;
            live_proxy_set_header Host cc_common;
        }
    }

    #############http end##########################
}
'''

rtmpHead = '''

rtmp {
    resolver 119.29.29.29 valid=1s;

    log_format fms_access_logformat $msec ' ' $session_time ' ' $remote_addr ' ' '-' ' ' $bytes_sent ' '  $command ' '
           $tcurl/$name?$args ' ' '-' ' ' '-' ' ' $command ' ' '"' $pageurl '"' ' ' '"' $flashver '"' ' ' '-' ' '
           ")@out#(RL=" $bytes_received;

    access_log  /data/proclog/log/sms/access/access.log   fms_access_logformat;

    rtmp_billing off;                           #billing switch
    rtmp_billing_port  10000;
    rtmp_billing_interval 300;                   #billing calculate interval (s)
    rtmp_billing_log_path /data/proclog/log/sms/billing;     #directory where billing file stores
    rtmp_billing_path /usr/local/sms/sbin/rtmpbillingd;    #directory where billing process stores
    rtmp_billing_pid_path /var/run;     #directory where billing process id file stores
'''

rtmp = '''
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

def httpConfig(sUrls):

    if sUrls is None:
        return
    lUrls = re.split("\s+", sUrls)
    lUrls = [i for i in lUrls if not len(i) == 0]
    sUrls = ' '.join(lUrls)

    config = http % (sUrls)
    ng.write('%s%s' % (config, os.linesep))
    

def rtmpConfig(sUrls):

    if sUrls is None:
        return

    lUrls = re.split("\s+", sUrls)

    configs = ""

    for url in lUrls:
        if len(url) == 0:
            continue
        config = rtmp % (url, url, url)
        ng.write('%s%s' % (config, os.linesep))
        configs += config

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

    ng = open('nginxConfig.conf', 'w')

    # wrte http header 
    ng.write(httpHead)

    # write http
    httpConfig(sUrls)

    # write rtmp header
    ng.write(rtmpHead)

    # wrtie rtmp
    rtmpConfig(sUrls)

    # write rtmp close quote
    ng.write('}%s' % os.linesep) 
