import { HTTP_STATUS, HTTP_STATUS_MESSAGES } from '../constants/status.http';
import Api from '../helpers/api';
const axios = require('axios');
const cheerio = require('cheerio');

class NewsController {
  static fetch = async (req, res) => {
    try {
      let { url, div, link, title, image, details, datetime } = req.body;
      link = link.split(', ');
      title = title.split(', ');
      image = image.split(', ');
      details = details.split(', ');
      datetime = datetime.split(', ');

      let maxPages = 1;
      // initialized with the first webpage to visit
      const paginationURLsToVisit = [url];

      let visitedURLs = [];
      let items = [];

      // iterating until the queue is empty
      // or the iteration limit is hit
      while (paginationURLsToVisit.length !== 0 && visitedURLs.length <= maxPages) {
        // the current webpage to crawl
        const paginationURL = paginationURLsToVisit.pop();
        // retrieving the HTML content from paginationURL
        const pageHTML = await axios.get(paginationURL);
        // adding the current webpage to the
        // web pages already crawled
        visitedURLs.push(paginationURL);
        // initializing cheerio on the current webpage
        let $ = cheerio.load(pageHTML.data);
        let list = $(div);
        let div_link = $(link[0]);
        let div_title = $(title[0]);
        let div_image = $(image[0]);
        let div_details = $(details[0]);
        let div_datetime = $(datetime[0]);
        for (let index = 0; index < list.length; index++) {
          let el_link = div_link[index];
          let el_title = div_title[index];
          let el_image = div_image[index];
          let el_details = div_details[index];
          let el_datetime = div_datetime[index];
          const val_link = link.length == 1 ? $(el_link).html() : $(el_link).attr(link[1]);
          const val_title = title.length == 1 ? $(el_title).html() : $(el_title).attr(title[1]);
          const val_image = image.length == 1 ? $(el_image).html() : $(el_image).attr(image[1]);
          const val_details =
            details.length == 1 ? $(el_details).html() : $(el_details).attr(details[1]);
          const val_datetime =
            datetime.length == 1 ? $(el_datetime).html() : $(el_datetime).attr(datetime[1]);
          items.push({
            url: url,
            link: val_link,
            title: val_title,
            image: val_image,
            details: val_details,
            datetime: val_datetime,
          });
        }
      }

      // logging the crawling results
      return Api.response(
        res,
        req.headers.format,
        false,
        HTTP_STATUS.OK,
        HTTP_STATUS_MESSAGES.OK,
        items.length,
        items,
      );
    } catch (e) {
      return Api.response(res, req.headers.format, true, HTTP_STATUS.SERVER_ERROR, e.message);
    }
  };
}

export default NewsController;
