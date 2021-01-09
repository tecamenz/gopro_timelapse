from html.parser import HTMLParser
import urllib.request
import json

class DirParser(HTMLParser):
    dirs = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if attrs[0][0] == 'href':
                href = attrs[0][1]
                if 'GOPRO' in href:
                    self.dirs.append(href)



class ImageParser(HTMLParser):
    images = []
    def handle_starttag(self, tag, attrs):
        if tag =='a':
            if attrs[0][0] == 'href':
                href = attrs[0][1]
                if 'JPG' in href: 
                    self.images.append(href)



if __name__ == "__main__":
    image_urls = []
    ret = urllib.request.urlopen('http://10.5.5.9/videos/DCIM')
    dcim = ret.read().decode()
    print(dcim)
    dir_parser = DirParser()
    im_parser = ImageParser()
    dir_parser.feed(dcim)
    for d in dir_parser.dirs:
        directory = d.split('/')[-2]
        ret = urllib.request.urlopen('http://10.5.5.9/videos/DCIM/'+directory)
        uri = ret.read().decode()
        im_parser.feed(uri)

    images_sorted = im_parser.images
    # jsonString = json.dumps(images_sorted)
    with open('images.json', 'w') as f:
        json.dump(images_sorted, f)
        
    # images_sorted = sorted(images_sorted, reverse=True)
    im = images_sorted[-300]
    url = 'http://10.5.5.9' + im
    filename = im.split('/')[-1]
    urllib.request.urlretrieve(url, filename)
