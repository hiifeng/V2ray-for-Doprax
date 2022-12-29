# V2ray for Doprax
Create By ifeng<br>
Web Site: https://www.hicairo.com <br>
Telegram: https://t.me/HiaiFeng <br>

# 简介：
本项目用于在 Doprax.com 免费服务上部署 V2ray ，采用的方案为 Nginx + WebSocket + VMess/VLess + TLS。速度与 Replit 相比较慢，但是官方宣传不限流量，服务启动后永不停机。
# 注意事项：
<b>请勿滥用，账号封禁风险自负。</b>
# 部署：
<p>1、登录自己的 GitHub 账号后 Fork 该项目。</p>
<p>2、注册 <a href="https://www.doprax.com/signup/">Doprax.com</a> 账号登录后 Import 该项目。</p>
<p>详细使用方案请参考：https://www.hicairo.com/post/55.html</p>

# 使用方法：
<p>1、服务器端配置</p>
<p>请使用 <a href="https://www.v2fly.org/awesome/tools.html">第三方工具</a> 生成一个新的 UUID 。在 Doprax.com 登录后依次点击左侧菜单中的 Main ,窗口右侧的 Edit source code ，选择 Dockerfile 文件，编辑 UUID 及伪装地址信息保存后重启服务。</p>
<img src="https://www.hicairo.com/zb_users/upload/2022/12/202212291672276227538571.webp">
<pre class="notranslate"><code># 用新生成的 UUID 替换 de04add9-5c68-8bab-950c-08cd5320df18
ENV UUID de04add9-5c68-8bab-950c-08cd5320df18
# VMESS_WSPATH / VLESS_WSPATH 两个常量分别定义了 Vmess/VLess 的伪装路径，
# 请分别修改内容中的vmess或vless。注意：伪装路径前无需加  /
ENV VMESS_WSPATH vmess
ENV VLESS_WSPATH vless
</code></pre>

<p>2、客户端配置</p>
<p>节点客户端配置需要手动进行，下面以 V2rayN 为例。
<p>下图为 VMess 配置示意图，请修改标示内容，其他设置于图片中显示一致。(注意：此处请在伪装路径前加 / )</p>
<img src="https://www.hicairo.com/zb_users/upload/2022/12/202212291672276258394161.webp">
<p>下图为 VMess 配置示意图，请修改标示内容，其他设置于图片中显示一致。(注意：此处请在伪装路径前加 / )</p>
<img src="https://www.hicairo.com/zb_users/upload/2022/12/202212291672276274474231.webp">

# 反馈与交流：
在使用过程中，如果遇到问题，请使用Telegram与我联系。（ https://t.me/HiaiFeng ）
