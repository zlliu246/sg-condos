<script setup>

const faqs = [
  {qn: "what is this?", ans: "For you to easily query condo transaction data using SQL"},
  {qn: "why did you start this project?", ans: "I was looking for condos to buy, and existing solutions were either paid or shit."},
  {qn: "do you earn money from this?", ans: "no, but if you strongly insist on giving me money, please feel free to do so."},
  {qn: "why did you expose this to the public?", ans: "I'll be sad if my hard work goes into the project graveyard just like that."},
  {qn: "what data is there?", ans: "1) condo transaction data 2) condo project data 3) some facility data"},
  {qn: "how is this data collected?", ans: "1) URA data 2) scraping 3) onemap API"},
  {qn: "tech used to collect data?", ans: "Python, Selenium, Onemap API, Airflow, Pandas etc"},
  {qn: "tech used for this site?", ans: "Vue, DuckDB, Netlify (this site has no backend)"},
  {qn: "how are we able to make SQL queries on this site?", ans: "DuckDB magic and static CSV files"},
  {qn: "how often will data be updated?", ans: "maybe every month? or when I feel like it"},
]

</script>

<template>
  <div class="p-4">
    <h3>Condo DB SG</h3>

    <table class="table table-striped table-dark">
      <thead>
        <tr>
          <th></th>
          <th>FAQ</th>
          <th>Answer</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(faq, i) in faqs">
          <td>{{ i+1 }}</td>
          <td>{{ faq.qn }}</td>
          <td>{{ faq.ans }}</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>