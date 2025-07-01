<!-- SCRIPT STARTS HERE -->
<script setup>

import axios from 'axios'
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router';

import DataTable from '../components/DataTable.vue'
import MetaDataTable from '../components/MetaDataTable.vue'
import { QUERY_MAP, SCHEMA_METADATA_LIST } from '../components/Constants.vue'

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

async function runQuery(db, query) {
    const conn = await db.connect()
    const response = (await conn.query(query))
    const result = response.toArray().map((row) => row.toJSON())
    return result
}

const state = reactive({
  db: null,
  query: QUERY_MAP.PROJECTS.query.trim(),
  tableData: [],
})

const router = useRouter()
const textareaRef = ref(null)

onMounted(() => {
  initDb().then(
    (db) => {
      state.db = db
      handleSubmitClick()
    }
  )
})

function handleSubmitClick() {
  runQuery(state.db, state.query).then(
    (result) => {
      state.tableData = result
      // console.log(state.tableData[0])
    }
  ).catch((error) => {
    alert(error)
  })
}

function handleSampleButtonClick(query) {
  state.query = query.trim()
}

function getTextAreaHeight() {
  try {
    return textareaRef.value.offsetHeight;
  } catch (error) {
    return 500
  }
}

function handleTextAreaKeyDownTabs(event) {
    if (event.key != "Tab") return
    event.preventDefault()
    const textarea = event.target
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const spaces = '    '
    textarea.value =
      textarea.value.substring(0, start) +
      spaces +
      textarea.value.substring(end)
}

</script>

<!-- TEMPLATE STARTS HERE -->
<template>
  <div class="p-4">

    <div>
      <div class="row">
        <div class="col-sm-6">

            <!-- TEXTAREA WHERE SQL QUERY GOES -->
            <textarea
              class="query-box form-control"
              rows="20"
              ref="textareaRef"
              style="font: monospace"
              v-model="state.query"
              @keydown="handleTextAreaKeyDownTabs"
            ></textarea>

        </div>

        <div class="col-sm-3" style="position:relative">

           <h6>Sample queries:</h6>

            <button 
              class="btn btn-secondary w-100 mb-2"
              @click="handleSampleButtonClick(QUERY_MAP[queryName].query)"
              v-for="queryName in Object.keys(QUERY_MAP)">
              {{ QUERY_MAP[queryName].desc }}
            </button>

            <!-- SUBMIT BUTTON -->
            <button class="btn btn-success w-100 position-absolute bottom-0 start-0" 
              @click="handleSubmitClick">
              Submit
            </button>

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
    </div>

</div>
</template>
