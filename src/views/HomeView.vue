<!-- SCRIPT STARTS HERE -->
<script setup>

import axios from 'axios'
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router';

import DataTable from '../components/DataTable.vue'
import MetaDataTable from '../components/MetaDataTable.vue'
import { DEFAULT_QUERIES, SCHEMA_METADATA_LIST } from '../components/Constants.vue'

import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import duckdb_wasm_next from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

async function initDb() {
  const MANUAL_BUNDLES = {
      mvp: {mainModule: duckdb_wasm, mainWorker: mvp_worker,},
      eh: {mainModule: duckdb_wasm_next, mainWorker: eh_worker},
  };
  const bundle = await duckdb.selectBundle(MANUAL_BUNDLES);
  const worker = new Worker(bundle.mainWorker);
  const logger = new duckdb.ConsoleLogger();
  const db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);

  const projectsContent = await (await fetch("/csvs/projects.csv")).text()
  const salesContent = await (await fetch("/csvs/sales.csv")).text()
  const projectsFacilitiesAssocContent = await (await fetch("/csvs/projects_facilities_assoc.csv")).text()
  await db.registerFileText('projects.csv', projectsContent)
  await db.registerFileText('sales.csv', salesContent)
  await db.registerFileText('projects_facilities_assoc.csv', projectsFacilitiesAssocContent)
  return db
}

const state = reactive({
  db: null,
  query: DEFAULT_QUERIES[0].query.trim(),
  tableData: [],
  messageToUser: '',
  savedQueryDesc: '',
  savedQueries: [],
})

const router = useRouter()
const textareaRef = ref(null)

onMounted(() => {
  loadSavedQueries()
  setUrlParamQueryIfExists()
  initDb().then(
    (db) => {
      state.db = db
      handleSubmitClick()
    }
  )
})

async function runQuery(db, query) {
    const conn = await db.connect()
    const response = (await conn.query(query))
    return response.toArray().map((row) => row.toJSON())
}

function setUrlParamQueryIfExists() {
  // eg. http://localhost:5173/?query=WITH+normalized+AS+%28%0A++++SELECT%0A++++++++project_name%2C+price%2C+psf%2C+sale_date%2C+sale_type%2C+floor_level%2C%0A++++++++CASE+%0A++++++++++++WHEN+area+%3C+600+THEN+%27%3C+600%27%0A++++++++++++WHEN+area+%3C+700+THEN+%27600+to+699%27%0A++++++++++++WHEN+area+%3C++800+THEN+%27700+to+799%27%0A++++++++++++WHEN+area+%3C+900+THEN+%27800+to+899%27%0A++++++++++++WHEN+area+%3C+1000+THEN+%27900+to+999%27%0A++++++++++++ELSE+%27%3E%3D+1000%27%0A++++++++END+as+area%0A++++FROM+%0A++++++++read_csv_auto%28%27sales.csv%27%29+sales%0A++++++++LEFT+JOIN+read_csv_auto%28%27projects.csv%27%29+projects%0A++++++++ON+sales.project_id+%3D+projects.id%0A++++WHERE+%0A++++++++project_name+%3D+%27forest+woods%27%0A%29%0ASELECT%0A++++MIN%28project_name%29+AS+project_name%2C%0A++++YEAR%28sale_date%29+AS+year%2C%0A++++floor_level%2C%0A++++area%2C%0A++++ROUND%28AVG%28price%29%29+AS+avg_price%2C%0A++++ROUND%28AVG%28psf%29%29+AS+avg_psf%0AFROM%0A++++normalized%0AGROUP+BY%0A++++YEAR%28sale_date%29%2C+floor_level%2C+area%0AORDER+BY%0A++++YEAR%28sale_date%29%2C+floor_level%2C+area
  const params = new URLSearchParams(window.location.search);
  const query = params.get('query')
  if (query != null) state.query = query
}

function getLocalStorageQueries() {
  let localQueries = JSON.parse(localStorage.getItem("savedQueries"))
  if (localQueries == null) return []
  return localQueries
}

function loadSavedQueries() {
  state.savedQueries = []
  let localQueries = getLocalStorageQueries()
  for (const row of localQueries) { state.savedQueries.push(row) }
  for (const row of DEFAULT_QUERIES) { state.savedQueries.push(row) }
}

function handleSubmitClick() {
  runQuery(state.db, state.query).then(
    (result) => { state.tableData = result }
  ).catch((error) => { alert(error) })
}

function handleSavedQueryButtonClick(savedQuery) {
  state.query = savedQuery.query.trim()
  let defaultQueryDescs = DEFAULT_QUERIES.map(row => row.desc)
  if (defaultQueryDescs.includes(savedQuery.desc)) return
  state.savedQueryDesc = savedQuery.desc
}

function getTextAreaHeight() {
  try {
    return textareaRef.value.offsetHeight;
  } catch (error) { return 500 }
}

function handleTextAreaKeyDownTabs(event) {
    if (event.key != "Tab") return
    event.preventDefault()
    const textarea = event.target
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const spaces = '    '
    textarea.value = textarea.value.substring(0, start) + spaces + textarea.value.substring(end)
}

function handleShareClick() {
  let url = new URL(window.location.origin + window.location.pathname);
  url.searchParams.append('query', state.query);
  window.history.pushState({}, '', url);
  navigator.clipboard.writeText(url).then(
    (res) => {
      state.messageToUser = 'Copied to clipboard';
      setTimeout(function() {state.messageToUser = ""}, 2000);
    }
  )
}

function handleSaveClick() {
  if (state.savedQueryDesc.length == 0) {
    alert("Please give your saved query a description")
    return
  }
  let savedQueries = []
  for (const row of getLocalStorageQueries()) {
    if (row.desc == state.savedQueryDesc) continue
    savedQueries.push(row)
  }
  savedQueries.push({
    desc: state.savedQueryDesc,
    query: state.query,
    type: 'localstorage'
  })
  localStorage.setItem("savedQueries", JSON.stringify(savedQueries));
  state.savedQueryDesc = ''
  loadSavedQueries()
}

function deleteLocalSavedQuery(desc) {
  let confirmation = window.confirm(`Confirm delete ${desc}?`)
  if (confirmation == false) {return}
  let savedQueries = getLocalStorageQueries()
  let newSavedQueries = []
  for (const row of savedQueries) {
    if (row.desc != desc) { newSavedQueries.push(row) }
  }
  localStorage.setItem("savedQueries", JSON.stringify(newSavedQueries))
  loadSavedQueries()
}

</script>

<!-- TEMPLATE STARTS HERE -->
<template>
  <div class="p-4">

    <div>
      <div class="row">
        <div class="col-sm-6" ref="textareaRef">

            <!-- TEXTAREA WHERE SQL QUERY GOES -->
            <textarea
              class="query-box form-control"
              rows="20"
              style="font-family: 'Courier New', Courier, monospace;"
              v-model="state.query"
              @keydown="handleTextAreaKeyDownTabs"
            ></textarea>

            <!-- SUBMIT BUTTON -->
            <div class="w-100 mt-2">

              <div style="display:flex">
                <button class="btn btn-success w-75 me-2" 
                  @click="handleSubmitClick"
                  title="Submits SQL query">
                  Submit
                </button>
                
                <button class="btn btn-primary w-50 me-2" 
                  @click="handleShareClick"
                  title="adds query to url params. Share url to share with friends">
                  Share
                </button>

                <input 
                  v-model="state.savedQueryDesc"
                  class="form-control me-2" 
                  placeholder="Describe saved query here">

                <button class="btn btn-danger w-50" 
                  @click="handleSaveClick"
                  title="save your query in localStorage">
                  Save
                </button>
              </div>

              <div style="color:limegreen" class="mb-2">{{ state.messageToUser }}</div>

            </div>

        </div>

        <div class="col-sm-3" style="position:relative;" 
          :style="{'max-height': `${getTextAreaHeight()}px`, 'overflow-y': 'scroll'}">

           <h6>Saved queries:</h6>

            <div v-for="savedQuery in state.savedQueries" 
              style="display:flex; ">

              <button 
                class="btn btn-secondary w-100 mb-2 btn-sm"
                @click="handleSavedQueryButtonClick(savedQuery)"
                >
                {{ savedQuery.desc }}
              </button>

              <button v-if="savedQuery.type=='localstorage'"
                class="btn btn-danger mb-2 ms-2 btn-sm"
                @click="deleteLocalSavedQuery(savedQuery.desc)">
                Delete
              </button>

            </div>

        </div>

        <div class="col-sm-3" :style="{'max-height': `${getTextAreaHeight()}px`, 'overflow-y': 'scroll'}">
          <div v-for="schemaMetadata in SCHEMA_METADATA_LIST" class="metadata-table">
            <MetaDataTable :schemaMetadata="schemaMetadata"/>
          </div>
        </div>

      </div>
    </div>

    <br>

    <div style="overflow: scroll">
      <DataTable :tableData="state.tableData" />
      <div v-if="state.tableData.length == 0">Loading</div>
    </div>

</div>
</template>
