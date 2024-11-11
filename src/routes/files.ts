import { Router } from 'express';
import FilesController from '../controllers/FilesController';
const router = Router();

router.post('/upload-request', [], FilesController.uploadRequest);
router.get('/upload-status', [], FilesController.uploadStatus);
router.post('/upload', [], FilesController.upload);

export default router;
