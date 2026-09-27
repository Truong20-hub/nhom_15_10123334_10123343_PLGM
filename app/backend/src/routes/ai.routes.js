const express = require('express');
const router = express.Router();
const aiController = require('../controllers/ai.controller');

router.get('/health', aiController.health);
router.get('/models', aiController.models);
router.post('/predict', aiController.predict);
router.get('/evaluate', aiController.evaluate);

module.exports = router;