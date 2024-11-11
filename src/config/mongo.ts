import { MongoClient } from 'mongodb';

const MongoDB = {
  DB: undefined,
  connect: (callback) => {
    MongoClient.connect(
      process.env.DATABASE_MONGO,
      {
        // useNewUrlParser: true,
        // useUnifiedTopology: true,
      },
      function (err, client) {
        if (err) {
          callback(err);
        }
        MongoDB.DB = client.db(process.env.DATABASE_NAME);
        console.info('Connected to database.');
        callback(null);
      },
    );
  },
};

export default MongoDB;
