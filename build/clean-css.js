#!/usr/bin/env node
/**
 * @license
 * Copyright 2016 RwandaSoft Ltd. All rights reserved.
 *
 */

const fs = require('fs');
const CleanCSS = require('clean-css');
const files = [
  'static/styles/inline.css',
  'static/styles/main.css',
];
const opts = {
  keepSpecialComments: 1
};

files.forEach(f => {
  fs.writeFileSync(f, new CleanCSS(opts).minify([f]).styles, 'utf8');
});
