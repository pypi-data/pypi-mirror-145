import datetime


def open_urls(*urls):
    """打开一组 url，调用时可以单个变量 open_urls(url)，也可以 open_urls(*urls) 其中 urls 为一个序列"""
    import webbrowser as web

    for url in urls:
        web.open(url)


def open_questions(qids):
    """打开一组 xue.cn 习题id的习题独立页"""
    urls = init_urls_by_qids(*qids)
    open_urls(*urls)


def init_urls_by_qids(*qids):
    return [f"https://xue.cn/hub/app/exercise/{qid}" for qid in qids]


def download_files(imgdir, *urls):
    """批量下载，可下载 url 文件或图片"""
    from urllib.request import urlretrieve

    # 检查文件夹是否存在
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    fail_urls = []
    for url in urls:
        # 下载图片并按规则保存到本地
        ifile = f"{imgdir}\\{url.split('/')[-1]}"

        try:
            urlretrieve(url, ifile)
            print(datetime.datetime.now(), url, "done...")
        except Exception as e:
            print(e)
            fail_urls.append(url)

    # 下载结果
    if len(fail_urls) == 0:
        return print("all is done,图片存放于", imgdir)
    else:
        print(len(fail_urls), "张图片下载失败了")
        return fail_urls


def init_urls_by_qids(*qids):
    return [f"https://xue.cn/hub/app/exercise/{qid}" for qid in qids]


def open_chapters(paths):
    """打开一组 xue.cn 章节的独立网页"""
    import webbrowser as web

    booksinfo = JsonFile(FILE_INFO["names"]).read()
    for path in paths:
        bs = path.split("%2F", maxsplit=1)
        for bi in booksinfo:
            if bi["dirname"] == bs[0]:
                url = f'https://xue.cn/hub/reader?bookId={bi["book_id"]}&path={bs[0]}/{bs[1]}'
                web.open(url)
                break
