const mysql = require('mysql2');

import { promisify } from 'util';

const pool = mysql.createPool({
    host: process.env.DATABASE_HOST,  
    user: process.env.DATABASE_USERNAME,      
    password:process.env.DATABASE_PASSWORD, 
    port:process.env.DATABASE_PORT, 
    database:process.env.DATABASE_NAME,  
  });

  const getConnection = promisify(pool.getConnection).bind(pool);
const query = promisify(pool.query).bind(pool);

export async function fetchDataFromTable() {
  try {
    const connection = await getConnection();
    try {
      const [rows, fields] = await query('SELECT * FROM App_MailServerConfig');
      console.log('Rows from the MailServerConfig table:', rows);
      // Process the rows or perform other operations
      return rows;
    } catch (error) {
      console.error('Error querying the table:', error);
    }
    connection.release(); // Release the connection back to the pool
  } catch (error) {
    console.error('Error getting connection from pool:', error);
  }
}
  