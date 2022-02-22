import os
import zipfile

def create_proxy_extension(proxy):
    """proxy_server username:password@ip:port"""

    ip = proxy.split("@")[1].split(":")[0]
    port = int(proxy.split(":")[-1])
    login = proxy.split(":")[0]
    password = proxy.split("@")[0].split(":")[1]

    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Proxy GramLikes",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
    """

    background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };
        chrome.proxy.settings.set({value: config, scope: "regular"}, 
        function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
    """ % (
        ip,
        port,
        login,
        password,
    )

    dir_path = "assets/chrome_extensions"

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    pluginfile = "%s/proxy_auth.zip" % (dir_path)


    with zipfile.ZipFile(pluginfile, "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return pluginfile