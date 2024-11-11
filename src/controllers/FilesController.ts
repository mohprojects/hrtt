import { FILE_EXTENSIONS_HINT, FILE_MAX_SIZE, FILE_MAX_SIZE_HINT } from '../config/files';
import { HTTP_STATUS, HTTP_STATUS_MESSAGES } from '../constants/status.http';
import Api from '../helpers/api';
import Random from '../helpers/random';
const { promisify } = require('util');
const Busboy = require('busboy');
const path = require('path');
const fs = require('fs');
const getFileDetails = promisify(fs.stat);

const getTempPath = (fileKey, fileDir, fileName) => {
  let path = 'tmp';
  if (!fs.existsSync(path)) {
    fs.mkdirSync(path, { recursive: true });
  }
  return path + '/' + fileName;
};

const getUploadsPath = (fileKey, fileDir, fileName) => {
  let path = 'uploads';
  let bucket = fileDir;
  if (bucket) {
    path = path + '/' + bucket;
    if (!fs.existsSync(path)) {
      fs.mkdirSync(path, { recursive: true });
    }
  }
  return path + '/' + fileName;
};

class FilesController {
  static uploadRequest = async (req, res) => {
    try {
      if (!req.body || !req.body.fileKey) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Missing "fileKey"',
        );
      }
      if (!req.body || !req.body.fileDir) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Missing "fileDir"',
        );
      }
      if (!req.body || !req.body.fileName) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Missing "fileName"',
        );
      }
      let fileName = Random.getRandomUUID(); // new Date().getTime() / 1000;
      fileName = fileName.split('-').join('');
      fileName = fileName + Date.now();
      fileName = fileName.toUpperCase();
      let ext = path.extname(req.body.fileName).toLowerCase();
      if (!FILE_EXTENSIONS_HINT.includes(ext)) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Invalid file format. Supports only ' + FILE_EXTENSIONS_HINT,
        );
      }
      const fileId = fileName;
      fs.createWriteStream(getTempPath(req.body.fileKey, req.body.fileDir, fileId + ext), {
        flags: 'w',
      });
      return Api.response(
        res,
        req.headers.format,
        false,
        HTTP_STATUS.OK,
        HTTP_STATUS_MESSAGES.OK,
        1,
        { fileId: fileId, fileExt: ext, fileKey: req.body.fileKey, fileDir: req.body.fileDir },
      );
    } catch (e) {
      return Api.response(
        res,
        req.headers.format,
        true,
        HTTP_STATUS.SERVER_ERROR,
        HTTP_STATUS_MESSAGES.SERVER_ERROR,
      );
    }
  };
  static uploadStatus = async (req, res) => {
    try {
      if (
        req.query &&
        req.query.fileName &&
        req.query.fileId &&
        req.query.fileKey &&
        req.query.fileDir
      ) {
        const fileId = req.query.fileId;
        let ext = path.extname(req.query.fileName).toLowerCase();
        getFileDetails(getTempPath(req.query.fileKey, req.query.fileDir, fileId + ext))
          .then((stats) => {
            res.status(200).json({ totalChunkUploaded: stats.size });
          })
          .catch((err) => {
            console.error('failed to read file', err);
            return Api.response(
              res,
              req.headers.format,
              true,
              HTTP_STATUS.BAD_REQUEST,
              'No file with such credentials',
              1,
              { credentials: req.query },
            );
          });
      } else {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'No file with such credentials',
          1,
          { credentials: req.query },
        );
      }
    } catch (e) {
      return Api.response(
        res,
        req.headers.format,
        true,
        HTTP_STATUS.SERVER_ERROR,
        HTTP_STATUS_MESSAGES.SERVER_ERROR,
      );
    }
  };
  static upload = async (req, res) => {
    try {
      const contentRange = req.headers['content-range'];
      const fileId = req.headers['x-file-id'];
      const fileExt = req.headers['x-file-ext'];
      const fileKey = req.headers['x-file-key'];
      const fileDir = req.headers['x-file-dir'];

      if (!contentRange) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Missing "Content-Range" header',
        );
      }

      if (!fileId) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Missing "X-File-Id" header',
        );
      }

      if (!fileExt) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Missing "X-File-Ext" header',
        );
      }

      if (!fileKey) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Missing "X-File-Key" header',
        );
      }

      if (!fileDir) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Missing "X-File-Dir" header',
        );
      }

      const match = contentRange.match(/bytes=(\d+)-(\d+)\/(\d+)/);

      if (!match) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Invalid "Content-Range" Format',
        );
      }

      const rangeStart = Number(match[1]);
      const rangeEnd = Number(match[2]);
      const fileSize = Number(match[3]);
      if (fileSize > Number(FILE_MAX_SIZE)) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'File exceeds maximum size ' + FILE_MAX_SIZE_HINT + '.',
        );
      }

      if (rangeStart >= fileSize || rangeStart >= rangeEnd || rangeEnd > fileSize) {
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.BAD_REQUEST,
          'Invalid "Content-Range" provided',
        );
      }

      const busboy = Busboy({ headers: req.headers });

      busboy.on('file', (_, file, fileName) => {
        let ext = path.extname(fileName.filename).toLowerCase();
        const filePath = getTempPath(fileKey, fileDir, fileId + ext);
        if (!fileId) {
          req.pause();
        }
        getFileDetails(filePath)
          .then((stats) => {
            if (stats.size !== rangeStart) {
              return Api.response(
                res,
                req.headers.format,
                true,
                HTTP_STATUS.BAD_REQUEST,
                'Bad "chunk" provided',
              );
            }
            file.pipe(fs.createWriteStream(filePath, { flags: 'a' })).on('error', (e) => {
              console.error('failed upload', e);
              return Api.response(
                res,
                req.headers.format,
                true,
                HTTP_STATUS.BAD_REQUEST,
                'Unable to write into file.',
              );
            });
          })
          .catch((err) => {
            return Api.response(
              res,
              req.headers.format,
              true,
              HTTP_STATUS.SERVER_ERROR,
              'No file with such credentials',
              1,
              { credentials: req.query },
            );
          });
      });

      busboy.on('error', (e) => {
        console.error('failed upload', e);
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.SERVER_ERROR,
          'Unable to upload file.',
        );
      });

      busboy.on('finish', () => {
        const tempPath = getTempPath(fileKey, fileDir, fileId + fileExt);
        const uploadPath = getUploadsPath(fileKey, fileDir, fileId + fileExt);
        fs.renameSync(tempPath, uploadPath);
        let result = {
          key: fileKey,
          dir: fileDir,
          ext: fileExt,
          path: uploadPath,
        };
        return Api.response(
          res,
          req.headers.format,
          true,
          HTTP_STATUS.OK,
          HTTP_STATUS_MESSAGES.OK,
          1,
          result,
        );
      });

      req.pipe(busboy);
    } catch (e) {
      return Api.response(
        res,
        req.headers.format,
        true,
        HTTP_STATUS.SERVER_ERROR,
        HTTP_STATUS_MESSAGES.SERVER_ERROR,
      );
    }
  };
}

export default FilesController;
