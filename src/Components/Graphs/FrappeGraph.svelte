<script lang="ts">
  import Fa from "svelte-fa";
  import { faExpand } from "@fortawesome/free-solid-svg-icons";
  import GraphTypes from "./GraphTypes.svelte";
  import Chart from "svelte-frappe-charts";

  export let chartType: string;
  export let chartFullscreen: boolean;
  export let chartData: {
    labels: number[];
    datasets: { values: number[] }[];
  };
</script>

<div class="card" class:fullscreen={chartFullscreen}>
  <GraphTypes bind:chartType />
  <div class="copyfullButtons">
    <button on:click={() => (chartFullscreen = !chartFullscreen)}
      ><Fa icon={faExpand} fw /></button
    >
  </div>

  <h2>Graph</h2>
  {#if chartData.datasets.values.length < 10000}
    <Chart data={chartData} type="line" />
  {:else}
    <p>
      Basic chart is disabled for more than 10000 prime numbers for performance
      reasons
    </p>
  {/if}
</div>
