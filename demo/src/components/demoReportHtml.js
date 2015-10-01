var demoReportHtml = `
<div class="container-fluid main-container">
  <div id="wealth-quintile-results" class="section level1">
    <h1>Wealth Quintile Results</h1>
    <p>2 respondents have been interviewed.</p>
    <p>Warning: Your sample is too small. Collect at least 100 responses to be representative.</p>
    <div id="national-quintile-results" class="section level2">
      <h2>National quintile results</h2>
      <p>These are the national quintile results for these respondents:</p>
      <table class="table table-condensed">
        <caption>Respondents by wealth quintile</caption>
        <thead>
          <tr class="header">
            <th align="left">Wealth quintile</th>
            <th align="left">Percentage of respondents</th>
          </tr>
        </thead>
        <tbody>
          <tr class="odd">
            <td align="left">4</td>
            <td align="left">100</td>
          </tr>
          <tr class="even">
            <td align="left">Total</td>
            <td align="left">100</td>
          </tr>
        </tbody>
      </table>
      <p>
        <img src="${require('../images/sample_graph.png')}" />
      </p>
      <p>The table above shows you the percentage of your respondents that were in each national wealth quintile.</p>
      <p>0% of your respondents were in the bottom two quintiles. This means that a relatively small number of respondents were poor. For more information on interpreting wealth quintile results, <a href="http://www.equitytool.org/wealth-quintiles/">please click here</a>.</p>
    </div>
    <div id="urban-quintile-results" class="section level2">
      <h2>Urban quintile results</h2>
      <p>These are the urban quintile results for these respondents:</p>
        <table class="table table-condensed">
          <caption>Respondents by wealth quintile</caption>
          <thead>
            <tr class="header">
              <th align="left">Wealth quintile</th>
              <th align="left">Percentage of respondents</th>
            </tr>
          </thead>
          <tbody>
            <tr class="odd">
              <td align="left">2</td>
              <td align="left">100</td>
            </tr>
            <tr class="even">
              <td align="left">Total</td>
              <td align="left">100</td>
            </tr>
          </tbody>
        </table>
        <img src="${require('../images/sample_graph.png')}" />
      </p>
      <p>The table above shows you the percentage of your respondents that were in each urban wealth quintile.</p>
      <p>100% of your respondents were in the bottom two quintiles. This means that a relatively large number of respondents were poor. For more information on interpreting wealth quintile results, <a href="http://www.equitytool.org/wealth-quintiles/">please click here</a>.</p>
    </div>
  </div>
</div>
`;
export default demoReportHtml;
