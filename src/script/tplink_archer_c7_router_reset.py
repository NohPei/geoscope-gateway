import hashlib
import urllib
import urllib2
import sys

ROUTER_IP = "192.168.60.1"
USERNAME = "geoscope"
PASSWORD = "soupgeo"


class TPLink_Archer_C7_Router_Web_Interface:
    """ Class for scraping/navigating the TPLink Archer C7 Router Web UI. Originally for
    the purpose of scheduling reboots using cron. Can probably be extended to automate
    many other functions in the web UI with a little bit of snooping around the html.

    Only tested on the Archer C7, but I imagine there's a good chance it would work on 
    other models if they use the same Web UI. 

    https://github.com/vicwomg
    """

    def __init__(self, router_ip, username, password):
        self.latest_tested_version = "3.15.3 Build 180114 Rel.39265n"

        self.login_url = "http://%s/userRpm/LoginRpm.htm?Save=Save"
        self.reboot_url_path = "/userRpm/SysRebootRpm.htm"

        self.router_ip = router_ip
        self.username = username
        self.password = password

    def login(self):
        print "Logging in to router..."
        self.cookie = self.get_auth_cookie()
        self.get_session_url()

    def get_auth_cookie(self):
        hexmd5_pw = hashlib.md5(self.password).hexdigest()
        auth_string = urllib.quote_plus(
            (self.username + ":" + hexmd5_pw).encode('base64').strip())
        cookie = "Authorization=Basic%20" + auth_string
        return cookie

    def get_session_url(self):
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', self.cookie))
        f = opener.open(self.login_url % self.router_ip)
        output = f.read()
        router_url = "http://%s/" % self.router_ip
        if (router_url in output):
            url_auth_string = output.split(
                self.router_ip + '/')[1].split('/')[0]
            self.session_url = "http://%s/%s" % (
                self.router_ip, url_auth_string)
            opener.close()
            f.close()
            print "Session URL is: " + self.session_url
        else:
            print "ERROR: Failed to scrape out session url. "
            print "  Bad username/password? "
            print "  Or you're already logged in to the admin interface somewhere else?"
            print "  Or perhaps unsupported web UI firmware. Last tested on: " + self.latest_tested_version
            sys.exit(1)

    def reboot(self):

        reboot_params = "?Reboot=Reboot"
        referer = self.session_url + self.reboot_url_path
        reboot_command_url = referer + reboot_params
        print "Rebooting router with: %s ..." % reboot_command_url

        opener = urllib2.build_opener()

        # needs proper cookie and referer or it will fail authorization
        opener.addheaders.append(('Cookie', self.cookie))
        opener.addheaders.append(('Referer', referer))

        f = opener.open(reboot_command_url)
        opener.close()
        f.close()
        print "Reboot command sent"


def main():
    tp = TPLink_Archer_C7_Router_Web_Interface(ROUTER_IP, USERNAME, PASSWORD)
    tp.login()
    tp.reboot()


if __name__ == "__main__":
    main()
