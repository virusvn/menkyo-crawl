import csv from 'csv';
import fs from 'fs';
import path from 'path';

import Kuroshiro from 'kuroshiro';
import KuromojiAnalyzer from 'kuroshiro-analyzer-kuromoji';
import YahooWebAnalyzer from 'kuroshiro-analyzer-yahoo-webapi';
import MecabAnalyzer from 'kuroshiro-analyzer-mecab';

const parse = csv.parse;
const analyzer = new KuromojiAnalyzer();

const yahoo_analyzer = new YahooWebAnalyzer({
  appId: 'dj00aiZpPTFvVEFzcFFrdXEwQyZzPWNvbnN1bWVyc2VjcmV0Jng9NTY-'
});

const mecab_analyzer = new MecabAnalyzer({
  dictPath: '/usr/local/lib/mecab/dic/mecab-ipadic-neologd/',
  execOptions: {
    maxBuffer: 200 * 1024,
    timeout: 0
  }
});

const kuroshiro = new Kuroshiro();
const mecab_kuroshiro = new Kuroshiro();
const yahoo_kuroshiro = new Kuroshiro();
async function initial() {
  await kuroshiro.init(analyzer);
  await mecab_kuroshiro.init(mecab_analyzer);
  await yahoo_kuroshiro.init(yahoo_analyzer);
}

async function convert_to_furigana(text) {
  let result;
  try {
    let result = await kuroshiro.convert(text, {
      mode: 'furigana'
    });
    if (result != text) {
      return result;
    }
    //fallback to mecab
    console.log('Fallback to mecab');
    result = await mecab_kuroshiro.convert(text, {
      mode: 'furigana'
    });
    if (result != text) {
      return result;
    }
    console.log('Fallback to yahoo');
    result = await yahoo_kuroshiro.convert(text, {
      mode: 'furigana'
    });
    return result;
  } catch (error) {
    console.log(error);
  }
  return result;
}

let output = 'anki_data_with_ruby.csv';
let input = 'anki_data_with_numbers.csv';
let parser = parse({ delimiter: ',' });
let transform = csv.transform(function(record) {
  //question
  convert_to_furigana(record[2]).then(function(res) {
    record[2] = res;
  });
  //anwser
  convert_to_furigana(record[3]).then(function(res) {
    record[3] = res;
  });

  return record;
});
var writer = fs.createWriteStream(path.normalize(__dirname + '/' + output));
var stringifier = csv.stringify();
initial().then(function() {
  fs.createReadStream(path.normalize(__dirname + '/' + input))
    .pipe(parser)
    .pipe(transform)
    .pipe(csv.stringify())
    .pipe(writer);
});
