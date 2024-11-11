import { Router } from 'express';
import routesEmail from './email';
import routesFiles from './files';
import routesNews from './news';
const routes = Router();

routes.use('', routesEmail);
routes.use('', routesFiles);
routes.use('/news', routesNews);

export default routes;
