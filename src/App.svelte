<script lang="ts">
  import Chart from "svelte-frappe-charts";
  import { invoke } from "@tauri-apps/api/tauri";
  import { slide } from "svelte/transition";
  import CodeMirror from "./CodeMirrorComponent.svelte";
  import DyGraphComponent from "./DyGraphComponent.svelte";
  import "./progress.css";

  export let name: string;

  // Primes will be calculated upto this number
  let finalValue: number;

  // Hardcoded data upto 100 for initializing the chart
  let primes: number[] = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97,
  ];

  let calculating = false;
  let calculationTime = 0;
  let compositeNumbers = 74; // Hardcoded value for the default prime numbers
  let chartType = "frappe";

  // Chart data in csv format, recalculated on every change of primes
  $: csvChartData = ["X,Y\n"]
    .concat(primes.map((prime, i) => `${i},${prime}\n`))
    .join("");

  // Chart data, recalculated on every change of primes
  $: chartData = {
    labels: [...Array(primes.length).keys()].map((i) => i + 1),
    datasets: [
      {
        values: primes,
      },
    ],
  };

  // Codemirror options
  $: options = {
    mode: "markdown",
    lineNumbers: false,
    lineWrapping: true,
    value: primes.join(", "),
  };

  // References to the CodeMirror and DyGraph instances
  let editor;
  let graph;

  async function calculate() {
    // Save because finalValue binds to input and may change during calculation
    const chosenFinalValue = finalValue;

    // Change chart to dygraph if we have too much data to prevent crashes
    if (chosenFinalValue >= 10000) chartType = "dygraph";
    else chartType = "frappe";

    // Start the timer
    calculating = true;
    const calculationStart = Date.now();

    // Calculate primes upto finalValue
    primes = await invoke("calculate", { x: finalValue });

    // Update stats
    calculationTime = (Date.now() - calculationStart) / 1000;
    compositeNumbers = chosenFinalValue - primes.length - 1; // -1 because 2 doesn't count as a composite number
    calculating = false;
  }
</script>

<main>
  <div class="card">
    <h1 class="title">Welcome to {name}!</h1>
    <p>
      Use this application to generate prime sequences and graph them all within
      the comfort of your desktop.
    </p>

    <div class="input-group">
      <input
        type="number"
        bind:value={finalValue}
        class="input"
        min="0"
        max="100000"
        placeholder="100"
      />
      <button on:click={calculate} class="button">Calculate</button>
    </div>
  </div>

  {#if calculating}
    <div class="bar card" in:slide out:slide />
  {/if}

  {#if primes}
    <div class="card">
      <h2>Stats</h2>
      <p>
        {primes.length} prime numbers calculated up to {primes.at(-1)}
      </p>
      <p>The calculation took {calculationTime} seconds</p>
      <p>
        There are {compositeNumbers} composite numbers up to {primes.at(-1)}
      </p>
    </div>

    <div id="primes" class="card">
      <h2>Primes</h2>
      <p>
        <CodeMirror bind:editor {options} class="editor" />
      </p>
    </div>

    {#if chartType === "frappe"}
      <div class="card">
        <select
          name="Graph Types"
          id="graphTypes"
          style="position: absolute; left: 10px"
          bind:value={chartType}
        >
          <option value="frappe">Basic</option>
          <option value="dygraph">Scientific</option>
        </select>
        <h2>Graph</h2>
        {#if primes.length < 10000}
          <Chart data={chartData} type="line" />
        {:else}
          <p>
            Basic chart is disabled for more than 10000 prime numbers for
            performance reasons
          </p>
        {/if}
      </div>
    {:else}
      <div class="card" style="height: 600px">
        <select
          name="Graph Types"
          id="graphTypes"
          style="position: absolute; left: 10px"
          bind:value={chartType}
        >
          <option value="frappe">Basic</option>
          <option value="dygraph">Scientific</option>
        </select>
        <h2>Graph</h2>
        <DyGraphComponent bind:data={csvChartData} class="chart" />
      </div>
    {/if}
  {/if}
</main>

<style>
  main {
    text-align: center;
    padding-bottom: 1em;
    max-width: none;
    margin: 0 auto;
    background: var(--main-bg);
    color: var(--body-color);
  }

  .title {
    color: #ff3e00;
    font-size: 3em;
    font-weight: 300;
  }

  .card {
    position: relative;
    background: var(--card-bg);
    /* Cast a nice shadow */
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    padding: 1em;
    margin: 1em;
  }

  #primes {
    /* Use the codemirror scroll for performance */
    overflow: hidden;
  }

  #primes p {
    /* Comfortable font for reading huge amounts of data */
    font-size: 1.1em;
    font-weight: 100;
    font-family: monospace;
    font-variant-numeric: tabular-nums;
  }

  .input-group {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 10px;
  }

  .input {
    max-width: 60%;
    flex-grow: 5;
    border: 1px solid var(--border-color);
    border-radius: 5px;
    font-size: 1.2em;
    font-weight: 100;
    font-family: monospace;
    background: var(--card-bg);
    color: var(--body-color);
  }

  .button {
    min-width: 100px;
    max-width: 20%;
    flex-grow: 1;
    border: none;
    border-radius: 5px;
    font-size: 1.2em;
    font-weight: 100;
    background-color: #00a8ff;
    color: white;
  }

  /* Light mode */
  :root {
    --border-color: #ccc;
    --card-bg: white;
    --main-bg: white;
    --body-color: #222;
  }

  /* Dark mode */
  @media (prefers-color-scheme: dark) {
    :root {
      --border-color: #ccc;
      --card-bg: #222;
      --main-bg: #111;
      --body-color: #ffffff;
    }
  }
</style>
