#!/usr/bin/env node

var defaultXmlPath = `${__dirname}/data/tabular.xml`

var fs = require('fs')
var xpath = require('xpath')
var dom = require('xmldom')
var program = require('commander')

function selectSubset (arr, limit) {
  // Return a subset of arr, retaining the order of the original
  while (arr.length > limit) {
    arr.splice(Math.floor(Math.random() * arr.length), 1)
  }
  return arr
}

program
  .description('Generate a JSON object containing ICD-10-CM codes.')
  .option('--random-subset [limit]',
          'Return a random subset to limit (default: 250)',
          parseInt)
  .option('--xml <path>',
          `Path to XML file of ICD-10 codes (default: ${defaultXmlPath})`,
          defaultXmlPath)
program.parse(process.argv)

if (program.randomSubset === true) {
  program.randomSubset = 250
}

fs.readFile(program.xml, function (err, data) {
  if (err) {
    return console.log(err)
  }

  var doc = new dom.DOMParser().parseFromString(String(data), 'text/xml')
  var nodes = xpath.select('//diag[name and desc]', doc)
  var codes = []

  nodes.forEach(function (node, index, arr) {
    codes.push({
      'code': node.getElementsByTagName('name')[0].textContent,
      'desc': node.getElementsByTagName('desc')[0].textContent
    })
  })

  console.log(JSON.stringify({
    'description': ('International Statistical Classification of Diseases ' +
                    'and Related Health Problems, 10th revision'),
    'source': 'http://www.cdc.gov/nchs/icd/icd10cm.htm',
    'codes': (program.randomSubset) ? selectSubset(codes, program.randomSubset)
                                    : codes
  }))
})
