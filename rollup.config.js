const intro = `/*!
 *
 * Copyright 2017 RwandaSoft Ltd. All rights reserved.
 *
 * Build: ${(new Date()).toISOString()}
 */`;

import cleanup from 'rollup-plugin-cleanup';
import eslint from 'rollup-plugin-eslint';

export default {
  entry: 'scripts/main.js',
  dest: 'static/scripts/main.js',
  plugins: [
    cleanup()
  ],
  intro
};
