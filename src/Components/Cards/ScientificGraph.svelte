<script lang="ts">
  import GraphTypes from "../Util/GraphTypes.svelte";
  import DyGraphs from "../Util/DyGraphs.svelte";
  import Fa from "svelte-fa";
  import { faExpand } from "@fortawesome/free-solid-svg-icons";

  export let primes: number[];
  export let chartType: string;
  export let chartFullscreen: boolean;

  // Chart data in csv format, recalculated on every change of primes
  $: csvChartData = ["X,Y\n"]
    .concat(primes.map((prime, i) => `${i},${prime}\n`))
    .join("");
</script>

<div
  class="card"
  class:fullscreen={chartFullscreen}
  style="height: var(--graphHeight)"
>
  <GraphTypes bind:chartType />
  <div class="copyfullButtons">
    <button on:click={() => (chartFullscreen = !chartFullscreen)}
      ><Fa icon={faExpand} fw /></button
    >
  </div>

  <h2>Graph</h2>
  <DyGraphs bind:data={csvChartData} class="chart" />
</div>
