## SEO Meta-Data

This a python module that helps you get SEO data on any website, you have to import it in your script and your good to go

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install seometa
```

## Usage

```python
import threading

from seo import SEO, read_txt


def get_sublists(original_list, number_of_sub_list_wanted): # sublisting to use Threads
    sublists = list()
    for sub_list_count in range(number_of_sub_list_wanted):
        sublists.append(original_list[sub_list_count::number_of_sub_list_wanted])
    return sublists


def worker(websites, file_name):
    for website in websites:
        seo_keywords = SEO(website) # init the object eg. website = 'google.com'
        seo_keywords.run(path=f'{file_name}.csv') # run the process by giving the save file


def main(): 
    websites = read_txt('website.txt') # Reading websites from a text fole
    file_name = input('File: ') 
    n = int(input('Threads: '))

    all_websites = get_sublists(websites, n)

    threads = []

    for website_list in all_websites:
        t = threading.Thread(target=worker, args=[website_list, file_name])
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
