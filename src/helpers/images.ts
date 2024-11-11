import axios from 'axios';
const fs = require('fs');

const Images = {
  // hash plain password
  async download(url, path) {
    return await axios({ url, responseType: 'stream' }).then(
      (response) =>
        new Promise((resolve, reject) => {
          response.data
            .pipe(fs.createWriteStream(path))
            .on('finish', () => resolve(true))
            .on('error', (e) => reject(e));
        }),
    );
  },
};

export default Images;
