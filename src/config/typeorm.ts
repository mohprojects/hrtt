import 'reflect-metadata';
import { DataSource } from 'typeorm';
import dotenv = require('dotenv');
dotenv.config();

export const appDataSource = new DataSource({
  type: 'mysql',
  host: process.env.DATABASE_HOST,
  port: Number(process.env.DATABASE_PORT),
  database: process.env.DATABASE_NAME,
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD,
  timezone: 'Z',
  synchronize: false,
  logging: false,
  entities: [],
  migrations: ['src/migrations/**/*.ts'],
  subscribers: ['src/subscribers/**/*.ts'],
});
