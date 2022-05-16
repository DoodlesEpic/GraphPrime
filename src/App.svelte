<script lang="ts">
  import Chart from "svelte-frappe-charts";
  import { invoke } from "@tauri-apps/api/tauri";
  import "./progress.css";

  export let name: string;

  // Primes will be calculated upto this number
  let finalValue: number;

  // Hardcoded data upto 100 for initializing the chart
  let primes: number[] = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97,
  ];

  let calculating: boolean = false;

  // Chart data, recalculated on every change of primes
  $: data = {
    labels: [...Array(primes.length).keys()].map((i) => i + 1),
    datasets: [
      {
        values: primes,
      },
    ],
  };

  async function calculate() {
    calculating = true;
    primes = await invoke("calculate", { x: finalValue });
    calculating = false;
  }
</script>

<main>
  <div>
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
    <div class="bar" />
  {/if}

  {#if primes}
    <div id="primes">
      <p>
        {primes.join(", ")}
      </p>
    </div>

    <div><Chart {data} type="line" /></div>
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

  div {
    /* Cast a nice shadow */
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    padding: 1em;
    margin: 1em;
  }

  #primes {
    max-height: 500px;
    overflow: scroll;
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
