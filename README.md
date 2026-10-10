# 反诈二维码演练页（GitHub Pages + 不蒜子 版）

纯静态方案：页面托管在 GitHub Pages，计数用不蒜子的免费统计脚本。没有后端，没有服务器，没有账号费用。

与 EdgeOne Pages 版（`../fanzha_qrcode`）相比，这一版的代价是：计数在第三方服务器上，不能归零、不能修改；不蒜子是个人维护的免费服务，偶尔 502。

## 目录结构

```
index.html                   # 根路径，只做跳转到 course/register/
course/register/index.html   # 落地页，二维码指向这里
.nojekyll                    # 告诉 GitHub Pages 不要用 Jekyll 处理
tools/make_qr.py             # 生成二维码
```

## 本地预览

```bash
python3 -m http.server 8790
```

打开 `http://localhost:8790/course/register/`。本地预览时页面会识别出是内网地址，显示一个模拟数字，不会去碰线上计数。

## 部署步骤

### 1. 建仓库并推送

在 GitHub 新建一个**公开**仓库（私有仓库的 Pages 需要付费），名字就是网址的一部分，建议用不显眼的名字，比如 `open-course`。然后在本目录执行：

```bash
git init
git add .
git commit -m "init"
git branch -M main
git remote add origin https://github.com/<你的用户名>/open-course.git
git push -u origin main
```

### 2. 开启 GitHub Pages

仓库页面 **Settings → Pages**，Source 选 **Deploy from a branch**，Branch 选 `main`，目录选 `/ (root)`，保存。等一两分钟，页面顶部会出现网址：

```
https://<你的用户名>.github.io/open-course/
```

落地页完整地址是：

```
https://<你的用户名>.github.io/open-course/course/register/
```

### 3. 生成二维码

```bash
python3 -m venv .venv
.venv/bin/pip install "qrcode[pil]"
.venv/bin/python tools/make_qr.py https://<你的用户名>.github.io/open-course/course/register/ -o output/qr.png
```

### 4. 正式发布前

- 用真机扫一次确认能打开、能出数字。
- 把你测试产生的访问次数填进 `course/register/index.html` 里的 `COUNT_OFFSET`，显示时会减掉。改完重新 push，等一分钟生效。
- 页脚的"制作方：XXXX"改成你的课程或单位名称。

## 必须知道的几个限制

**计数按域名算，不按页面算。** 不蒜子统计 `site_pv` 时，把 `<你的用户名>.github.io` 下的所有页面算在一起。如果你的 GitHub 账号已经用 Pages 放过别的东西（博客、作业等），数字会混在一起。最干净的做法是**新注册一个 GitHub 账号专门放这个项目**。

**为什么不用按页面统计的 page_pv。** 不蒜子靠 Referer 头识别页面，iPhone 上的 Safari 和微信内置浏览器出于隐私只会发送域名，不发完整路径，于是 iPhone 用户全部被记到站点根目录下，数字就乱了。`site_pv` 不依赖这个，所以更稳。

**不能归零。** 数据在不蒜子服务器上，没有后台可以改。想从 1 开始只能换一个全新的域名（也就是新 GitHub 账号），或者用 `COUNT_OFFSET` 把已有数字减掉。

**同一个人刷新不会重复计数。** 编号第一次拿到后存在手机 localStorage 里，之后打开直接显示，不再加载计数脚本。清了浏览器数据或换设备就算新的一个人。

**不蒜子不稳定时怎么办。** 页面已经做了自动重试：单次等 4 秒，最多试 3 次，之后才显示横杠。实测不蒜子接口会间歇性 502，重试能挡掉大部分。如果还是经常失败，把 `course/register/index.html` 里的 `COUNTER` 从 `'busuanzi'` 改成 `'vercount'`。Vercount 是兼容不蒜子的免费替代，不靠 Referer，稳定得多，页面其他地方不用改。

**国内访问。** `github.io` 在国内时通时不通，手机流量下一般能开，但可能要等几秒。微信打开境外域名会弹"非微信官方网页"提示，点继续即可。如果试下来打不开的比例高，就换回 EdgeOne Pages 版。
