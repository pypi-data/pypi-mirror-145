# officy

common python code for office use. like dir,file,etc.

办公用途的常用 python 代码，比较多涉及到文本、文件、文件夹、网页等。

### Install:

```sh
pip install officy
```

or :

```sh
pip install -r requirements.txt
```

如果您有需要，可以 clone 到本地，比如，在 `/work-space>` 下执行 ```git clone https://github.com/liujuanjuan1984/officy.git```。

完成后，`cd officy` 后所在目录/路径，请添加到 `PYTHONPATH` 环境变量中。

### How to use:

```py
from officy import Dir,JsonFile
Dir(".").black()
JsonFile("temp.json").read({})
```
