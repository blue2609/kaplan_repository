import scrapy
from scrapy_splash import SplashRequest 


class TableauscraperSpider(scrapy.Spider):
    name = 'TableauScraper'
    allowed_domains = ['www.tableau.com']
    # start_urls = ['https://www.tableau.com/support/releases/']

    mainPageScript = '''
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(1))
        return {
            html = splash:html()
        }
    end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://www.tableau.com/support/releases/',callback=self.parse,endpoint='execute',args={
            'lua_source':self.mainPageScript
        })

    def parse(self, response):
        tableauContainerList = response.xpath("//div[@class='accordion__item']")
        for tableau_version_container in tableauContainerList :
            release_version = tableau_version_container.xpath(".//h3[@class='heading--h5']/text()").get().strip()
            maintenance_versions_list = tableau_version_container.xpath(".//a") 

            for maintenance_version in maintenance_versions_list:
                maintenance_version_link = response.urljoin(maintenance_version.xpath(".//@href").get())
                maintenance_version_text = maintenance_version.xpath(".//text()").get().strip()
                maintenance_version_releaseDate = maintenance_version.xpath(".//span/text()").get().strip()

                # yield SplashRequest(url=maintenance_version_link,callback=self.parseInstallerPage,meta={
                #     'release_version':release_version,
                #     'maintenance_version_text':maintenance_version_text,
                #     'maintenance_version_link':maintenance_version_link,
                #     'maintenance_version_releaseDate':maintenance_version_releaseDate
                # },endpoint='execute',args={
                #     'lua_source':self.installerPageScript,
                #     'timeout':90,
                #     'resource_timeout':10,
                #     'wait':20,
                #     'images':0
                # })

                yield SplashRequest(url=maintenance_version_link,callback=self.parseInstallerPage,meta={
                    'release_version':release_version,
                    'maintenance_version_text':maintenance_version_text,
                    'maintenance_version_link':maintenance_version_link,
                    'maintenance_version_releaseDate':maintenance_version_releaseDate
                },args={
                    'wait':4
                })
    
    def parseInstallerPage(self,response):

        # -- output the html output to an html file -- 
        # with open('test.html','wb') as htmlFile:
        #     htmlFile.write(response.body)

        WindowsInstaller = response.xpath("//h3[contains(text(),'Windows')]/following-sibling::ul/li/a")
        WindowsInstaller_text = WindowsInstaller.xpath(".//text()").get()
        WindowsInstaller_link = WindowsInstaller.xpath(".//@href").get()

        # add the current page URL to relative path 
        if 'https' not in WindowsInstaller_link:
            WindowsInstaller_link = response.urljoin(WindowsInstaller_link)

        yield {
            'Release Version':response.request.meta['release_version'],
            'maintenance_version_text':response.request.meta['maintenance_version_text'],
            'maintenance_version_link':response.request.meta['maintenance_version_link'],
            'maintenance_version_releaseDate':response.request.meta['maintenance_version_releaseDate'],
            'Windows Installer Link':WindowsInstaller_link,
            'Windows Installer Text':WindowsInstaller_text
        }




            
            
            
