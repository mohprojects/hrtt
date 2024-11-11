import { HTTP_STATUS, HTTP_STATUS_MESSAGES } from '../constants/status.http';
import Api from '../helpers/api';
import Mail from '../helpers/mail';

class EmailController {
  static send = async (req, res) => {
    try {
      let { subject, html, emailFr, emailTo } = req.body;
      // send mail
      Mail.sendBackground(subject, html, req.body);
      return Api.response(
        res,
        req.headers.format,
        false,
        HTTP_STATUS.OK,
        HTTP_STATUS_MESSAGES.OK,
        1,
        'Success',
      );
    } catch (e) {
      return Api.response(res, req.headers.format, true, HTTP_STATUS.SERVER_ERROR, e.message);
    }
  };
}

export default EmailController;
