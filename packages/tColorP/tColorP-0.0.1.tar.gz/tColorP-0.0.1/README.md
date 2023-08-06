# TColorP

[![](https://img.shields.io/badge/language-Python-blue)](https://www.python.org/) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ruxia-TJY/TColorP) ![linux](https://img.shields.io/badge/-Linux-yellow?logo=linux) ![windows](https://img.shields.io/badge/-Windows-blue?logo=windows)

print with color.

```python
from TColorP import TColorP, TColor

tcp = TColorP()
tcp.success('success')
tcp.error('error')
tcp.warning('warning')
tcp.normal('normal')

tcp.formatColor([TColor.method_normal, TColor.foreground_cyan])
print('hello')
tcp.formatColor([TColor.method_normal])
print('TColorP')
```

![view](View.png)


## License

MIT License,Thanks!