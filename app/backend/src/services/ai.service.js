const axios = require('axios');
const { AI_SERVICE_URL } = require('../config/env');
const logger = require('../config/logger');

const aiClient = axios.create({
  baseURL: AI_SERVICE_URL,
  timeout: 15000,
});

exports.checkHealth = async (reqId) => {
  logger.info('Gọi AI service GET /health', { reqId });
  const res = await aiClient.get('/health');
  logger.info(`AI service trả về status ${res.status}`, { reqId });
  return res.data;
};

exports.listModels = async (reqId) => {
  logger.info('Gọi AI service GET /api/models', { reqId });
  const res = await aiClient.get('/api/models');
  logger.info(`AI service trả về status ${res.status}`, { reqId });
  return res.data;
};

exports.predict = async (mobileData, modelName = 'best_model.pkl', reqId) => {
  logger.info(`Gọi AI service POST /api/predict model=${modelName}`, { reqId });
  const res = await aiClient.post('/api/predict', mobileData, {
    params: { model: modelName },
  });
  logger.info(`AI service trả về status ${res.status}`, { reqId });
  return res.data;
};

exports.evaluate = async (modelName, datasetName, reqId) => {
  logger.info(`Gọi AI service GET /api/evaluate model=${modelName} dataset=${datasetName}`, {
    reqId,
  });
  const res = await aiClient.get('/api/evaluate', {
    params: { model_name: modelName, dataset_name: datasetName },
  });
  logger.info(`AI service trả về status ${res.status}`, { reqId });
  return res.data;
};