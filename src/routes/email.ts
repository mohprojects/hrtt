import { Router } from 'express';
import EmailController from '../controllers/EmailController';
const router = Router();

router.post('/send-mail', [], EmailController.send);

export default router;
