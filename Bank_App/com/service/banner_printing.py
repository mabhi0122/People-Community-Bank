from Bank_App.com.service.constants import welcome_banner_path, exit_banner_path

def bannerPrinting():
    with open(welcome_banner_path, 'r') as fp:
        data = fp.read()
        print(data)
        return None

def exitBannerPrinting():
    with open(exit_banner_path, 'r') as fp:
        data = fp.read()
        print(data)
        return None

# bannerPrinting()
# exitBannerPrinting()