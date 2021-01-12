def return_html_str(str):
    html_str = '<html lang="en"><head><title>图</title><meta charset="utf-8"><style>img {display: block; width: 100%;}</style></head><body>%s</body></html>' % str
    return html_str
with open('2020-12-07/index.html', 'w') as f:
    html = return_html_str(123)
    f.write(html)
    f.close()