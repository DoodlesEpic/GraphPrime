<svelte:options runes={true} />

<script lang="ts">
  import GraphTypes from "../Util/GraphTypes.svelte";
  import DyGraphs from "../Util/DyGraphs.svelte";
  import Fa from "svelte-fa";
  import { faExpand } from "@fortawesome/free-solid-svg-icons";

  let {
    primes,
    chartType = $bindable(),
    chartFullscreen = $bindable()
  }: {
    primes: number[];
    chartType: string;
    chartFullscreen: boolean;
  } = $props();

  const csvChartData = $derived(
    ["X,Y\n"].concat(primes.map((prime, i) => `${i},${prime}\n`)).join("")
  );

  const options = $derived({
    data: csvChartData,
    fullscreen: chartFullscreen
  });
</script>

<div class="card" class:fullscreen={chartFullscreen} style="height: var(--graphHeight)">
  <GraphTypes bind:chartType />
  <div class="copyfullButtons">
    <button
      aria-label="Toggle graph fullscreen"
      onclick={() => (chartFullscreen = !chartFullscreen)}><Fa icon={faExpand} fw /></button
    >
  </div>

  <h2>Graph</h2>
  {#if primes.length === 0}
    <p>No prime numbers in this range.</p>
  {:else}
    <DyGraphs {options} class="chart" />
  {/if}
</div>
