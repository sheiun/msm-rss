# MSM RSS

<https://m.nexon.com/forum/310>

```js
copy(
  Array.from(document.querySelectorAll("a.list-group-item")).map((el) => ({
    id: parseInt(el.getAttribute("href").split("/")[3]),
    name: el.children[0].children[1].children[0].innerText,
    desc: el.children[0].children[1].children[1].innerText,
  }))
);
```

## Caddyfile

```caddyfile
<YOUR_DOMAIN> {
	file_server /msm.xml {
		root /home/sheiun/msm-rss/static/
		index msm.xml
	}
}
```

## Corntab

`crontab -e`

```plain
0 */1 * * * cd /home/sheiun/msm-rss/ && python3.9 feed.py
```
