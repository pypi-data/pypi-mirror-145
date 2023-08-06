# Rawproxy

a tiny proxy server for raw.githubusercontent.com

It's so hard to fetch script from `https://raw.githubusercontent.com` sometimes.
So I create this proxy server to map `https://raw.githubusercontent/path/to/some/scripts` to `https://myhost/raw.githubusercontent/path/to/some/scripts`.
and deploy it on cloud. Accessibility improvements will make your life easier!

## Example



## Deploy to ubuntu server

```commandline
python3 -m pip install rawproxy
sudo ln -s $(python3 -m site --user-site)/rawproxy/rawproxy.service /etc/systemd/system/rawproxy.service
sudo systemctl daemon-reload
sudo systemctl start rawproxy.service
```
