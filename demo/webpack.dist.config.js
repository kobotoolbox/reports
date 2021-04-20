/*
 * Webpack distribution configuration
 *
 * This file is set up for serving the distribution version. It will be compiled to dist/ by default
 */

'use strict';

const webpack = require('webpack');
const path = require('path');
const ESLintPlugin = require('eslint-webpack-plugin');

module.exports = {
  mode: "production",

  entry: './src/components/main.js',

  output: {
    path: path.resolve(__dirname, '../koboreports/static/assets/'),
    filename: 'main.js',
    publicPath: '/assets/',
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

  plugins: [new ESLintPlugin()],

};
