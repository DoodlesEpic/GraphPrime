<svelte:options runes={true} />

<script lang="ts">
  import Fa from "svelte-fa";
  import { faExpand } from "@fortawesome/free-solid-svg-icons";
  import GraphTypes from "../Util/GraphTypes.svelte";
  import FrappeChart from "../Util/FrappeChart.svelte";

  let {
    primes,
    chartType = $bindable(),
    chartFullscreen = $bindable()
  }: {
    primes: number[];
    chartType: string;
    chartFullscreen: boolean;
  } = $props();

  const chartData = $derived({
    labels: [...Array(primes.length).keys()].map((i) => i + 1),
    datasets: [
      {
        values: primes
      }
    ]
  });
</script>

<div class="card" class:fullscreen={chartFullscreen}>
  <GraphTypes bind:chartType />
  <div class="copyfullButtons">
    <button onclick={() => (chartFullscreen = !chartFullscreen)}><Fa icon={faExpand} fw /></button>
  </div>

  <h2>Graph</h2>
  {#if primes.length < 10000}
    <FrappeChart data={chartData} type="line" />
  {:else}
    <p>Basic chart is disabled for more than 10000 prime numbers for performance reasons</p>
  {/if}
</div>
