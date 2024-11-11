import { Router } from 'express';
import NewsController from '../controllers/NewsController';
const router = Router();

router.post('/fetch', [], NewsController.fetch);

export default router;
