import 'reflect-metadata';
import MongoDB from './config/mongo';
import { appDataSource } from './config/typeorm';
import appRoutes from './routes/index';
import express = require('express');
import cors = require('cors');
import dotenv = require('dotenv');
import morgan = require('morgan');
import xss = require('xss-clean');
import helmet = require('helmet');
import compression = require('compression');
import cookieParser = require('cookie-parser');
import ExpressBrute = require('express-brute');
import MemcachedStore = require('express-brute-memcached');
const bodyParser = require('body-parser');
dotenv.config();

// initialize bruteForce
let store;
if (process.env.NODE_ENV === 'dev') {
  store = new ExpressBrute.MemoryStore(); // stores state locally, don't use this in production
} else {
  // stores state with memcached
  store = MemcachedStore;
}
const bruteForce = new ExpressBrute(store);

//Connects to the Database -> then starts the express
appDataSource
  .initialize()
  .then(async () => {
    const port = Number(process.env.NODE_PORT);
    const host = process.env.NODE_HOST;
    // Create a new express application instance
    const app = express();
    app.set('port', port);
    // Call middleware
    app.use(xss());
    app.use(helmet());
    app.use(compression());
    app.use(cookieParser());
    const corsOptions = {
      origin: '*',
      allowedHeaders: [
        'Content-Type',
        'Authorization',
        'Accept',
        'x-www-form-urlencoded',
        'x-requested-with',
        'x-auth',
        'x-file-id',
        'x-file-key',
        'x-file-dir',
        'x-file-ext',
        'content-range',
      ],
      credentials: true,
    };
    app.use(cors(corsOptions));
    // app.use(cors());
    app.use(express.json());
    app.use(express.static('resources'));
    app.use(express.urlencoded({ extended: true }));
    // body parser
    app.use(bodyParser());

    // enable logs
    if (process.env.NODE_ENV === 'dev') {
      app.use(morgan('dev'));
    }

    // connect to mongo
    MongoDB.connect((err) => {
      if (err) {
        console.error('Unable to connect to mongoose db: ', err);
        process.exit(1);
      }
    });

    // Set all routes from routes folder
    app.use('', appRoutes);

    app.listen(port, host, () => {
      console.log(`Server started on port ${port}!`);
    });
  })
  .catch((err) => {
    console.log('Unable to connect to database: ', err);
    process.exit(1);
  });
