import * as nodemailer from 'nodemailer';
import MongoDB from '../config/mongo';
import { fetchDataFromTable } from '../config/mysql';


const environment = process.env;
// const MAIL_SENDER = environment.MAIL_SENDER;
// const MAIL_HOST = environment.MAIL_HOST;
// const MAIL_PORT = environment.MAIL_PORT;
// const MAIL_USERNAME = environment.MAIL_USERNAME;
// const MAIL_PASSWORD = environment.MAIL_PASSWORD;

// export const MailTransporter = nodemailer.createTransport({
//   host: MAIL_HOST,
//   port: MAIL_PORT,
//   secure: false,
//   tls: {
//     maxVersion: 'TLSv1.3',
//     minVersion: 'TLSv1.2',
//     rejectUnauthorized: false
//   },
//   auth: {
//     user: MAIL_USERNAME,
//     pass: MAIL_PASSWORD,
//   },
// });
// console.error(MailTransporter);
const Mail = {
  async sendBackground(subject, html, data) {
    const mailServerConfigData = await fetchDataFromTable();
    let doc = null;
    let dbo = MongoDB.DB;
    let collection = await dbo.collection('logs_email');
    let mailOptions = {
      from: mailServerConfigData.sender,
      to: data.emailTo,
      subject: subject,
      html: html,
    };
    doc = {
      userId: data.userId,
      type: data.type,
      model: data.model,
      modelId: data.modelId,
      emailFr: data.emailFr,
      emailTo: data.emailTo,
      emailCc: data.emailCc,
      subject: data.subject,
      message: data.message,
      body: html,
      createdAt: data.createdAt,
      updatedAt: data.updatedAt,
      attemptAt: data.attemptAt,
      attemptNo: 0,
      attemptResult: null,
    };
    try {
      const transporter = nodemailer.createTransport({
        host: mailServerConfigData.host,
        port: mailServerConfigData.port,
        secure: false,
        tls: {
          maxVersion: 'TLSv1.3',
          minVersion: 'TLSv1.2',
          rejectUnauthorized: false
        },
        auth: {
          user: mailServerConfigData.username,
          pass: mailServerConfigData.password,
        },
      });
      collection.insertOne(doc, async function (err, res) {
        if (err) {
          console.error(err);
        }
        let objectId = res['insertedId'];
        await transporter.sendMail(mailOptions, function (error, info) {
          if (error) {
            collection.updateOne(
              { _id: objectId },
              {
                $set: {
                  attemptResult: error,
                  updatedAt: new Date().getTime() / 1000,
                },
              },
            );
            console.error(error);
            return {
              error: true,
              message: error,
            };
          } else {
            collection.updateOne(
              { _id: objectId },
              {
                $set: {
                  attemptResult: info,
                  updatedAt: new Date().getTime() / 1000,
                },
              },
            );
            console.error(info);
            return {
              error: false,
              message: info,
            };
          }
        });
      });
    } catch (e) {
      console.error(e);
      return {
        error: true,
        message: e.message,
      };
    }
  },
};

export default Mail;
