<script lang="ts">
  import Chart from "svelte-frappe-charts";
  import { invoke } from "@tauri-apps/api/tauri";
  import { slide } from "svelte/transition";
  import CodeMirror from "./CodeMirrorComponent.svelte";
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

  // Chart data, recalculated on every change of primes
  $: data = {
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

  // Reference to the CodeMirror instance
  let editor;

  async function calculate() {
    // Start the timer and save the chosen final value
    // Since finalValue updates on input and could change during the calculation
    calculating = true;
    const calculationStart = Date.now();
    const chosenFinalValue = finalValue;

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
    <h1>Welcome to {name}!</h1>
    <p>
      Use this application to generate prime sequences and graph them all within
      the comfort of your desktop.
    </p>

    <input
      type="number"
      bind:value={finalValue}
      min="0"
      max="100000"
      placeholder="100"
    />
    <button on:click={calculate}>Calculate</button>
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

    <div class="card">
      <h2>Graph</h2>
      <Chart {data} type="line" />
    </div>
  {/if}
</main>

<style>
  main {
    text-align: center;
    padding-bottom: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    font-size: 3em;
    font-weight: 300;
  }

  .card {
    /* Cast a nice shadow */
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    padding: 1em;
    margin: 1em;
  }

  #primes {
    max-height: 500px;
    overflow: scroll;
  }

  #primes p {
    /* Comfortable font for reading huge amounts of data */
    font-size: 1.1em;
    font-weight: 100;
    font-family: monospace;
    font-variant-numeric: tabular-nums;
  }

  input {
    width: 70%;
    padding: 0.5em;
    margin-bottom: 1em;
    border: 1px solid #eee;
    border-radius: 5px;
    font-size: 1.2em;
    font-weight: 100;
    font-family: monospace;
  }
  button {
    width: 20%;
    padding: 0.5em;
    margin-bottom: 1em;
    border: 1px solid #eee;
    border-radius: 5px;
    font-size: 1.2em;
    font-weight: 100;
    font-family: monospace;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
