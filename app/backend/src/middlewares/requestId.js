const { v4: uuidv4 } = require('uuid');
const logger = require('../config/logger');

function requestId(req, res, next) {
  req.reqId = uuidv4().slice(0, 8); // rút gọn cho dễ đọc log
  const start = Date.now();

  logger.info(`--> ${req.method} ${req.originalUrl}`, { reqId: req.reqId });

  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info(`<-- ${req.method} ${req.originalUrl} ${res.statusCode} (${duration}ms)`, {
      reqId: req.reqId,
    });
  });

  next();
}

module.exports = requestId;