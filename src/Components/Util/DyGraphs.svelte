<svelte:options runes={true} />

<script lang="ts">
  import { onMount } from "svelte";
  import Dygraph from "dygraphs";

  let {
    options = {
      data: "",
      fullscreen: false
    },
    class: classes = ""
  }: {
    options: { data: string; fullscreen: boolean };
    class?: string;
  } = $props();

  let element: HTMLElement;

  let graph = $state.raw<Dygraph>();

  onMount(() => {
    const chart = new Dygraph(element, options.data, {});
    graph = chart;
    return () => chart.destroy();
  });

  $effect(() => {
    graph?.updateOptions({ file: options.data });
  });

  $effect(() => {
    void options.fullscreen;
    graph?.resize();
  });
</script>

<div bind:this={element} class={classes}></div>

<style>
  .chart {
    position: absolute;
    inset: 100px 10px 10px 10px;
  }
</style>
