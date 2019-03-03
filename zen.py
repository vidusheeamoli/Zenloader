from bs4 import BeautifulSoup
import requests
import lxml
import os
import urllib


def mkdir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)


if __name__ == '__main__':
	mkdir('./output') #make output directory if not already made
	output_dir = os.path.join(os.path.dirname(__file__), 'output')

	first_source = requests.get("https://zenpencils.com/archives/").text
	first_soup = BeautifulSoup(first_source, 'lxml')
	spans = first_soup.find_all('span', attrs={'class': 'comic-archive-title'})
	for span in spans:
		link = span.find('a')
		if link.has_attr('href'):
			image_link = link.attrs['href']
			second_source = requests.get(image_link).text
			second_soup = BeautifulSoup(second_source, 'lxml')
			all_divs = second_soup.find_all('div')
			heads = second_soup.find_all('h2')
			'''finding comic title'''
			for head in heads:
				image_title = head.text
				filename = ""
				for i in image_title:
					if i != ':':
						filename = filename + i
				print filename
				break
			'''checking if multiple images present'''
			image_list = []
			for img_div in all_divs:
				if img_div.has_attr('id'):
					if img_div.attrs['id'] == 'comic':
						img_sources = img_div.find_all('img')
						for img_src in img_sources:
							if img_src.has_attr('src'):
								image_list.append(img_src.attrs['src'])
						if len(image_list) == 1: # if only 1 image, download normally.
							filename = filename+'.jpg'
							output_path = output_dir+'/'+filename
							with open(output_path, 'wb') as output_img:
								output_img.write(urllib.urlopen(image_list[0]).read())
								output_img.close()
						else : #if multiple images, make a new directory
							new_directory_address = './output/'+filename
							mkdir(new_directory_address)
							new_output_dir = os.path.join(output_dir, filename)
							temp = 1
							for images in image_list:
								filename = str(temp) + '.jpg'
								output_path = new_output_dir+'/'+filename
								with open(output_path, 'wb') as output_img:
									output_img.write(urllib.urlopen(images).read())
									output_img.close()
								temp = temp + 1





