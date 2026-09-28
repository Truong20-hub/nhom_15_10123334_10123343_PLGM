const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const requestId = require('./middlewares/requestId');
const aiRoutes = require('./routes/ai.routes');
const errorHandler = require('./middlewares/errorHandler');

const app = express();

// Danh sách origin được phép (thêm domain ngrok mới vào đây nếu đổi)
const allowedOrigins = [
  'https://backtrack-alkalize-altitude.ngrok-free.dev',
  'http://localhost:5000',
  'http://localhost:8080',   // ← thêm dòng này
  'http://localhost:5173',
   'https://shoptalk-cherisher-likeness.ngrok-free.dev'   // ← thêm luôn để test trực tiếp frontend nếu cần
];

const corsOptions = {
  origin: function (origin, callback) {
    // cho phép request không có origin (Postman, curl, server-to-server...)
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS: ' + origin));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'ngrok-skip-browser-warning'],
  credentials: true,
};

// CORS - chỉ cấu hình 1 lần, middleware này đã tự xử lý preflight OPTIONS
app.use(cors(corsOptions));

app.use(express.json());
app.use(requestId);
app.use(morgan('dev'));

// Healthcheck
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    message: 'Backend healthy'
  });
});

// AI routes
app.use('/api/ai', aiRoutes);

app.get('/', (req, res) => {
  res.json({ message: 'Backend đang chạy' });
});

app.use(errorHandler);

module.exports = app;