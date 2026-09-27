const http = require('http');
const httpProxy = require('http-proxy');

const proxy = httpProxy.createProxyServer();

const server = http.createServer((req, res) => {
  if (req.url.startsWith('/api')) {
    proxy.web(req, res, { target: 'http://localhost:5000' }, () => {
      res.writeHead(502);
      res.end('Backend lỗi hoặc chưa chạy');
    });
  } else {
    proxy.web(req, res, { target: 'http://localhost:5173' }, () => {
      res.writeHead(502);
      res.end('Frontend lỗi hoặc chưa chạy');
    });
  }
});

server.on('upgrade', (req, socket, head) => {
  proxy.ws(req, socket, head, { target: 'http://localhost:5173' });
});

server.listen(8001, () => {
  console.log('✅ Proxy đang chạy tại http://localhost:8001');
});