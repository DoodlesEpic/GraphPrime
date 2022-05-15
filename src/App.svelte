<script lang="ts">
  import Chart from "svelte-frappe-charts";
  import { invoke } from "@tauri-apps/api/tauri";

  export let name: string;

  // Primes will be calculated upto this number
  let finalValue: number;

  // Hardcoded data upto 100 for initializing the chart
  let primes: number[] = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97,
  ];

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
    primes = await invoke("calculate", { x: finalValue });
  }
</script>

<main>
  <h1>Welcome to {name}!</h1>
  <p>
    Use this application to generate prime sequences and graph them all within
    the comfort of your desktop.
  </p>

  <input type="number" bind:value={finalValue} min="0" max="100000" />
  <button on:click={calculate}>Calculate</button>

  {#if primes}
    <p>
      {primes.join(", ")}
    </p>

    <Chart {data} type="line" />
  {/if}
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    font-size: 4em;
    font-weight: 100;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
