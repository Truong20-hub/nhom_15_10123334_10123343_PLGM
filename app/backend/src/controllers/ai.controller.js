const aiService = require('../services/ai.service');
const logger = require('../config/logger');

exports.health = async (req, res, next) => {
  logger.info('Bắt đầu kiểm tra health AI service', { reqId: req.reqId });

  try {
    const data = await aiService.checkHealth(req.reqId);
    logger.info('Health check thành công', { reqId: req.reqId });
    res.status(200).json({ success: true, data });
  } catch (err) {
    logger.error(`Health check thất bại: ${err.message}`, { reqId: req.reqId });
    next(err);
  }
};

exports.models = async (req, res, next) => {
  logger.info('Bắt đầu lấy danh sách model', { reqId: req.reqId });

  try {
    const data = await aiService.listModels(req.reqId);
    logger.info(`Lấy danh sách model thành công (${data?.models?.length ?? 0} model)`, {
      reqId: req.reqId,
    });
    res.status(200).json({ success: true, data });
  } catch (err) {
    logger.error(`Lấy danh sách model thất bại: ${err.message}`, { reqId: req.reqId });
    next(err);
  }
};

exports.predict = async (req, res, next) => {
  const { model } = req.query;

  logger.info(`Bắt đầu predict model=${model}`, { reqId: req.reqId });

  try {
    const data = await aiService.predict(req.body, model, req.reqId);
    logger.info(`Predict thành công, kết quả=${data?.price_range}`, { reqId: req.reqId });
    res.status(200).json({ success: true, data });
  } catch (err) {
    logger.error(`Predict thất bại: ${err.message}`, { reqId: req.reqId });
    next(err);
  }
};

exports.evaluate = async (req, res, next) => {
  const { model_name, dataset_name } = req.query;

  logger.info(`Bắt đầu evaluate model=${model_name} dataset=${dataset_name}`, {
    reqId: req.reqId,
  });

  try {
    const data = await aiService.evaluate(model_name, dataset_name, req.reqId);
    logger.info(`Evaluate thành công, accuracy=${data?.accuracy}`, { reqId: req.reqId });
    res.status(200).json({ success: true, data });
  } catch (err) {
    logger.error(`Evaluate thất bại: ${err.message}`, { reqId: req.reqId });
    next(err);
  }
};