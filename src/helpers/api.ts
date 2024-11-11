import { APP_NAME, APP_VERSION } from '../constants/app';

var convert = require('xml-js');

const Api = {
  // api parse and format response
  response(res, format, error, status, message, count = 0, data = null, onlyData = false) {
    if (res.headersSent) {
      return;
    }
    let jsonResponse;
    if (onlyData) {
      jsonResponse = data;
    } else {
      jsonResponse = {
        version: APP_NAME + ' - v' + APP_VERSION,
        error: error,
        status: status,
        message: message,
        count: count,
        data: data,
      };
    }
    if (format == 'xml') {
      // https://github.com/nashwaan/xml-js#readme
      var options = {
        compact: true,
        trim: false,
        spaces: 4,
        nativeType: true,
        addParent: false,
        alwaysArray: false,
        alwaysChildren: false,
      };
      return res.status(status).send(convert.json2xml(jsonResponse, options));
    }
    return res.status(status).send(jsonResponse);
  },
};
export default Api;
