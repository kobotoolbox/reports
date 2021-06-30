const sass = require('node-sass');
const fs = require('fs');
const path = require('path');
const outputPath = path.resolve(__dirname, '../koboreports/static/login.css');
const result = sass.render({
  file: 'src/styles/DRFLogin.scss',
  outFile: outputPath
}, function(sassError, result) {
  if (!sassError) { // no errors during compilation
    fs.writeFile(outputPath, result.css, function(fsError) {
      if (!fsError) {
        //console.log("Don't take my word for it, but ... Success.");
        console.log('Successfully wrote the DRF login CSS to', outputPath);
      }
    });
  } else {
    console.error(sassError);
  }
});
