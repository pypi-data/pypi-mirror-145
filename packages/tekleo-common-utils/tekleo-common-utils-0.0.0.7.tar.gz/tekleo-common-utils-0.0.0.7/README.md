# TekLeo Common Utils
A python package with shared utils methods that can be used in a variety of python projects, but are mostly tailored towards web / ml applications.


# Description
Under construction...

### Utils OpenCV
- `blur_gaussian` apply Gaussian blur
- `rotate_bound` rotate image bounded, preserving the original dimensions and cutting all rotated content that doesn't fit into original image size 
- `rotate_free` rotate image freely, changing dimensions to make sure all rotated content fits inside
- `deskew` deskew (straighten) image, works best on text images, like page scans and etc.

### Utils Random
- `get_random_user_agent` generate a random User-Agent for HTTP headers (using [user_agent library](https://pypi.org/project/user-agent/)) 

# Installation
 
## Normal installation

```bash
pip install tekleo-common-utils
```

## Development installation

```bash
git clone https://github.com/jpleorx/tekleo-common-utils.git
cd tekleo-common-utils
pip install --editable .
```

# Links
In case you’d like to check my other work or contact me:
* [Personal website](https://tekleo.net/)
* [GitHub](https://github.com/jpleorx)
* [PyPI](https://pypi.org/user/JPLeoRX/)
* [DockerHub](https://hub.docker.com/u/jpleorx)
* [Articles on Medium](https://medium.com/@leo.ertuna)
* [LinkedIn (feel free to connect)](https://www.linkedin.com/in/leo-ertuna-14b539187/)