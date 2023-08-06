import http.client
import re
import traceback
import urllib
import urllib.parse

HTTP_PROXY_HEADER_NAME = ["HTTP_X_FORWARDED_FOR", "X-FORWARDED-FOR", "CLIENTIP", "REMOTE_ADDR"]
HTTP_USER_AGENT = ["HTTP_USER_AGENT", "USER_AGENT" "USER-AGENT"]
HTTP_HOST = ["HTTP_HOST", "HOST"]


class Platform(object):
    UNKNOW = 0
    WINSOWS = 1
    IPHONE = 2
    IPAD = 3
    MAC = 4
    ANDROID = 5
    LINUX = 6


class HttpUtils(object):

    def __init__(self, host):
        self.host = host
        self.reqheaders = {'Content-type': 'application/x-www-form-urlencoded',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Host': host,
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1', }

    def get(self, url, param):
        conn = None
        res = None
        try:
            conn = http.client.HTTPConnection(self.host)
            if param is not None:
                data = urllib.parse.urlencode(param)
                conn.request("GET", url + "?" + data, headers=self.reqheaders)
            else:
                conn.request("GET", url, headers=self.reqheaders)
            res = conn.getresponse().read()
        except:
            print(traceback.print_exc())
        finally:
            if conn:
                conn.close()
        return res

    def get_with_ssl(self, url, param):
        conn = None
        res = None
        try:
            conn = http.client.HTTPSConnection(self.host)
            if param is not None:
                data = urllib.parse.urlencode(param)
                conn.request("GET", url + "?" + data, headers=self.reqheaders)
            else:
                conn.request("GET", url, headers=self.reqheaders)
            res = conn.getresponse().read()
        except:
            print(traceback.print_exc())
        finally:
            if conn:
                conn.close()
        return res

    def post(self, url, param):
        conn = None
        res = None
        try:
            conn = http.client.HTTPConnection(self.host)
            if param is not None:
                data = urllib.parse.urlencode(param)
                conn.request('POST', url, data, self.reqheaders)
            else:
                conn.request('POST', url, headers=self.reqheaders)
            res = conn.getresponse().read()
        except:
            print(traceback.print_exc())
        finally:
            if conn:
                conn.close()
        return res

    def post_with_ssl(self, url, param):
        conn = None
        res = None
        try:
            conn = http.client.HTTPSConnection(self.host)
            if param is not None:
                data = urllib.parse.urlencode(param)
                conn.request('POST', url, data, self.reqheaders)
            else:
                conn.request('POST', url, headers=self.reqheaders)
            res = conn.getresponse().read()
        except:
            print(traceback.print_exc())
        finally:
            if conn:
                conn.close()
        return res


def get_client_ip(headers):
    return get_client_ip_with_header(headers)


def get_host(headers):
    headers_upper = {}
    for k, v in headers.items():
        headers_upper[k.upper()] = v
    for name in HTTP_HOST:
        if name in headers_upper:
            ip = headers_upper[name]
            if len(ip) > 0:
                return ip
    return ''


def get_client_ip_with_header(headers):
    headers_upper = {}
    for k, v in headers.items():
        headers_upper[k.upper()] = v
    for name in HTTP_PROXY_HEADER_NAME:
        if name in headers_upper:
            ip = headers_upper[name]
            if len(ip) > 0:
                return ip.split(",")[0]
    return ''


def get_client_platform(headers):
    headers_upper = {}
    for k, v in headers.items():
        headers_upper[k.upper()] = v
    for name in HTTP_USER_AGENT:
        if name in headers_upper:
            user_agent = headers_upper[name].upper()
            if "WINDOWS" in user_agent:
                return Platform.WINSOWS
            if "IPHONE" in user_agent:
                return Platform.IPHONE
            if "IPAD" in user_agent:
                return Platform.IPAD
            if "MAC" in user_agent:
                return Platform.MAC
            if "ANDROID" in user_agent:
                return Platform.ANDROID
            if "LINUX" in user_agent:
                return Platform.LINUX
    return Platform.UNKNOW


def get_user_agent(headers):
    headers_upper = {}
    for k, v in headers.items():
        headers_upper[k.upper()] = v
    for name in HTTP_USER_AGENT:
        if name in headers_upper:
            user_agent = headers_upper[name].upper()
            return user_agent
    return ''


def is_mobile(headers):
    """
    is pc or mobile
    :param headers:
    :return:
    """
    headers_upper = {}
    for k, v in headers.items():
        headers_upper[k.upper()] = v
    factor = ''
    for name in HTTP_USER_AGENT:
        if name in headers_upper:
            factor = headers_upper[name]
            break
    is_mobile = False
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp' \
                    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)' \
                    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)' \
                     r'|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)' \
                     r'|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw' \
                     r'|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8' \
                     r'|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit' \
                     r'|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)' \
                     r'|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji' \
                     r'|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx' \
                     r'|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi' \
                     r'|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)' \
                     r'|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg' \
                     r'|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21' \
                     r'|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-' \
                     r'|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it' \
                     r'|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)' \
                     r'|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)' \
                     r'|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit' \
                     r'|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'

    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(factor) is not None:
        is_mobile = True
    user_agent = factor[0:4]
    if _short_matches.search(user_agent) is not None:
        is_mobile = True

    return is_mobile
