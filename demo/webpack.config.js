/*
 * Webpack development server configuration
 *
 * This file is set up for serving the webpack-dev-server, which will watch for changes and recompile as required if
 * the subfolder /webpack-dev-server/ is visited. Visiting the root will not automatically reload.
 */

'use strict';

const webpack = require('webpack');
const path = require('path');
const ESLintPlugin = require('eslint-webpack-plugin');

module.exports = {
  mode: "development",

  entry: [
      './src/components/main.js'
  ],

  devServer: {
    contentBase: false,
    // send everything except /static/assets/main.js to the Python server
    // (hopefully that is localhost:5000!)
    proxy: {
      '/': 'http://localhost:5000'
    },
  },

  output: {
    path: path.resolve(__dirname, '../koboreports/static/assets/'),
    filename: 'main.js',
    publicPath: '/static/assets/'
  },

  resolve: {
    extensions: ['.js', '.jsx', '.css', '.scss'],
    alias: { // TODO: reconsider this for being too magical?
      'styles': path.resolve(__dirname, './src/styles'),
      'mixins': path.resolve(__dirname, './src/mixins'),
      'components': path.resolve(__dirname, './src/components/'),
      'stores': path.resolve(__dirname, './src/stores/'),
      'actions': path.resolve(__dirname, './src/actions/'),
    },
  },

  module: {
    rules: [
    {
      test: /\.(js|jsx)$/,
      exclude: /node_modules/,
      loader: 'babel-loader'
    }, {
      test: /\.css$/,
      use: ['style-loader', 'css-loader']
    }, {
      test: /\.s[ac]ss$/i,
      use: ['style-loader', 'css-loader', { loader: 'sass-loader', options: { sassOptions: {outputStyle: 'expanded'} } } ]
      //loader: 'style-loSader!css-loader!sass-loader?outputStyle=expanded'
    }, {
      test: /\.(png|jpg|woff|woff2)$/,
      use: [ { loader: 'url-loader', options: {limit: 8192} } ]
    }]
  },

  plugins: [
    new ESLintPlugin(),
  ]

};
