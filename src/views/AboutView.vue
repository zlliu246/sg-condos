<script setup>

const faqs = [
  {cat: "project", qn: "what is this?", ans: "A simple project for you to easily query Singapore condo transaction data using SQL"},
  {cat: "project", qn: "what value can I gain by using this project?", ans: "You can easily query past condo transaction data (with augmentations eg. latitude/longitude values, number of units in project, TOP year, nearby amenities, distance from MRT etc)"},
  {cat: "project", qn: "but I can find this data on URA?", ans: "URA data doesn't have data on latitude/longitude, num_units, TOP year, nearby amenities etc"},
  {cat: "project", qn: "why did you start this project?", ans: "I was looking for condos to buy, and existing solutions were either paid or shit."},
  {cat: "project", qn: "do you earn money from this?", ans: "no, but if you strongly insist on giving me money, please feel free to do so."},
  {cat: "project", qn: "why did you expose this to the public?", ans: "I'll be sad if my hard work goes into the project graveyard just like that."},
  {cat: "data", qn: "what data is there?", ans: "1) condo transaction data 2) condo project data 3) some facility data"},
  {cat: "data", qn: "how is this data collected?", ans: "1) URA data 2) scraping 3) onemap API"},
  {cat: "data", qn: "how is this data updated?", ans: "I have one script that 1) pulls data from URA using selenium 2) cleans and deduplicates it 3) fetches additional info from different sources eg. num_nuits, top, developer, latitude, longitude 4) craft new CSV file"},
  {cat: "data", qn: "how often is data updated?", ans: "perhaps every month, as there are not that many condo transactions in Singapore"},
  {cat: "tech", qn: "tech used to collect data?", ans: "Python, Selenium, Onemap API, Airflow, Pandas etc"},
  {cat: "tech", qn: "tech used for this site?", ans: "Vue, DuckDB, Netlify (this site has no backend)"},
  {cat: "tech", qn: "how are we able to make SQL queries on this site?", ans: "DuckDB magic and static CSV files"},
  {cat: "data", qn: "Some of the data is screwed up", ans: "Yep, but I cannot look through 100k rows of data myself to verify it. Do send me an email if you see wrong data."},
  {cat: "data", qn: "There's no data before 2020?", ans: "Yep, URA only shows data from past 5 years. And data older than 5 years old isn't really that useful (my subjective opinion tho)"},
  {cat: "data", qn: "How do I do custom analysis on the data?", ans: "You can download it locally from <site> and analyse it yourself"},
]

/**
 * what data pipelines are used?
 * 
 */

</script>

<template>
  <div class="p-4" style="max-width:1600px">
    <h3>Condo DB SG</h3>

    <table class="table table-striped table-dark">
      <thead>
        <tr>
          <th></th>
          <th>Category</th>
          <th>FAQ</th>
          <th>Answer</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(faq, i) in faqs">
          <td>{{ i+1 }}</td>
          <td>{{ faq.cat }}</td>
          <td>{{ faq.qn }}</td>
          <td>{{ faq.ans }}</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>