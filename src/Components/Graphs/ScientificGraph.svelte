<script lang="ts">
  import GraphTypes from "./GraphTypes.svelte";
  import DyGraphs from "../DyGraphs.svelte";
  import Fa from "svelte-fa";
  import { faExpand } from "@fortawesome/free-solid-svg-icons";

  export let chartType: string;
  export let chartFullscreen: boolean;
  export let csvChartData: string;
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
