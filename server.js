const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const path = require('path');

const app = express();
const PORT = 5000;

// Your Google Sheet published URL
const SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS1sC2-QtEOVimTbL8SWV974iaFbBrEsU9Q1J63d61L01jzL5FRsgQSGyIOpn8X6A/pubhtml?gid=1066747437&single=true";

app.use(express.static(__dirname));

app.get('/api/data', async (req, res) => {
  try {
    const response = await axios.get(SHEET_URL);
    const $ = cheerio.load(response.data);

    const table = $('table').first();
    const rows = [];

    table.find('tr').each((i, tr) => {
      const cells = [];
      $(tr).find('th, td').each((j, cell) => {
        cells.push($(cell).text().trim());
      });
      if (cells.length > 0) {
        rows.push(cells);
      }
    });

    res.json({ data: rows });
  } catch (error) {
    console.error('Error:', error.message);
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
