<script lang="ts">
  import Fa from "svelte-fa";
  import { faExpand } from "@fortawesome/free-solid-svg-icons";
  import GraphTypes from "../Util/GraphTypes.svelte";
  import Chart from "svelte-frappe-charts";

  export let primes: number[];
  export let chartType: string;
  export let chartFullscreen: boolean;

  // Chart data, recalculated on every change of primes
  $: chartData = {
    labels: [...Array(primes.length).keys()].map((i) => i + 1),
    datasets: [
      {
        values: primes
      }
    ]
  };
</script>

<div class="card" class:fullscreen={chartFullscreen}>
  <GraphTypes bind:chartType />
  <div class="copyfullButtons">
    <button on:click={() => (chartFullscreen = !chartFullscreen)}><Fa icon={faExpand} fw /></button>
  </div>

  <h2>Graph</h2>
  {#if primes.length < 10000}
    <Chart data={chartData} type="line" />
  {:else}
    <p>Basic chart is disabled for more than 10000 prime numbers for performance reasons</p>
  {/if}
</div>
